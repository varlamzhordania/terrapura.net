import {fetchWithAuth} from "$lib/api/index.svelte.js";
import {API_ENDPOINTS} from "$lib/config.js";

// Fetch all addresses
export async function fetchAddresses({page = 1, page_size = 25, pagination = true}) {
    const params = new URLSearchParams()
    params.append("page", page)
    params.append("page_size", page_size)
    if (!pagination) params.append('pagination', 'false');

    return fetchWithAuth(`${API_ENDPOINTS.account.address}?${params.toString()}`, {
        method: "GET"
    });
}

// Fetch a single address by ID
export async function fetchAddress(id) {
    return fetchWithAuth(API_ENDPOINTS.account.addressDetail(id), {
        method: "GET"
    });
}

// Create a new address
export async function createAddress(data) {
    return fetchWithAuth(API_ENDPOINTS.account.address(0, 0, false), {
        method: "POST",
        body: data,
    });
}

// Update an existing address
export async function updateAddress(id, data) {
    return fetchWithAuth(API_ENDPOINTS.account.addressDetail(id), {
        method: "PUT",
        body: data,
    });
}

// Partially update an existing address (PATCH)
export async function patchAddress(id, data) {
    return fetchWithAuth(API_ENDPOINTS.account.addressDetail(id), {
        method: "PATCH",
        body: data,
    });
}

// Delete an address
export async function deleteAddress(id) {
    return fetchWithAuth(API_ENDPOINTS.account.addressDetail(id), {
        method: "DELETE"
    });
}

export async function updateAccount(data) {
    return fetchWithAuth(API_ENDPOINTS.account.me, {
        method: "PATCH",
        body: data
    })
}

export async function requestPasswordReset(data) {
    return fetchWithAuth(API_ENDPOINTS.account.passwordReset, {
        method: 'POST',
        body: data,
        useToken: false,
    });
}

export async function confirmPasswordReset(data) {
    return fetchWithAuth(API_ENDPOINTS.account.passwordResetConfirm, {
        method: 'POST',
        body: data,
        useToken: false,
    });
}
