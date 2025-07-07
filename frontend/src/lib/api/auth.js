import {API_ENDPOINTS} from '$lib/config.js';
import {fetchWithAuth} from "$lib/api/index.js";

export async function retrieveSelf(token) {

    const res = await fetchWithAuth(API_ENDPOINTS.account.me, {
        token: token,
        parseJson: false,
    });

    if (!res.ok) {
        const data = await res.json();
        const err = new Error(data.error || data.detail || 'Something went wrong, please refresh the page.');
        err.status = res.status;
        throw err;
    }

    return await res.json();
}

export async function loginWithPassword({username, password, client_id, client_secret}) {

    const body = JSON.stringify({
        username,
        password,
        grant_type: 'password',
        client_id,
        client_secret,
    });

    const res = await fetch(API_ENDPOINTS.auth.token, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body,
    });

    if (!res.ok) {
        const data = await res.json();
        const err = new Error(data.error || 'Login failed');
        err.status = res.status;
        throw err;
    }

    return await res.json();
}

export async function refreshToken({refresh_token, client_id, client_secret}) {
    const body = JSON.stringify({
        refresh_token,
        grant_type: 'refresh_token',
        client_id,
        client_secret,
    });

    const res = await fetch(API_ENDPOINTS.auth.token, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body,
    });

    if (!res.ok) {
        const data = await res.json();
        const err = new Error(data.error || 'Refresh token failed');
        err.status = res.status;
        throw err;
    }

    return await res.json();
}

export async function revokeToken({token, client_id, client_secret}) {
    const body = JSON.stringify({
        token,
        client_id,
        client_secret
    });

    const res = await fetch(API_ENDPOINTS.auth.revokeToken, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            // 'Authorization':`Bearer ${token}`
        },
        body,
    });

    if (!res.ok) {
        const data = await res.json()
        console.log(data)
        throw new Error('Failed to revoke token');
    }

    return true;
}

export async function fetchCurrentUser(access_token) {
    const res = await fetch(API_ENDPOINTS.auth.me, {
        headers: {
            Authorization: `Bearer ${access_token}`,
        },
    });

    if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        const err = new Error(data.detail || 'Failed to fetch user');
        err.status = res.status;
        throw err;
    }

    return await res.json();
}

export async function convertSocialToken({backend, token}) {
    const body = new URLSearchParams({
        grant_type: 'convert_token',
        client_id: import.meta.env.VITE_OAUTH_CLIENT_ID,
        client_secret: import.meta.env.VITE_OAUTH_CLIENT_SECRET,
        backend,
        token,
    });

    const res = await fetch(API_ENDPOINTS.auth.convertToken, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body,
    });

    if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        const err = new Error(data.error_description || 'Social login failed');
        err.status = res.status;
        throw err;
    }

    return await res.json();
}
