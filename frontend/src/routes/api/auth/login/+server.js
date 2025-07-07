import {AUTH_CLIENT_ID, AUTH_CLIENT_SECRET} from '$env/static/private';
import {json} from '@sveltejs/kit';
import {loginWithPassword, retrieveSelf} from '$lib/api/auth.js';

export async function POST({request, cookies}) {
    try {
        let user;
        const {email, password} = await request.json();

        const {access_token, refresh_token, expires_in} = await loginWithPassword({
            username: email,
            password,
            client_id: AUTH_CLIENT_ID,
            client_secret: AUTH_CLIENT_SECRET
        });

        const res = await retrieveSelf(access_token);
        if (res?.email && res?.id) {
            user = res;
        }

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
            user,
        }, {status: 200});
    } catch (e) {
        const status = e.status || 400;
        const message = e.message || 'Login Failed, please try again';
        return json({error: message}, {status});
    }
}
