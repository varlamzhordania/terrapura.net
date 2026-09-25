<script>
    import {basket} from "$lib/states/basket.svelte.js";
    import Fa from "svelte-fa";
    import {faMinus, faPlus, faQuestionCircle, faTrashCan} from "@fortawesome/free-solid-svg-icons";
    import {formatCurrency, inputSteps} from "$lib/utils.svelte.js";
    import {configState} from "$lib/states/config.svelte.js";
    import {Tooltip} from "flowbite-svelte";


</script>

<svelte:head>
    <title>Terrapura | shopping cart</title>
</svelte:head>

{#snippet cartItem(data)}
    <div class="w-full flex justify-start items-start gap-2 border-b border-b-gray-300 py-2 ">
        <div class="aspect-square">
            <a href="/herbs/{data.herb.slug}">
                <img src={data.herb.media.file} alt={data.herb.name}
                     class="h-[150px] w-[150px] object-cover object-center rounded-md"/>
            </a>
        </div>
        <div class="flex flex-col gap-2 grow">
            <h2 class="text-2xl font-bold text-slate-800">
                {data.herb.name}
            </h2>
            <p class="italic text-slate-600 font-medium">
                also known as: {data.herb.latin_name}
            </p>

            <p class="text-gray-600 mb-4">
                Price:
                <strong>
                    {formatCurrency(data.price.converted_price || data.price.price, data.price.converted_currency || data.price.currency.code)}
                    {data.price.converted_currency}
                    per {data.price.unit}
                </strong><br/>
                Total Price:
                <strong>
                    {formatCurrency((data.price.converted_price || data.price.price) * data.quantity, data.price.converted_currency || data.price.currency.code)}
                </strong>
            </p>
        </div>
        <div class="flex flex-col space-y-2 items-center">
            <div class="border rounded-md border-gray-300 flex justify-between items-center">
                <button class="btn" onclick="{() => basket.increment(data,inputSteps(data.price.unit)[0])}">
                    <Fa icon={faPlus} size="lg"/>
                </button>
                <div class="flex justify-between items-center">
                    <input type="number" step={inputSteps(data.price.unit)[0]} min={inputSteps(data.price.unit)[1]}
                           id="data-price-{data.price.id}" name="input-data-price-{data.price.id}"
                           class="w-fit border-0 text-center bg-transparent focus:ring-0 p-0 form-control-number-no-button"
                           class:max-w-10={inputSteps(data.price.unit)[0] === 1}
                           class:max-w-14={inputSteps(data.price.unit)[0] === 0.01}
                           bind:value={data.quantity}
                           onchange={() => basket.save()}
                    />
                    <small class="text-xs">{data.price.unit}</small>
                </div>
                <button class="btn" onclick="{() => basket.decrement(data,inputSteps(data.price.unit)[0])}">
                    <Fa icon={faMinus} size="lg"/>
                </button>
            </div>
            <button class="btn btn-danger w-fit" onclick={()=> basket.remove(data.price.id,data.herb.id)}>
                <Fa icon={faTrashCan} size="lg"/>
            </button>
        </div>
    </div>
{/snippet}


<div class="grid grid-cols-1 lg:grid-cols-10 xl:grid-cols-12 gap-8 lg:gap-16">
    <section class="col-span-1 lg:col-span-7 xl:col-span-9">
        <h2 class="text-2xl font-bold font-heading mb-4">Shopping cart items</h2>
        <div class="flex flex-col space-y-2 justify-start items-start">
            {#if basket.items.length === 0}
                <p class="text-gray-500">Your basket is empty.</p>
            {:else}
                {#each basket.items as item}
                    {@render cartItem(item)}
                {/each}
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
                <li class="flex justify-between text-lg font-bold pt-2">
                    <span>Total</span>
                    <span>{formatCurrency(basket.subtotal, configState.state.currency)}</span>
                </li>
            </ul>
            <a
                    class="btn btn-primary w-full mt-2 disabled:opacity-50 disabled:cursor-not-allowed"
                    href="/checkout"
                    aria-disabled={basket.items.length === 0}
                    disabled={basket.items.length === 0}
            >
                Proceed to Checkout
            </a>
        {/if}
    </aside>
</div>