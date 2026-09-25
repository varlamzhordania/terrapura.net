import {fetchWithAuth} from "$lib/api/index.svelte.js";
import {API_ENDPOINTS} from "$lib/config.js";

export const fetchPartnerDetail = async (id) => {
    return await fetchWithAuth(API_ENDPOINTS.partners.partnerDetail(id))
}