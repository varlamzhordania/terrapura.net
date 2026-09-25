<script>
    import {page} from "$app/state";
    import {fetchBases, fetchProductByPK, updateProduct} from "$lib/api/seller.js";
    import {partnerState} from "$lib/states/partner.svelte.js";
    import {fetchHerbs} from "$lib/api/herbs.js";
    import AutoCompleteSelect from "$lib/components/AutoCompleteSelect.svelte";
    import {notFoundImage} from "$lib";
    import Spinner from "$lib/components/Spinner.svelte";
    import Fa from "svelte-fa";
    import {faSave, faTrash, faTrashCan} from "@fortawesome/free-solid-svg-icons";
    import Toast from "$lib/toast.js";


    let item = $state(null)
    let bases = $state([])
    let submitLoading = $state(false)
    let selectedHerb = $derived(item ? item.herb : null)
    let selectedBase = $derived(item ? item.base.id : null)


    const loadItem = async (partner_id, pk) => {
        item = await fetchProductByPK(partner_id, pk)
    }

    const loadHerbs = async (inputValue) => {
        const res = await fetchHerbs({page_size: 20, search: inputValue})
        if (res)
            return res.results
        return []
    }

    const loadBases = async (partner_id) => {
        bases = await fetchBases({partner_id: partner_id, pagination: false})
    }

    const getThumbnail = () => {
        if (!selectedHerb) return notFoundImage;
        if (selectedHerb.media) return selectedHerb.media.file;

        const images = selectedHerb.medias?.filter(img => img.type === "IMAGE" && img.file) || [];
        return images.find(img => img.is_featured)?.file || images[0]?.file || notFoundImage;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!selectedHerb?.id || !partnerState?.partner?.id) {
            Toast.error("Missing required data for submission.");
            return;
        }

        const preparedData = {
            herb: selectedHerb.id,
            base: selectedBase,
            quantity: item.quantity,
            quantity_unit: "kg",
            expiration_date: item.expiration_date,
            is_available: item.is_available,
            low_stock_threshold: item.low_stock_threshold,
        };

        submitLoading = true;

        try {
            await updateProduct(preparedData, partnerState.partner.id, page.params.pk);
            Toast.success("Changes saved successfully.")
        } catch (error) {
            Toast.error("Operation did failed, try again.")
        } finally {
            submitLoading = false;
        }
    };


    $effect(() => {
        loadItem(partnerState.partner.id, page.params.pk)
        loadBases(partnerState.partner.id)
    })

</script>

{#if item}
    <div class="grid grid-cols-1 md:grid-cols-12 lg:grid-cols-12 gap-2">
        <div class="col-span-1 md:col-span-7 lg:col-span-7 space-y-2 order-2 md:order-1">
            <form onsubmit={handleSubmit} class="space-y-2">

                <div class="card card-border">
                    <h2 class="text-2xl font-semibold capitalize">
                        Information
                    </h2>
                    <div class="">
                        <div class="space-y-2">
                            <div>
                                <AutoCompleteSelect
                                        label="Product"
                                        placeholder="Search herb by name..."
                                        id="input-product"
                                        fetcher={loadHerbs}
                                        bind:value={selectedHerb}
                                        getLabel={(h) => h.name}
                                        getValue={(h) => h}
                                        required
                                        disabled
                                />
                            </div>
                            <div>
                                <label for="input-base" class="form-control-label">
                                    Inventory Base
                                </label>
                                <select id="input-base" class="form-control-field" bind:value={selectedBase} required
                                        disabled>
                                    {#each bases as base}
                                        <option value={base.id}>{base.name}</option>
                                    {/each}
                                </select>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card card-border">
                    <h2 class="text-2xl font-semibold capitalize">
                        Stock
                    </h2>
                    <div class="">
                        <div class="space-y-2">
                            <div>
                                <label for="input-quantity" class="form-control-label">
                                    Quantity
                                </label>
                                <input type="number" id="input-quantity" class="form-control-field"
                                       bind:value={item.quantity}/>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card card-border">
                    <h2 class="text-2xl font-semibold capitalize">
                        Prices
                    </h2>
                    <div class="">
                        <div class="space-y-2">
                            <div>
                                <label for="input-quantity" class="form-control-label">
                                    Quantity
                                </label>
                                <input type="number" id="input-quantity" class="form-control-field"/>
                            </div>
                        </div>
                    </div>
                </div>


                <div class="flex gap-2 flex-wrap md:flex-nowrap">
                    <button type="submit" class="btn btn-primary w-full">
                        {#if submitLoading}
                            <Spinner size="xs"/>
                        {:else}
                            <Fa icon={faSave} size="lg"/>
                            Save changes
                        {/if}

                    </button>
                    <button type="button" class="btn btn-danger btn-outline w-full">
                        <Fa icon={faTrash} size="lg"/>
                        Delete product
                    </button>
                </div>
            </form>
        </div>
        <div class="col-span-1 md:col-span-5 lg:col-span-5 order-1 md:order-1">
            <div class="card card-border flex lg:flex-nowrap gap-2">
                <div class="w-full max-w-20">
                    <a href="/herbs/{selectedHerb?.slug}" target="_blank">
                        <img src={getThumbnail()} alt={selectedHerb?.name}
                             class="aspect-square object-cover size-20 rounded-sm"/>
                    </a>
                </div>
                <div class="flex justify-between items-start flex-wrap w-full">
                    <div class="space-y-2">
                        <a href="/herbs/{selectedHerb?.slug}" target="_blank">
                            <h3 class="text-xl font-bold">{selectedHerb?.name}</h3>
                        </a>
                        <p class="text-xs italic text-slate-600 font-medium">
                            also known as : {selectedHerb?.latin_name}
                        </p>
                        <a href="/herbs/{selectedHerb?.slug}" class="link link-info">more</a>
                    </div>
                    <span class="badge badge-info text-base">{selectedHerb?.category}</span>
                </div>
            </div>
        </div>

    </div>
{:else }
    <div class="w-full h-full flex justify-center items-center">
        <Spinner size="lg"/>
    </div>
{/if}
