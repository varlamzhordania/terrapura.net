import {authState} from '$lib/states/auth.svelte.js';

export async function fetchWithAuth(url, {
    method = 'GET',
    body = null,
    token = null,
    headers = {},
    parseJson = true,
    retry = true  // only retry once on 401
} = {}) {
    const finalHeaders = {
        'Content-Type': 'application/json',
        ...headers
    };

    const accessToken = token || authState.access_token;

    if (accessToken) {
        finalHeaders['Authorization'] = `Bearer ${accessToken}`;
    }

    const res = await fetch(url, {
        method,
        headers: finalHeaders,
        body: body ? JSON.stringify(body) : null,
    });

    if (res.status === 401 && retry) {
        // Try to refresh token
        const refreshRes = await fetch('/api/auth/refresh-token', {method: 'POST'});
        if (refreshRes.ok) {
            const {access_token, expires_in} = await refreshRes.json();
            authState.access_token = access_token;
            authState.expire_in = expires_in

            // Retry original request with new token
            return await fetchWithAuth(url, {
                method,
                body,
                headers,
                parseJson,
                token: access_token,
                retry: false  // prevent infinite retry loop
            });
        } else {
            const err = new Error('Unauthorized: Refresh token expired or invalid.');
            err.status = 401
            throw err
        }
    }

    if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`HTTP ${res.status}: ${errorText}`);
    }

    return parseJson ? await res.json() : res;
}
