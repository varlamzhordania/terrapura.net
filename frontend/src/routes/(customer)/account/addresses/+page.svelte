<script>
    import {createAddress, deleteAddress, fetchAddresses, updateAddress} from "$lib/api/account.js";
    import {onMount} from "svelte";
    import Toast from "$lib/toast.js";
    import {
        faAddressBook,
        faAddressCard,
        faFloppyDisk, faPencil,
        faPlus, faTrash,
        faUser,
        faXmark
    } from "@fortawesome/free-solid-svg-icons";
    import Fa from "svelte-fa";
    import Spinner from "$lib/components/Spinner.svelte";

    let pageSetting = $state({
        page_size: 15,
        page: 1,
    });

    let addresses = $state([]);
    let loading = $state(true);
    let showForm = $state(false);
    let isEditing = $state(false);
    let editingId = $state(null);

    let addressForm = $state({
        full_name: "",
        phone_number: "",
        line1: "",
        line2: "",
        city: "",
        state: "",
        postal_code: "",
        country: "",
        is_default: false
    });

    const loadAddresses = async () => {
        loading = true;
        try {
            const res = await fetchAddresses(pageSetting);
            addresses = res.results || [];
        } catch (err) {
            Toast.error("Failed to load addresses.");
        } finally {
            loading = false;
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault()

        try {
            if (isEditing && editingId) {
                await updateAddress(editingId, addressForm);
                Toast.success("Address updated successfully.");
            } else {
                await createAddress(addressForm);
                Toast.success("Address added successfully.");
            }
            showForm = false;
            isEditing = false;
            editingId = null;
            addressForm = {
                full_name: "",
                phone_number: "",
                line1: "",
                line2: "",
                city: "",
                state: "",
                postal_code: "",
                country: "",
                is_default: false
            };
            await loadAddresses();
        } catch (err) {
            Toast.error("Failed to save address. Please check your input.");
        }
    };

    const handleEdit = (address) => {
        addressForm = {...address};
        editingId = address.id;
        isEditing = true;
        showForm = true;
    };

    const handleDelete = async (id) => {
        if (!confirm("Are you sure you want to delete this address?")) return;
        try {
            const res = await deleteAddress(id);
            if (res?.detail) {
                Toast.success(res.detail);
            } else {
                Toast.success("Address deleted successfully.");
            }
            await loadAddresses();
        } catch (err) {
            Toast.error("Failed to delete address.");
        }
    };

    onMount(() => {
        loadAddresses();
    });
</script>


{#snippet addressItem(data)}
    <div class="card bg-gray-100 hover:bg-gray-200 w-full space-y-2 flex flex-wrap justify-between items-start">
        <div class="space-y-1">
            <p class="font-medium">{data.full_name} {data.is_default ? "(Default)" : ""}</p>
            <p class="text-sm">{data.phone_number}</p>
            <p class="text-sm">{data.line1}</p>
            {#if data.line2}
                <p class="text-sm">{data.line2}</p>
            {/if}
            <p class="text-sm">{data.city}, {data.state}</p>
            <p class="text-sm">{data.country} - {data.postal_code}</p>
        </div>
        <div class="flex space-x-2 mt-3 md:mt-0">
            <button
                    class="btn btn-info"
                    onclick={() => handleEdit(data)}
            >
                <Fa icon={faPencil}/>
                Edit
            </button>
            <button
                    class="btn btn-danger"
                    onclick={() => handleDelete(data.id)}
            >
                <Fa icon={faTrash}/>
                Delete
            </button>
        </div>
    </div>

{/snippet}


<div class="container space-y-2">
    <div class="card bg-gray-100 text-slate-900 shadow-none flex flex-wrap justify-between items-center gap-2">
        <div class="flex justify-start items-center gap-2">
            <Fa icon={faAddressBook} size="lg"/>
            <h2 class="text-2xl font-heading font-bold">My addresses</h2>
        </div>

        <button class="btn"
                class:btn-primary={!showForm}
                onclick={() => {showForm= !showForm}}
        >
            {#if showForm}
                <Fa icon={faXmark} size="lg"/>
                Close
            {:else if isEditing}
                <Fa icon={faAddressCard} size="lg"/>
                Edit Address
            {:else}
                <Fa icon={faPlus} size="lg"/>
                Add New Address
            {/if}
        </button>
    </div>


    {#if showForm}
        <div class="card bg-gray-100">
            <h3 class="text-lg font-semibold">
                {#if isEditing}
                    Edit Address
                {:else}
                    Add New Address
                {/if}
            </h3>
            <form class="space-y-2" onsubmit={handleSubmit}>
                <div class="flex flex-col md:flex-row gap-2">
                    <div class="w-full">
                        <label for="full_name-input" class="form-control-label">Full Name</label>
                        <input type="text"
                               id="full_name-input"
                               name="full_name"
                               placeholder="John Doe"
                               bind:value={addressForm.full_name}
                               class="form-control-field"
                               required
                        />
                    </div>

                    <div class="w-full">
                        <label for="phone_number-input" class="form-control-label">Phone Number</label>
                        <input type="text"
                               id="phone_number-input"
                               name="phone_number"
                               placeholder="+1 555 123 4567"
                               bind:value={addressForm.phone_number}
                               class="form-control-field"
                               required
                        />
                    </div>
                </div>

                <div>
                    <label for="line1-input" class="form-control-label">Address Line 1</label>
                    <input type="text"
                           id="line1-input"
                           name="line1"
                           placeholder="123 Main St"
                           bind:value={addressForm.line1}
                           class="form-control-field md:col-span-2"
                           required
                    />
                </div>

                <div>
                    <label for="line2-input" class="form-control-label">Address Line 2</label>
                    <input type="text"
                           id="line2-input"
                           name="line2"
                           placeholder="Apartment, suite, etc. (optional)"
                           bind:value={addressForm.line2}
                           class="form-control-field md:col-span-2"
                    />
                </div>

                <div class="flex flex-col md:flex-row gap-2">
                    <div class="w-full">
                        <label for="city-input" class="form-control-label">City</label>
                        <input type="text"
                               id="city-input"
                               name="city"
                               placeholder="New York"
                               bind:value={addressForm.city}
                               class="form-control-field"
                               required
                        />
                    </div>

                    <div class="w-full">
                        <label for="state-input" class="form-control-label">State</label>
                        <input type="text"
                               id="state-input"
                               name="state"
                               placeholder="NY"
                               bind:value={addressForm.state}
                               class="form-control-field"
                               required
                        />
                    </div>
                </div>

                <div class="flex flex-col md:flex-row gap-2">
                    <div class="w-full">
                        <label for="postal_code-input" class="form-control-label">Postal Code</label>
                        <input type="text"
                               id="postal_code-input"
                               name="postal_code"
                               placeholder="10001"
                               bind:value={addressForm.postal_code}
                               class="form-control-field"
                               required
                        />
                    </div>

                    <div class="w-full">
                        <label for="country-input" class="form-control-label">Country</label>
                        <input type="text"
                               id="country-input"
                               name="country"
                               placeholder="USA"
                               bind:value={addressForm.country}
                               class="form-control-field"
                               required
                        />
                    </div>
                </div>

                <div class="flex items-center space-x-2 md:col-span-2 ">
                    <input type="checkbox" id="is_default-checkbox" bind:checked={addressForm.is_default}
                           class="form-control-checkbox"/>
                    <label class="form-control-label" for="is_default-checkbox">
                        Set as Default
                    </label>
                </div>

                <div class="flex justify-end space-x-2">
                    <button type="button" class="btn btn-danger btn-outline"
                            onclick={() => {showForm=false; isEditing=false; editingId=null;}}>
                        Cancel
                    </button>

                    <button type="submit" class="btn btn-primary">
                        {#if loading.account}
                            <Spinner size="xs"/>
                            Saving...
                        {:else }
                            <Fa icon={faFloppyDisk} size="lg"/>
                            Save
                        {/if}
                    </button>
                </div>
            </form>
        </div>
    {/if}

    {#if loading}
        <p class="text-gray-500">Loading addresses...</p>
    {:else if addresses.length === 0}
        <p class="">No addresses found. Add a new one.</p>
    {:else}
        <div class="grid gap-4">
            {#each addresses as address}
                {@render addressItem(address)}
            {/each}
        </div>
    {/if}
</div>
