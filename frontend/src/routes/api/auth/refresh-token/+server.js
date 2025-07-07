import {json} from '@sveltejs/kit';
import {AUTH_CLIENT_ID, AUTH_CLIENT_SECRET} from '$env/static/private';
import {refreshToken} from '$lib/api/auth.js';

export async function POST({cookies}) {
    const refresh_token = cookies.get('refresh_token');
    if (!refresh_token) {
        return json({error: 'No refresh token'}, {status: 401});
    }

    try {
        const {access_token, refresh_token, expires_in} = await refreshToken({
            refresh_token,
            client_id: AUTH_CLIENT_ID,
            client_secret: AUTH_CLIENT_SECRET
        });

        cookies.set('access_token', access_token, {
            path: '/',
            httpOnly: true,
            sameSite: 'lax',
            maxAge: expires_in,
            secure: true,
        });

        cookies.set('refresh_token', refresh_token, {
            path: '/',
            httpOnly: true,
            sameSite: 'lax',
            maxAge: 60 * 60 * 24 * 7, // 7 days
            secure: true,
        });

        return json({
            access_token,
            expires_in,
        }, {status: 200});
    } catch (e) {
        return json({error: 'Failed to refresh token'}, {status: 401});
    }
}
