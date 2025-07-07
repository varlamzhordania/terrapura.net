import {json} from '@sveltejs/kit';

export async function GET({cookies}) {
    const token = cookies.get('access_token');
    if (!token) {
        return json({error: 'You are not logged in.'}, {status: 401});
    }

    try {
        cookies.set('access_token', '', {
            path: '/',
            expires: new Date(0),
            httpOnly: true,
            secure: true,
            sameSite: 'Strict',
        });

        cookies.set('refresh_token', '', {
            path: '/',
            expires: new Date(0),
            httpOnly: true,
            secure: true,
            sameSite: 'Strict',
        });

        return json({success: true, message: "Logout successful."}, {status: 200})
    } catch (e) {
        return json({error: 'Failed to revoke token'}, {status: 401});
    }
}
