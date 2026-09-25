<script>
    import {page} from "$app/state";
    import Fa from "svelte-fa";
    import {faAngleLeft, faAngleRight, faCheckSquare, faPlus, faSearch} from "@fortawesome/free-solid-svg-icons";
    import Spinner from "$lib/components/Spinner.svelte";
    import {notFoundImage} from "$lib";

    let {
        children,
        title,
        columns = [],
        items = [],
        addNew = true,
        addLink,
        pageSetting,
        handlePage,
        handleSearch,
        editLink = "/%pk%/",
        isEditable = true,
        isDeletable = true,
    } = $props()

    let totalPages = $derived(
        Array.from({length: Math.ceil(pageSetting.count / pageSetting.page_size)}, (_, i) => i + 1)
    );

    const getEditLink = (id) => {
        return page.url.pathname + editLink.replace("%pk%", id)
    }

    function prevPage() {
        if (pageSetting.page > 1) {
            handlePage(pageSetting.page - 1);
        }
    }

    function nextPage() {
        if (pageSetting.page < totalPages.length) {
            handlePage(pageSetting.page + 1);
        }
    }

    function getValue(obj, path) {
        if (!obj || !path) return null;
        return path.split(".").reduce((acc, part) => acc && acc[part], obj);
    }

</script>

{#snippet colItem(data, row)}
    <td class:truncate={data?.truncate}
        style:width={data.width ? `${data.width}px`: '120px'}
        title={getValue(row, data.key)}
        align={data.align ? data.align : 'left'}
    >
        {#if data.type === "image"}
            <img src={getValue(row, data.key) || notFoundImage} alt={data.label}
                 class="aspect-square max-w-18 object-cover rounded-md"/>
        {:else if data.type === "boolean"}
            {#if getValue(row, data.key)}
                <Fa icon={faCheckSquare} class="text-primary-700"/>
            {:else}
                <Fa icon={faCheckSquare}/>
            {/if}
        {:else}
            {#if data.truncate && typeof getValue(row, data.key) === "string"}
                {getValue(row, data.key).substring(0, 50) + "..."}
            {:else}
                {getValue(row, data.key)}
            {/if}
        {/if}
    </td>

{/snippet}

<div class="space-y-2">
    <div class="card border border-gray-300 bg-white">
        <!-- Header -->
        <div class="flex justify-between items-center flex-wrap gap-2 mb-4 border-b border-b-gray-300 pb-2">
            <div class="flex justify-start items-center space-x-0.5 bg-gray-100 rounded-sm">
                <input type="text" placeholder="Search..."
                       class="form-control-transparent w-auto"
                       onchange={handleSearch}
                />
                <div class="px-2.5">
                    <Fa icon={faSearch}/>
                </div>
            </div>
            <div>
                {#if addNew}
                    <a href={addLink} class="btn btn-primary rounded-sm">
                        <Fa icon={faPlus}/>
                        Add New
                    </a>
                {/if}
            </div>
        </div>

        <!-- Table -->
        <div class="table-wrapper">
            <table class="table">
                <thead class="table-head">
                <tr class="bg-gray-100 text-left text-sm text-gray-600">
                    {#each columns as col}
                        <th scope="col" class:truncate={col?.truncate}
                            style="{col.width ? `width:${col.width};`: 'width:120px;'}"
                            align={col.headerAlign ? col.headerAlign : 'left'}
                        >
                            {col.label}
                        </th>
                    {/each}
                    <th scope="col" style="width: 120px;">Actions</th>
                </tr>
                </thead>
                <tbody>
                {#if pageSetting.loading}
                    <tr>
                        <td colspan={columns.length + 1}>
                            <div class="w-full flex justify-center items-center">
                                <Spinner/>
                            </div>
                        </td>
                    </tr>
                {:else}
                    {#if items.length > 0}
                        {#each items as row}
                            <tr>
                                {#each columns as col}
                                    {@render colItem(col, row)}
                                {/each}
                                <td>
                                    <div class="flex justify-between items-center flex-wrap">
                                        {#if isEditable}
                                            <a href={getEditLink(row.id)}
                                               class="btn btn-ghost-secondary btn-sm">Edit</a>
                                        {/if}
                                        {#if isDeletable}
                                            <button class="btn btn-ghost-danger btn-sm">Delete</button>
                                        {/if}
                                    </div>
                                </td>
                            </tr>
                        {/each}
                    {:else}
                        <tr>
                            <td colspan={columns.length + 1} class="text-center py-6 text-gray-400">
                                No data found
                            </td>
                        </tr>
                    {/if}
                {/if}
                </tbody>
            </table>
        </div>

        <!-- Pagination -->
        <div class="flex justify-between items-center flex-wrap gap-2 mt-4 text-sm">
            <span class="text-gray-500 text-sm">
                Showing {(pageSetting.page - 1) * pageSetting.page_size + 1}
                – {Math.min(pageSetting.page * pageSetting.page_size, pageSetting.count)}
                of {pageSetting.count}
            </span>
            <div class="flex items-center space-x-2">
                <button class="pagination-btn" onclick={prevPage} disabled={pageSetting.page === 1}>
                    <Fa icon={faAngleLeft}/>
                </button>
                {#each totalPages as page}
                    <button class="pagination-btn" aria-current={pageSetting.page === page ? 'page' : 'none' }
                            disabled={pageSetting.page === page}
                            onclick={() => handlePage(page)}
                    >
                        {page}
                    </button>
                {/each}
                <button class="pagination-btn" onclick={nextPage} disabled={pageSetting.page === totalPages.length}>
                    <Fa icon={faAngleRight}/>
                </button>
            </div>
        </div>
    </div>
</div>
