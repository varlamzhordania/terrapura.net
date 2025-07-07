<script>
    import {onMount} from 'svelte';
    import {slide} from "svelte/transition";
    import {
        fetchHerbs,
        fetchCategories,
        fetchTags,
        fetchSymptom,
    } from '$lib/api/herbs.js';
    import HerbCard from "$lib/components/HerbCard.svelte";
    import {pushState} from "$app/navigation";
    import Fa from "svelte-fa";
    import {faChevronDown, faChevronRight} from "@fortawesome/free-solid-svg-icons";

    let showCategories = $state(true)
    let showTags = $state(true)
    let showSymptoms = $state(true)


    let herbs = $state([]);
    let categories = $state([]);
    let tags = $state([]);
    let symptoms = $state([]);

    let selectedCategory = $state([]);
    let selectedTags = $state([]);
    let selectedSymptoms = $state([])

    let page = $state(1);
    let loading = $state(true);
    let error = $state(null);

    const pageSize = 25; // backend page size

    async function loadHerbs(push = true) {
        try {
            loading = true;
            error = null;

            const params = new URLSearchParams();

            params.append("page", page)


            if (selectedCategory.length > 0) {
                params.set("category", selectedCategory.join(","));
            }

            if (selectedTags.length > 0) {
                params.set("tags", selectedTags.join(","));
            }

            if (selectedSymptoms.length > 0) {
                params.set("symptoms", selectedSymptoms.join(","));
            }

            // Push new state to URL
            if (push) {
                const query = params.toString();
                const newUrl = `${window.location.pathname}${query ? `?${query}` : ""}`;
                pushState(newUrl, {});
            }

            herbs = await fetchHerbs(Object.fromEntries(params));
        } catch (err) {
            error = err.message;
        } finally {
            loading = false;
        }
    }

    onMount(async () => {
        try {
            const urlParams = new URLSearchParams(window.location.search);

            const cat = urlParams.get("category");
            if (cat) selectedCategory = cat.split(",");

            const tag = urlParams.get("tags");
            if (tag) selectedTags = tag.split(",");

            const sym = urlParams.get("symptoms");
            if (sym) selectedSymptoms = sym.split(",");

            const pge = urlParams.get("page");
            if (pge) page = Number(pge);


            [categories, tags, symptoms] = await Promise.all([
                fetchCategories(),
                fetchTags(),
                fetchSymptom(),
            ]);
            await loadHerbs();
        } catch (err) {
            error = err.message;
        }
    });

    function goToPage(p) {
        page = p;
        loadHerbs();
        scrollTo({top: 0, behavior: "smooth"});

    }

</script>

{#snippet Category(data)}
    <li class="flex justify-start items-center">
        <input type="checkbox" id="category-{data.slug}" name="category" class="form-control-checkbox"
               value={data.slug}
               bind:group={selectedCategory}
               onchange={()=> loadHerbs()}
        >
        <label for="category-{data.slug}" class="form-control-label text-sm text-slate-500 truncate">
            {data.name}
        </label>
    </li>
{/snippet}

{#snippet Tag(data)}
    <li class="flex justify-start items-center">
        <input type="checkbox" id="tag-{data.slug}" name="tag" class="form-control-checkbox"
               value={data.slug}
               bind:group={selectedTags}
               onchange={()=> loadHerbs()}
        >
        <label for="tag-{data.slug}" class="form-control-label text-sm text-slate-500">
            {data.name}
        </label>
    </li>
{/snippet}

{#snippet Symptom(data)}
    <li class="flex justify-start items-center">
        <input type="checkbox" id="symptom-{data.slug}" name="symptom" class="form-control-checkbox"
               value={data.slug}
               bind:group={selectedSymptoms}
               onchange={()=> loadHerbs()}
        >
        <label for="symptom-{data.slug}" class="form-control-label text-sm text-slate-500">
            {data.name}
        </label>
    </li>
{/snippet}

<div class="grid grid-cols-1 lg:grid-cols-10 xl:grid-cols-12 gap-8 lg:gap-16">
    <aside class="col-span-1 lg:col-span-3 xl:col-span-2">
        <div class="flex flex-col gap-4 p-2">

            <!-- Categories -->
            <div>
                <button class="btn justify-between items-center cursor-pointer px-0 w-full"
                        onclick={() => showCategories = !showCategories}>
                    <span class="capitalize">
                        Categories <small>({categories.length})</small>
                    </span>
                    <Fa icon={showCategories ? faChevronDown : faChevronRight}/>
                </button>
                {#if showCategories}
                    <ul class="space-y-1 max-h-[100px] lg:max-h-[200px] overflow-y-auto" transition:slide>
                        {#each categories as category}
                            {@render Category(category)}
                        {/each}
                    </ul>
                {/if}
            </div>

            <!-- Tags -->
            <div>
                <button class="btn justify-between items-center cursor-pointer px-0 w-full"
                        onclick={() => showTags = !showTags}>
                    <span class="capitalize">
                        Tags <small>({tags.length})</small>
                    </span>
                    <Fa icon={showTags ? faChevronDown : faChevronRight}/>
                </button>
                {#if showTags}
                    <ul class="space-y-1 max-h-[100px] lg:max-h-[200px] overflow-y-auto" transition:slide>
                        {#each tags as tag}
                            {@render Tag(tag)}
                        {/each}
                    </ul>
                {/if}
            </div>

            <!-- Symptoms -->
            <div>
                <button class="btn justify-between items-center cursor-pointer px-0 w-full"
                        onclick={() => showSymptoms = !showSymptoms}>
                    <span class="capitalize">
                        Symptoms <small>({symptoms.length})</small>
                    </span>
                    <Fa icon={showSymptoms ? faChevronDown : faChevronRight}/>
                </button>
                {#if showSymptoms}
                    <ul class="space-y-1 max-h-[100px] lg:max-h-[200px] overflow-y-auto" transition:slide>
                        {#each symptoms as symptom}
                            {@render Symptom(symptom)}
                        {/each}
                    </ul>
                {/if}
            </div>

        </div>
    </aside>

    <!-- Herb List -->
    <section class="col-span-1 lg:col-span-7 xl:col-span-10 p-2">
        <div class="mb-10">
            {#if loading}
                <p>Loading herbs...</p>
            {:else if error}
                <p class="text-red-500">Error: {error}</p>
            {:else if herbs.results?.length === 0}
                <p>No herbs found.</p>
            {:else}
                <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                    {#each herbs.results || herbs as herb}
                        <HerbCard data={herb} shadow/>
                    {/each}
                </div>
            {/if}
        </div>

        {@render Pagination()}

    </section>
</div>


{#snippet Pagination()}
    {#if herbs.count > pageSize}
        <nav class="mt-8 flex justify-center">
            <ul class="inline-flex items-center space-x-1">
                {#each Array(Math.ceil(herbs.count / pageSize)) as _, i}
                    {#if i + 1 === page}
                        <li>
                            <button class="btn btn-primary text-lg">{i + 1}</button>
                        </li>
                    {:else}
                        <li>
                            <button class="btn btn-secondary text-lg"
                                    onclick={() => goToPage(i + 1)}>
                                {i + 1}
                            </button>
                        </li>
                    {/if}
                {/each}
            </ul>
        </nav>
    {/if}
{/snippet}