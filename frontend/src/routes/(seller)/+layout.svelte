<script>
    import {partnerState} from "$lib/states/partner.svelte.js";
    import {fetchPartnerDetail} from "$lib/api/partners.js";

    let {children} = $props();

    const loadPartnerDetail = async (id) => {
        partnerState.partner = await fetchPartnerDetail(id)
    }

    $effect(() => {
        if (partnerState.role?.partner_id) {
            loadPartnerDetail(partnerState.role?.partner_id)
        }
    })


</script>

<div>
    {@render children()}
</div>