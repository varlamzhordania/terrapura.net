const initialState = {
    access_token: null,
    refresh_token: null,
    logged_in: false,
    expire_in: null,
    user: null
}

export const authState = $state(initialState);

export function loadAuthStateFromStorage() {
    const access = localStorage.getItem('access_token');
    const refresh = localStorage.getItem('refresh_token');
    const expire = localStorage.getItem('expire_in');
    const user = localStorage.getItem('user');

    authState.access_token = access;
    authState.refresh_token = refresh;
    authState.expire_in = expire;
    authState.logged_in = !!access;
    authState.user = user ? JSON.parse(user) : null;
}

export function setAuth({access, refresh = null, expire_in = null, user = null}) {
    authState.access_token = access;
    authState.refresh_token = refresh;
    authState.expire_in = expire_in;
    authState.logged_in = true;
    authState.user = user;
}

export function clearAuth() {
    authState.access_token = null;
    authState.refresh_token = null;
    authState.expire_in = null;
    authState.logged_in = false;
    authState.user = null;

    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('expire_in');
    localStorage.removeItem('user');
}
