import {fetchWithAuth} from "$lib/api/index.svelte.js";
import {API_ENDPOINTS} from "$lib/config.js";

export const fetchBases = async ({
                                     partner_id,
                                     page = 1,
                                     page_size = 25,
                                     pagination = true,
                                     search = "",
                                 }) => {
    const params = new URLSearchParams()
    params.append("page", page)
    params.append("page_size", page_size)
    if (search.length > 0) params.append("search", search)
    if (!pagination) params.append('pagination', 'false');
    return await fetchWithAuth(`${API_ENDPOINTS.partners.seller.inventory.bases(partner_id)}?${params.toString()}`)
}

export const fetchBaseByPK = async (partner_id, pk) => {
    return await fetchWithAuth(API_ENDPOINTS.partners.seller.inventory.baseDetail(partner_id, pk))
}

export const fetchProducts = async ({
                                        partner_id,
                                        page = 1,
                                        page_size = 25,
                                        pagination = true,
                                        search = "",
                                    }) => {
    const params = new URLSearchParams()
    params.append("page", page)
    params.append("page_size", page_size)
    if (search.length > 0) params.append("search", search)
    if (!pagination) params.append('pagination', 'false');
    return await fetchWithAuth(`${API_ENDPOINTS.partners.seller.inventory.products(partner_id)}?${params.toString()}`)
}

export const fetchProductByPK = async (partner_id, pk) => {
    return await fetchWithAuth(API_ENDPOINTS.partners.seller.inventory.productDetail(partner_id, pk))
}

export const updateProduct = async (data, partner_id, pk) => {
    return await fetchWithAuth(`${API_ENDPOINTS.partners.seller.inventory.productDetail(partner_id, pk)}`, {
        method: "PUT",
        body: data,
    })
}