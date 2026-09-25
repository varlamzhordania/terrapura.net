<script>
    import {basket} from "$lib/states/basket.svelte.js";
    import {formatCurrency} from "$lib/utils.svelte.js";
    import {configState} from "$lib/states/config.svelte.js";
    import {fetchAddresses} from "$lib/api/account.js";
    import {onMount} from "svelte";
    import {fetchPaymentMethods, postOrder, stripeOrderPayment} from "$lib/api/checkout.js";
    import Toast from "$lib/toast.js";
    import {faQuestionCircle} from "@fortawesome/free-solid-svg-icons";
    import {Tooltip} from "flowbite-svelte";
    import Fa from "svelte-fa";
    import Spinner from "$lib/components/Spinner.svelte";
    import {faStripe} from "@fortawesome/free-brands-svg-icons";

    let addresses = $state([]);
    let paymentMethods = $state([])
    let selectedPayment = $state(null)
    let selectedAddress = $state(null);
    let loading = $state(false)
    let addressForm = $state({})
    let acceptTerm = $state(false)
    let isDisabled = $derived(!acceptTerm || basket.items.length === 0)


    const loadAddresses = async () => {
        addresses = await fetchAddresses({pagination: false});
        if (addresses.length > 0) {
            selectedAddress = addresses.find(a => a.is_default)?.id || addresses[0].id;
        }
    };

    const loadPaymentMethods = async () => {
        paymentMethods = await fetchPaymentMethods(configState.state.currency)
        if (paymentMethods.length > 0) {
            selectedPayment = paymentMethods[0]
        }
    }

    const handleStripePayment = async (orderId) => {
        try {
            const paymentResponse = await stripeOrderPayment({order_id: orderId});

            if (!paymentResponse?.checkout_url) {
                Toast.error("Unable to get Stripe checkout URL. Please try again.");
                return false;
            }

            window.location.href = paymentResponse.checkout_url;
            return true;
        } catch (err) {
            console.error("Stripe payment error:", err);
            Toast.error("Something went wrong while starting payment. Please try again.");
            return false;
        }
    };

    const paymentHandlers = {
        stripe: handleStripePayment,
        // future: paypal: handlePayPalPayment, etc.
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!selectedAddress && !addressForm) {
            Toast.error("Please select or enter a shipping address.");
            return;
        }

        if (!selectedPayment || !paymentHandlers[selectedPayment.code]) {
            Toast.error("Please select a valid payment method.");
            return;
        }

        // Validate against minimum amount
        const cartTotal = Number(basket.total);
        const minAmount = Number(selectedPayment.converted_min_amount);

        if (cartTotal < minAmount) {
            Toast.error(
                `This payment method requires a minimum of ${minAmount} ${selectedPayment.converted_currency}.`
            );
            return;
        }

        loading = true;
        try {
            const orderResponse = await postOrder({
                address_id: selectedAddress,
                address: addressForm,
                currency_code: configState.get("currency"),
            });

            if (!orderResponse?.order_id) {
                Toast.error("Order creation failed. Please try again.");
                return;
            }

            Toast.success("Order created! Redirecting to payment...");
            await paymentHandlers[selectedPayment.code](orderResponse.order_id);

        } catch (err) {
            console.error("Order submission error:", err);
            Toast.error("Something went wrong while creating the order. Please try again.");
        } finally {
            loading = false;
        }
    };

    onMount(() => {
        loadAddresses()

    })

    $effect(() => {
        loadPaymentMethods()
    })


</script>

<svelte:head>
    <title>Terrapura | checkout</title>
</svelte:head>

