<script>
    import {onMount} from "svelte";
    import {fetchOrders} from "$lib/api/checkout.js";
    import {formatCurrency} from "$lib/utils.svelte.js";

    let pageSetting = $state({
        page_size: 15,
        page: 1,
    });

    let orders = $state([]);

    const loadOrders = async () => {
        const res = await fetchOrders(pageSetting);
        orders = res.results || []

    };

    const statusColor = (status) => {
        switch (status) {
            case "pending":
                return "badge-warning";
            case "payment":
                return "badge-info";
            case "processing":
                return "badge-secondary";
            case "shipped":
                return "badge-dark";
            case "delivered":
                return "badge-success";
            case "cancelled":
                return "badge-danger";
            default:
                return "badge-neutral";
        }
    };


    onMount(() => {
        loadOrders();
    });
</script>

{#snippet ordersItem(data)}
    <tr>
        <td class="px-4 py-3 text-sm font-medium text-gray-900">#{data.id}</td>


        <td class="px-4 py-3 text-sm text-gray-600 truncate max-w-xs">
            {data.delivery_address.full_name}, {data.delivery_address.city}
        </td>
        <td class="px-4 py-3 text-sm text-gray-600 truncate max-w-xs">
            {Intl.DateTimeFormat(navigator.languages, {
                month: "long",
                day: "2-digit",
                year: "numeric"
            }).format(new Date(data.created_at))}

        </td>
        <td class="px-4 py-3 text-sm text-gray-800">
            {formatCurrency(data.total_price, data.currency.code)} {data.currency.code}
        </td>
        <td class="px-4 py-3">
            <span class={`badge ${statusColor(data.status)}`}>
                {data.status}
            </span>
        </td>
        <td class="px-4 py-3 text-right">
            <a
                    href="/account/orders/{data.id}"
                    class="link link-info "
            >
                Details
            </a>
        </td>
    </tr>
{/snippet}


<div class="py-6">
    <h1 class="text-2xl font-bold mb-6">My Orders</h1>

    {#if orders.length === 0}
        <p class="text-gray-500">No orders found.</p>
    {:else}
        <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 bg-white rounded-lg shadow">
                <thead class="bg-gray-50">
                <tr>
                    <th class="px-4 py-3 text-left text-sm font-semibold text-gray-600">Order ID</th>
                    <th class="px-4 py-3 text-left text-sm font-semibold text-gray-600">Address</th>
                    <th class="px-4 py-3 text-left text-sm font-semibold text-gray-600">Date</th>
                    <th class="px-4 py-3 text-left text-sm font-semibold text-gray-600">Total</th>
                    <th class="px-4 py-3 text-left text-sm font-semibold text-gray-600">Status</th>
                    <th class="px-4 py-3 text-right text-sm font-semibold text-gray-600"></th>
                </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                {#each orders as order}
                    {@render ordersItem(order)}
                {/each}
                </tbody>
            </table>
        </div>
    {/if}
</div>
