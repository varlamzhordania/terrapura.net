<script>

    import {fetchBases} from "$lib/api/seller.js";
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
            label: "Name",
            key: "name",
        },
        {
            label: "Country",
            key: "country",
        },
        {
            label: "Region",
            key: "region",
        },
        {
            label: "Address",
            key: "address",
            truncate: true,
            width: 220,
        },
        {
            label: "Contact Person",
            key: "contact_person",
        },

    ]

    const loadItems = async (id) => {
        pageSetting.loading = true;
        const res = await fetchBases({
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
           handleSearch={handleChangeSearch}/>