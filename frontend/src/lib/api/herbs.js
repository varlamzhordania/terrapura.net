import {API_ENDPOINTS} from "$lib/config.js";


export async function fetchHerbs({
                                     category,
                                     tags,
                                     symptoms,
                                     search = '',
                                     ordering = '',
                                     pagination = true,
                                     page = 1
                                 } = {}) {
    const params = new URLSearchParams();
    params.append("page", page)
    if (category) params.append('category', category);
    if (tags) params.append('tags', tags);
    if (symptoms) params.append('symptoms', symptoms);
    if (search) params.append('search', search);
    if (ordering) params.append('ordering', ordering);
    if (!pagination) params.append('pagination', 'false');


    const res = await fetch(`${API_ENDPOINTS.herbs.self}?${params.toString()}`);
    if (!res.ok) throw new Error(`Failed to fetch herbs`);
    return await res.json();
}


export async function fetchHerbDetail(slug) {
    const res = await fetch(API_ENDPOINTS.herbs.herbDetail(slug));

    if (!res.ok) {
        let errDetail = `Failed to fetch herb detail for slug: ${slug}`;
        try {
            const data = await res.json();
            if (data.detail) errDetail = data.detail;
        } catch (_) {
            // response is not JSON, keep generic message
        }

        const err = new Error(errDetail);
        err.status = res.status;
        throw err;
    }

    return await res.json();
}


export async function fetchCategories({pagination = false} = {}) {
    const params = new URLSearchParams();
    if (!pagination) params.append('pagination', 'false');

    const res = await fetch(`${API_ENDPOINTS.herbs.categories}?${params.toString()}`);
    if (!res.ok) throw new Error(`Failed to fetch categories`);
    return await res.json();
}


export async function fetchTags({pagination = false} = {}) {
    const params = new URLSearchParams();
    if (!pagination) params.append('pagination', 'false');

    const res = await fetch(`${API_ENDPOINTS.herbs.tags}?${params.toString()}`);
    if (!res.ok) throw new Error(`Failed to fetch tags`);
    return await res.json();
}


export async function fetchSymptom({pagination = false} = {}) {
    const params = new URLSearchParams();
    if (!pagination) params.append('pagination', 'false');

    const res = await fetch(`${API_ENDPOINTS.herbs.symptoms}?${params.toString()}`);
    if (!res.ok) throw new Error(`Failed to fetch symptoms`);
    return await res.json();
}
