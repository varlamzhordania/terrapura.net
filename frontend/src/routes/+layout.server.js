import {refreshToken, retrieveSelf} from "$lib/api/auth.js";
import {AUTH_CLIENT_ID, AUTH_CLIENT_SECRET} from '$env/static/private';

export async function load({cookies}) {
    let user = null;

    let access_token = cookies.get('access_token');
    const refresh_token = cookies.get('refresh_token');

    if (access_token) {
        try {
            const res = await retrieveSelf(access_token);
            if (res?.email && res?.id) {
                user = res;
            }
        } catch (e) {
            // If token is invalid or expired
            access_token = null;
            cookies.set('access_token', '', {
                path: '/',
                expires: new Date(0),
                httpOnly: true,
                secure: true,
                sameSite: 'Strict',
            });
        }
    }

    if (!access_token && refresh_token) {
        try {
            const refreshed = await refreshToken({
                refresh_token,
                client_id: AUTH_CLIENT_ID,
                client_secret: AUTH_CLIENT_SECRET
            });

            access_token = refreshed.access_token;

            cookies.set('access_token', refreshed.access_token, {
                path: '/',
                httpOnly: true,
                secure: true,
                sameSite: 'Strict',
                maxAge: refreshed.expires_in, // usually in seconds
            });

            cookies.set('refresh_token', refreshed.refresh_token, {
                path: '/',
                httpOnly: true,
                secure: true,
                sameSite: 'Strict',
                maxAge: 60 * 60 * 24 * 7, // 7 days
            });

            const res = await retrieveSelf(access_token);
            if (res?.email && res?.id) {
                user = res;
            }
        } catch (e) {
            // Refresh failed, clear refresh_token
            cookies.set('refresh_token', '', {
                path: '/',
                expires: new Date(0),
                httpOnly: true,
                secure: true,
                sameSite: 'Strict',
            });
        }
    }

    return {
        user,
        access_token
    };
}
