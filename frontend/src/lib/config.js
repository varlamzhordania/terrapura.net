import {env} from "$env/dynamic/public"

const BASE_URL = env.API_BASE_URL || 'http://localhost:8000';
const API_BASE = `${BASE_URL}/api/v1`;

export const API_ENDPOINTS = {
        herbs: {
            self: `${API_BASE}/herbs/`,
            herbDetail: (slug) => `${API_BASE}/herbs/${slug}/`,
            herbOffers: (slug, currency) => `${API_BASE}/herbs/${slug}/offers/?currency=${currency}`,
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
            me: `${API_BASE}/account/`,
            address: `${API_BASE}/account/address/`,
            addressDetail: (id) => `${API_BASE}/account/address/${id}/`,
            passwordReset: `${BASE_URL}/api/v1/account/password-reset/`,
            passwordResetConfirm: `${BASE_URL}/api/v1/account/password-reset-confirm/`,
        },
        checkout: {
            currencies: `${API_BASE}/checkout/currencies/`,
            paymentMethods: (currency) => `${API_BASE}/checkout/payment-methods/?currency=${currency}`,
            basketPricesUpdate: (prices, currency) => `${API_BASE}/checkout/cart/prices/?ids=${prices}&currency=${currency}`,
            basket: `${API_BASE}/checkout/cart/`,
            basketWithCurrency: (currency) => `${API_BASE}/checkout/cart/?currency=${currency}`,
            orderCreate: `${API_BASE}/checkout/orders/create/`,
            orderList: (page, pageSize) => `${API_BASE}/checkout/orders/?page=${page}&page_size=${pageSize}`,
            orderDetail: (id) => `${API_BASE}/checkout/orders/${id}/`,
            stripe: `${API_BASE}/checkout/stripe/`,
        },
        partners: {
            partnerDetail: (id) => `${API_BASE}/partners/${id}/`,
            seller: {
                inventory: {
                    bases: (partnerId) => `${API_BASE}/partners/${partnerId}/inventory/base/`,
                    baseDetail: (partnerId, baseId) => `${API_BASE}/partners/${partnerId}/inventory/base/${baseId}/`,
                    products: (partnerId) => `${API_BASE}/partners/${partnerId}/inventory/product/`,
                    productDetail: (partnerId, productId) => `${API_BASE}/partners/${partnerId}/inventory/product/${productId}/`,
                },
                orders: (partnerId) => `${API_BASE}/partners/${partnerId}/orders/`,
                orderDetail: (partnerId, orderId) => `${API_BASE}/partners/${partnerId}/orders/${orderId}/`,
                staffs: (partnerId) => `${API_BASE}/partners/${partnerId}/staffs/`,
                staffDetail: (partnerId, staffId) => `${API_BASE}/partners/${partnerId}/staffs/${staffId}/`,
                financial: (partnerId) => `${API_BASE}/partners/${partnerId}/financial/`,
                settings: (partnerId) => `${API_BASE}/partners/${partnerId}/settings/`,
            },
        }
    }
;