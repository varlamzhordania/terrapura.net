<script>
    import Spinner from "$lib/components/Spinner.svelte";

    let {
        label = "Select Item",
        placeholder = "Search...",
        id = "input-autocomplete",
        fetcher,
        minChars = 0,
        required,
        disabled,
        getLabel = (item) => item?.name ?? "",
        getValue = (item) => item?.id ?? item,
        value = $bindable(null),   // 👈 makes `bind:value` work
    } = $props();

    let search = $state("");
    let results = $state([]);
    let showList = $state(false);
    let loading = $state(false);
    let activeIndex = $state(-1);
    let debounceTimer;
    let container = $state(null)

    function handleInput(e) {
        search = e.target.value;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(searchItems, 250);
    }

    async function searchItems() {
        if (search.length < minChars) {
            results = [];
            showList = false;
            return;
        }
        loading = true;
        results = await fetcher(search);
        loading = false;
        showList = true;
        activeIndex = -1;
    }

    function selectItem(item) {
        value = getValue(item); // 👈 updates parent via bind:value
        search = getLabel(item);
        showList = false;
    }

    function handleKeydown(e) {
        if (!showList) return;

        if (e.key === "ArrowDown") {
            activeIndex = (activeIndex + 1) % results.length;
            e.preventDefault();
        } else if (e.key === "ArrowUp") {
            activeIndex = (activeIndex - 1 + results.length) % results.length;
            e.preventDefault();
        } else if (e.key === "Enter" && activeIndex >= 0) {
            selectItem(results[activeIndex]);
            e.preventDefault();
        } else if (e.key === "Escape") {
            showList = false;
        }
    }

    function handleClickOutside(event) {
        if (!container.contains(event.target)) {
            showList = false;
        }
    }

    $effect(() => {
        if (value) {
            search = getLabel(value);
        }
    });

</script>

<svelte:document on:mousedown={handleClickOutside}/>

{#snippet listItem(data, index)}
    <li class="px-2 py-1 hover:bg-gray-200" class:bg-gray-100={index === activeIndex}>
        <button class="w-full text-start cursor-pointer" onclick={() => selectItem(data)}>
            {getLabel(data)}
        </button>
    </li>
{/snippet}

<div class="relative" bind:this={container}>
    <label class="form-control-label" for={id}>
        {label}
    </label>
    <input
            type="text"
            id={id}
            bind:value={search}
            oninput={handleInput}
            onkeydown={handleKeydown}
            onfocus={() => showList = true}
            class="form-control-field"
            placeholder={placeholder}
            autocomplete="off"
            role="combobox"
            aria-expanded={showList}
            aria-controls={id + "-listbox"}
            {required}
            {disabled}
    />

    {#if showList}
        <ul
                id={id + "-listbox"}
                role="listbox"
                class="absolute z-10 bg-white border border-gray-300 rounded-md max-h-60 overflow-y-auto w-full shadow flex flex-col"
                style="top: calc(100% + 5px);"
        >
            {#if loading}
                <li class="px-2 py-2 flex justify-center items-center">
                    <Spinner/>
                </li>
            {:else if results.length > 0}
                {#each results as item, i}
                    {@render listItem(item, i)}
                {/each}
            {:else}
                <li class="px-2 py-1 text-gray-500">No item found.</li>
            {/if}
        </ul>
    {/if}
</div>
