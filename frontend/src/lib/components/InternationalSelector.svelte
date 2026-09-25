<script>
    import Fa from "svelte-fa";
    import {faGlobe} from "@fortawesome/free-solid-svg-icons";
    import {configState} from "$lib/states/config.svelte.js";
    import {basket} from "$lib/states/basket.svelte.js";
    import {slide} from "svelte/transition";
    import {onMount} from "svelte";
    import {fetchCurrencies} from "$lib/api/checkout.js";

    let openDropDown = $state(false);
    let dropDownEl = $state(null);
    let currency = $state(configState.state.currency);
    let language = $state(configState.state.language);

    const languages = [
        {code: 'en', label: 'English'},
        {code: 'es', label: 'Spanish'},
        {code: 'fr', label: 'French'},
        {code: 'de', label: 'German'},
    ];

    let currencies = $state([]);

    const loadCurrencies = async () => {
        currencies = await fetchCurrencies()
    }

    function toggleModal() {
        openDropDown = !openDropDown;
    }

    const updateBasket = (currency) => {
        basket.updatePrices(currency)
    }

    const handleClickOutside = (event) => {
        if (openDropDown && dropDownEl && !dropDownEl.contains(event.target)) {
            openDropDown = false;
        }
    }

    const handleApply = () => {
        configState.set('language', language)
        configState.set('currency', currency.toUpperCase())
        updateBasket(configState.state.currency)
    }

    onMount(() => {
        loadCurrencies()
    })


</script>


<svelte:document onclick={handleClickOutside}/>

<div class="relative inline-block" bind:this={dropDownEl}>
    <button
            class="btn"
            aria-haspopup="listbox"
            aria-expanded={openDropDown}
            aria-label="Select language and currency"
            onclick={toggleModal}
    >
        <Fa icon={faGlobe} size="lg"/>
        <span class="font-medium">
      {configState.get("language").toUpperCase()} - {configState.get("currency").toUpperCase()}
    </span>
    </button>

    {#if openDropDown}
        <div
                class="absolute right-0 mt-2 w-72 bg-white rounded-md border border-gray-300 shadow-lg p-4 z-20 divide-gray-300 divide-y space-y-2"
                transition:slide
                role="listbox"
                aria-label="Language and Currency selector"
        >
            <div>
                <h4 class="text-lg font-semibold font-heading mb-2">Set language and currency</h4>
                <p class="text-xs mb-2 font-medium">
                    Select your preferred language and currency<br/>
                    currency will affect your payment and product prices
                </p>
            </div>
            <div class="space-y-2 flex flex-col">
                <div class="mb-4">
                    <label for="language-selector" class="block text-sm font-semibold">
                        Language
                    </label>
                    <select
                            id="language-selector"
                            class="form-control-field w-full"
                            bind:value="{language}"
                    >
                        {#each languages as lang}
                            <option value={lang.code}>
                                {lang.label}
                            </option>
                        {/each}
                    </select>
                </div>
                <div>
                    <label for="currency-selector" class="block text-sm font-semibold">
                        Currency
                    </label>
                    <select
                            id="currency-selector"
                            class="form-control-field w-full"
                            bind:value="{currency}"
                    >
                        {#each currencies as curr}
                            <option value={curr.code} >
                                {curr.symbol} - {curr.name}
                            </option>
                        {/each}
                    </select>
                </div>

                <button class="btn btn-primary" onclick={handleApply}>Apply</button>
            </div>

        </div>
    {/if}
</div>

