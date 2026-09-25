<script>
    import {page} from "$app/state";
    import {fetchBaseByPK, updateProduct} from "$lib/api/seller.js";
    import {partnerState} from "$lib/states/partner.svelte.js";
    import AutoCompleteSelect from "$lib/components/AutoCompleteSelect.svelte";
    import Spinner from "$lib/components/Spinner.svelte";
    import Fa from "svelte-fa";
    import {faSave, faTrash} from "@fortawesome/free-solid-svg-icons";
    import Toast from "$lib/toast.js";


    let item = $state(null)
    let submitLoading = $state(false)


    const loadItem = async (partner_id, pk) => {
        item = await fetchBaseByPK(partner_id, pk)
    }

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
    })

    $inspect(item)

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
                                <label for="input-name" class="form-control-label">
                                    Name
                                </label>
                                <input type="text" id="input-name" class="form-control-field"
                                       placeholder="Enter a name for the inventory base..."
                                       bind:value={item.name} required>
                            </div>
                            <div>
                                <label for="input-region" class="form-control-label">
                                    Contact Person
                                </label>
                                <input type="text" id="input-region" class="form-control-field"
                                       placeholder="Enter the information of contact person..."
                                       bind:value={item.contact_person} required>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card card-border">
                    <h2 class="text-2xl font-semibold capitalize">
                        Location
                    </h2>
                    <div class="">
                        <div class="space-y-2">
                            <div>
                                <label for="input-region" class="form-control-label">
                                    Region
                                </label>
                                <input type="text" id="input-region" class="form-control-field"
                                       placeholder="Enter the region of base..."
                                       bind:value={item.region} required>
                            </div>
                            <div>
                                <label for="input-region" class="form-control-label">
                                    Address
                                </label>
                                <textarea id="input-region" class="form-control-field"
                                          placeholder="Enter the region of base..."
                                          bind:value={item.address} required>
                                </textarea>
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
                right
            </div>
        </div>

    </div>
{:else }
    <div class="w-full h-full flex justify-center items-center">
        <Spinner size="lg"/>
    </div>
{/if}
