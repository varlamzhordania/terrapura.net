import {authState} from '$lib/states/auth.svelte.js';
import Toast from "$lib/toast.js";


/**
 * Fetch wrapper that automatically adds auth token and retries once on 401.
 * Throws structured errors: { status, data }
 *
 * @template T
 * @param {string} url - The request URL.
 * @param {Object} [options={}] - Optional fetch settings.
 * @param {'GET'|'POST'|'PUT'|'PATCH'|'DELETE'} [options.method='GET'] - HTTP method.
 * @param {any} [options.body=null] - Request body. Will be JSON.stringified if provided.
 * @param {string|null} [options.token=null] - Override access token. Defaults to `authState.access_token`.
 * @param {boolean} [options.useToken=true] - Override use access token. Defaults to true.
 * @param {Record<string, string>} [options.headers={}] - Extra request headers.
 * @param {boolean} [options.parseJson=true] - Whether to parse the response as JSON.
 * @param {boolean} [options.retry=true] - Whether to retry once on 401.
 * @returns {Promise<T|Response>} Resolves with parsed JSON or raw Response.
 * @throws {Error} If request fails or unauthorized.
 */
export async function fetchWithAuth(
    url,
    {
        method = 'GET',
        body = null,
        token = null,
        useToken = true,
        headers = {},
        parseJson = true,
        retry = true
    } = {}
) {
    const finalHeaders = {
        'Content-Type': 'application/json',
        ...headers
    };

    const accessToken = token || authState.access_token;

    if (accessToken && useToken) {
        finalHeaders['Authorization'] = `Bearer ${accessToken}`;
    }

    const res = await fetch(url, {
        method,
        headers: finalHeaders,
        body: body ? JSON.stringify(body) : null,
    });

    if (res.status === 401 && retry) {
        const refreshRes = await fetch('/api/auth/refresh-token', {method: 'POST'});
        if (refreshRes.ok) {
            const {access_token, expires_in} = await refreshRes.json();
            authState.access_token = access_token;
            authState.expire_in = expires_in;

            return await fetchWithAuth(url, {
                method,
                body,
                headers,
                parseJson,
                token: access_token,
                retry: false
            });
        } else {
            const msg = 'Unauthorized: Please log in again.';
            Toast.error(msg);
            throw {status: 401, data: {detail: msg}};
        }
    }


    // Helper to safely parse JSON if it exists
    const safeParseJson = async () => {
        const contentType = res.headers.get('content-type') || '';
        const contentLength = res.headers.get('content-length');
        if (!contentType.includes('application/json') || contentLength === '0' || res.status === 204) {
            return null;
        }
        try {
            return await res.json();
        } catch {
            return null;
        }
    };

    if (!res.ok) {
        let errorData;
        try {
            errorData = await res.json();
        } catch {
            errorData = {detail: await res.text()};
        }

        let messages = [];

        if (errorData.detail) {
            // DRF "detail" error (single string)
            messages.push(errorData.detail);
        } else if (typeof errorData === 'object' && errorData !== null) {
            // Django validation errors (field -> [messages])
            for (const [field, errs] of Object.entries(errorData)) {
                if (Array.isArray(errs)) {
                    errs.forEach(err => {
                        // Capitalize field name for nicer display
                        const fieldName = field.replace(/_/g, ' ');
                        messages.push(`${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)}: ${err}`);
                    });
                } else if (typeof errs === 'string') {
                    messages.push(errs);
                }
            }
        } else {
            // Fallback to raw text
            messages.push(`Error ${res.status}`);
        }

        // Show each message as a separate toast
        messages.forEach(msg => Toast.error(msg));

        throw {status: res.status, data: errorData};
    }

    return parseJson ? await safeParseJson() : res;
}
