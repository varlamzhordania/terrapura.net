<script>

    import {fetchProducts} from "$lib/api/seller.js";
    import {partnerState} from "$lib/states/partner.svelte.js";
    import TableList from "$lib/components/TableList.svelte";

    let items = $state([])
    let pageSetting = $state({
        page_size: 25,
        page: 1,
        count: 0,
        search: "",
        loading: false,
    });

    const handleChangeSearch = (e) => {
        pageSetting.search = e.target.value
    }

    const setPage = (page) => {
        pageSetting.page = page
    }


    const COLUMNS = [
        {
            label: "Thumbnail",
            key: "herb.media.file",
            type: "image",
            width: 100,
        },
        {
            label: "Name",
            key: "herb.name",

        },
        {
            label: "Category",
            key: "herb.category",
        },
        {
            label: "Base",
            key: "base.name",
        },
        {
            label: "Quantity",
            key: "quantity",
            align: "center",
            headerAlign: "center",
        },
        {
            label: "Unit",
            key: "unit",
            align: "center",
            headerAlign: "center",
        },
        {
            label: "Available",
            key: "is_available",
            type: "boolean",
            align: "center",
            headerAlign: "center",
        },
        {
            label: "Low Stock Threshold",
            key: "low_stock_threshold",
            align: "center",
            headerAlign: "center",
        },
    ]

    const loadItems = async (id) => {
        pageSetting.loading = true;
        const res = await fetchProducts({
            partner_id: id,
            page: pageSetting.page,
            page_size: pageSetting.page_size,
            search: pageSetting.search
        })
        if (res.results) {
            items = res.results
            pageSetting.count = res.count
        }
        pageSetting.loading = false;
    }

    $effect(() => {
        loadItems(partnerState.partner.id)
    })


</script>


<TableList title="Inventory Products"
           columns={COLUMNS}
           items={items}
           pageSetting={pageSetting}
           handlePage={setPage}
           handleSearch={handleChangeSearch}
/>