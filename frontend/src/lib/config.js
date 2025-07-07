import {env} from "$env/dynamic/public"

const BASE_URL = env.API_BASE_URL || 'http://localhost:8000';
const API_BASE = `${BASE_URL}/api/v1`;

export const API_ENDPOINTS = {
    herbs: {
        self: `${API_BASE}/herbs/`,
        herbDetail: (slug) => `${API_BASE}/herbs/${slug}/`,
        categories: `${API_BASE}/herbs/categories/`,
        tags: `${API_BASE}/herbs/tags/`,
        symptoms: `${API_BASE}/herbs/symptoms/`,
    },
    auth: {
        authorize: `${BASE_URL}/api/auth/authorize/`,
        token: `${BASE_URL}/api/auth/token/`,
        refresh: `${BASE_URL}/api/auth/token/`,
        convertToken: `${BASE_URL}/api/auth/convert-token/`,
        revokeToken: `${BASE_URL}/api/auth/revoke-token/`,
        invalidateSessions: `${BASE_URL}/api/auth/invalidate-sessions/`,
        invalidateRefreshTokens: `${BASE_URL}/api/auth/invalidate-refresh-tokens/`,
        disconnectBackend: `${BASE_URL}/api/auth/disconnect-backend/`,
        social: {
            login: (backend) => `${BASE_URL}/api/auth/login/${backend}/`,
            complete: (backend) => `${BASE_URL}/api/auth/complete/${backend}/`,
            disconnect: (backend) => `${BASE_URL}/api/auth/disconnect/${backend}/`,
            disconnectById: (backend, id) => `${BASE_URL}/api/auth/disconnect/${backend}/${id}/`,
        },
    },
    account: {
        me: `${API_BASE}/account/me/`,
    },
};