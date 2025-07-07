import {error} from "@sveltejs/kit";
import {fetchHerbDetail} from "$lib/api/herbs.js";

export const load = async ({params}) => {
    try {
        const slug = params.slug;
        const response = await fetchHerbDetail(slug);

        if (response.detail && response.detail === "No Herb matches the given query.") {
            throw error(404, response.detail);
        }

        return response

    } catch (e) {
        if (e.status && e.message) {
            throw error(e.status, e.message);
        }
        throw error(400, 'Failed to load herb data');
    }
};