{#snippet addressItem(data)}
    <button class="flex flex-col w-full rounded-md p-4 transition border-2 border-primary-700 {selectedAddress === data.id ? 'bg-primary-50/30' : 'bg-white'} hover:border-primary-800 focus-within:border-primary-800 focus-within:bg-primary-50/30 cursor-pointer"
            type="button"
            onclick={()=> selectedAddress=data.id}
    >
        <div class="flex flex-col text-start">
            <span class="font-semibold text-lg">{data.full_name}</span>
            <span>{data.line1}</span>
            {#if data.line2}
                <span>{data.line2}</span>
            {/if}
            <span>{data.city}, {data.state ? `${data.state}, ` : ''}{data.postal_code}</span>
            <span>{data.country}</span>
        </div>
    </button>
{/snippet}

{#snippet paymentItem(data)}
    <button class="flex flex-col text-center items-center justify-center size-44 rounded-md p-4 transition border-2 border-secondary-400 {selectedPayment.code === data.code ? 'bg-secondary-50' : 'bg-white'} hover:border-secondary-600 focus-within:border-secondary-600 focus-within:bg-secondary-50 cursor-pointer"
            type="button"
            onclick={()=> selectedPayment=data}
    >
        {#if data.icon}
            <img src={data.icon} alt={data.name} class="size-28 z-10"/>
        {:else}
            <h4 class="text-2xl font-semibold">
                {data.name}
            </h4>
        {/if}

    </button>
{/snippet}

<form onsubmit={handleSubmit}>
    <div class="grid grid-cols-1 lg:grid-cols-10 xl:grid-cols-12 gap-8 lg:gap-16">
        <section class="col-span-1 lg:col-span-7 xl:col-span-9 space-y-5">
            <div>
                <h2 class="text-2xl font-bold font-heading">Shipping Address</h2>
                {#if addresses.length > 0}
                    <div class="flex flex-col flex-wrap justify-start items-start mt-4 space-y-2 w-full">
                        {#each addresses as address}
                            {@render addressItem(address)}
                        {/each}
                    </div>
                {:else}
                    <div class="space-y-4">
                        <h3 class="font-medium font-heading">Add a Shipping Address</h3>
                        <div class="space-y-3">
                            <!-- Full Name & Phone -->
                            <div class="flex gap-2">
                                <div class="w-full">
                                    <label for="addr-full-name" class="form-control-label">
                                        Full Name
                                    </label>
                                    <input
                                            type="text"
                                            id="addr-full-name"
                                            bind:value={addressForm.full_name}
                                            placeholder="John Doe"
                                            class="form-control-field"
                                            required
                                    />
                                </div>
                                <div class="w-full">
                                    <label for="addr-phone-number" class="form-control-label">
                                        Phone Number
                                    </label>
                                    <input
                                            type="tel"
                                            id="addr-phone-number"
                                            bind:value={addressForm.phone_number}
                                            placeholder="+1 555 123 4567"
                                            class="form-control-field"
                                            pattern="^\+?[0-9\s\-()]{7,20}$"
                                            title="Enter a valid phone number, e.g. +1 555 123 4567"
                                            required
                                    />
                                </div>
                            </div>

                            <!-- Address Lines -->
                            <div>
                                <label for="addr-line1" class="form-control-label">Address Line 1</label>
                                <input
                                        type="text"
                                        id="addr-line1"
                                        bind:value={addressForm.line1}
                                        placeholder="123 Main St, Apt 4B"
                                        class="form-control-field"
                                        required
                                />
                            </div>
                            <div>
                                <label for="addr-line2" class="form-control-label">Address Line 2</label>
                                <input
                                        type="text"
                                        id="addr-line2"
                                        bind:value={addressForm.line2}
                                        placeholder="Suite, building, floor, etc. (optional)"
                                        class="form-control-field"
                                />
                            </div>

                            <!-- City & State -->
                            <div class="flex gap-2">
                                <div class="w-full">
                                    <label for="addr-city" class="form-control-label">City</label>
                                    <input
                                            type="text"
                                            id="addr-city"
                                            bind:value={addressForm.city}
                                            placeholder="New York"
                                            class="form-control-field"
                                            required
                                    />
                                </div>
                                <div class="w-full">
                                    <label for="addr-state" class="form-control-label">State / Province / Region</label>
                                    <input
                                            type="text"
                                            id="addr-state"
                                            bind:value={addressForm.state}
                                            placeholder="New York"
                                            class="form-control-field"
                                            required
                                    />
                                </div>
                            </div>

                            <!-- Postal Code & Country -->
                            <div class="flex gap-2">
                                <div class="w-full">
                                    <label for="addr-postal" class="form-control-label">Postal / Zip Code</label>
                                    <input
                                            type="text"
                                            id="addr-postal"
                                            bind:value={addressForm.postal_code}
                                            placeholder="10001"
                                            class="form-control-field"
                                            required
                                    />
                                </div>
                                <div class="w-full">
                                    <label for="addr-country" class="form-control-label">Country</label>
                                    <input
                                            type="text"
                                            id="addr-country"
                                            bind:value={addressForm.country}
                                            placeholder="United States"
                                            class="form-control-field"
                                            required
                                    />
                                </div>
                            </div>

                            <label class="flex items-center space-x-2">
                                <input type="checkbox" id="default-address" bind:checked={addressForm.is_default}
                                       class="form-control-checkbox"/>
                                <label class="form-control-label" for="default-address">
                                    Set as default address
                                </label>
                            </label>
                        </div>
                    </div>
                {/if}
            </div>
            <div>
                <h2 class="text-2xl font-bold font-heading">Payment Method</h2>
                {#if paymentMethods.length > 0 }
                    <div class="flex flex-wrap justify-start items-start mt-4">
                        {#each paymentMethods as item}
                            {@render paymentItem(item)}
                        {/each}
                    </div>
                {:else}
                    <div>
                        <p class="font-medium">No payment method available right now.</p>
                    </div>
                {/if}
            </div>
        </section>
        <aside class="card bg-gray-100 h-fit col-span-1 lg:col-span-3 xl:col-span-3 space-y-2">
            <h2 class="text-xl font-bold text-slate-700">Order Summary</h2>

            {#if basket.items.length === 0}
                <p class="text-slate-500 font-heading">Your basket is empty.</p>
            {:else}
                <ul class="space-y-2 text-sm text-slate-700">
                    <li class="flex justify-between border-b border-b-gray-300 pb-2">
                        <div class="flex gap-1 justify-center items-center">
                        <span>
                            Subtotal
                        </span>
                            <div>
                                <Fa icon={faQuestionCircle}/>
                            </div>
                            <Tooltip class="w-64 text-sm font-light " title="About the Subtotal">
                                <p>
                                    The subtotal shown is rounded to two decimal places for easier reading.
                                    However, when processing payments, we use the exact amount with higher precision,
                                    which may cause minor differences in the final charged amount.
                                </p>
                                <p class="mt-2 text-xs text-gray-400 dark:text-gray-500">
                                    This helps ensure accurate currency conversion and precise billing.
                                </p>
                            </Tooltip>
                        </div>
                        <span>{formatCurrency(basket.subtotal, configState.state.currency)}</span>
                    </li>
                    <li class="flex justify-between border-b border-b-gray-300 pb-2">
                        <span>Tax ({basket.tax * 100}%)</span>
                        <span>{formatCurrency(basket.taxAmount, configState.state.currency)}</span>
                    </li>
                    <li class="flex justify-between text-lg font-bold pt-2">
                        <span>Total</span>
                        <span>{formatCurrency(basket.total, configState.state.currency)}</span>
                    </li>
                </ul>
                <label class="flex items-center space-x-2">
                    <input type="checkbox" id="acceptTerm" bind:checked={acceptTerm} class="form-control-checkbox"/>
                    <label class="form-control-label" for="acceptTerm">
                        Accept <a href="/terms-of-sale" class="link" target="_blank">terms of sale</a>
                    </label>
                </label>
                <button
                        class="btn btn-primary w-full mt-2"
                        aria-disabled={isDisabled}
                        disabled={isDisabled}
                        type="submit"
                >
                    {#if loading}
                        <Spinner/>
                    {:else }
                        Pay Now
                    {/if}

                </button>
            {/if}
        </aside>
    </div>
</form>
