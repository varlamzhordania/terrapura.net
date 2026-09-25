<script>
    import {fetchOrderDetail} from "$lib/api/checkout.js";
    import {onMount} from "svelte";

    let {data} = $props();
    let orderData = $state(null);
    let expandedItems = $state(false);

    const loadOrder = async () => {
        orderData = await fetchOrderDetail(data.id);
    }

    onMount(() => {
        loadOrder();
    });

    const toggleItems = () => {
        expandedItems = !expandedItems;
    };

    const formatDate = (dateStr) => {
        if (!dateStr) return "-";
        return Intl.DateTimeFormat(navigator.language, {
            month: "long",
            day: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit"
        }).format(new Date(dateStr));
    };

    const statusColor = (status) => {
        switch (status) {
            case "pending":
                return "bg-yellow-100 text-yellow-800";
            case "payment":
                return "bg-blue-100 text-blue-800";
            case "processing":
                return "bg-indigo-100 text-indigo-800";
            case "shipped":
                return "bg-purple-100 text-purple-800";
            case "delivered":
                return "bg-green-100 text-green-800";
            case "cancelled":
                return "bg-red-100 text-red-800";
            default:
                return "bg-gray-100 text-gray-800";
        }
    };
</script>

<div class="py-6 space-y-6">
    <h1 class="text-2xl font-bold">Order Details #{data.id}</h1>

    {#if !orderData}
        <p class="text-gray-500">Loading order details...</p>
    {:else}
        <!-- Order Summary -->
        <div class="bg-white shadow rounded-lg p-6 space-y-4">
            <div class="flex flex-col md:flex-row justify-between">
                <div class="space-y-1">
                    <p class="text-sm text-gray-500">Order ID</p>
                    <p class="font-semibold">#{orderData.id}</p>
                </div>
                <div class="space-y-1">
                    <p class="text-sm text-gray-500">Status</p>
                    <span class={`px-2 py-1 rounded-full text-sm font-medium ${statusColor(orderData.status)}`}>
                        {orderData.status}
                    </span>
                </div>
                <div class="space-y-1">
                    <p class="text-sm text-gray-500">Total</p>
                    <p class="font-semibold">{orderData.currency.symbol}{orderData.total_price}</p>
                </div>
            </div>

            <div class="space-y-1">
                <p class="text-sm text-gray-500">Created At</p>
                <p>{formatDate(orderData.created_at)}</p>
            </div>

            <div class="space-y-1">
                <p class="text-sm text-gray-500">Updated At</p>
                <p>{formatDate(orderData.updated_at)}</p>
            </div>

            <div class="space-y-1">
                <p class="text-sm text-gray-500">Delivery Address</p>
                <p>{orderData.delivery_address.full_name}</p>
                <p>{orderData.delivery_address.line1}</p>
                {#if orderData.delivery_address.line2}
                    <p>{orderData.delivery_address.line2}</p>
                {/if}
                <p>{orderData.delivery_address.city}, {orderData.delivery_address.state}</p>
                <p>{orderData.delivery_address.country}</p>
            </div>

            {#if orderData.notes}
                <div class="space-y-1">
                    <p class="text-sm text-gray-500">Notes</p>
                    <p>{orderData.notes}</p>
                </div>
            {/if}
        </div>

        <!-- Order Items -->
        <div class="bg-white shadow rounded-lg p-6">
            <div class="flex justify-between items-center mb-4">
                <h2 class="font-semibold text-lg">Items</h2>
                <button
                        class="text-blue-600 hover:text-blue-800 text-sm font-medium"
                        on:click={toggleItems}
                >
                    {expandedItems ? "Hide Items" : "View Items"}
                </button>
            </div>

            {#if expandedItems}
                <ul class="space-y-3">
                    {#each orderData.items as item}
                        <li class="flex flex-col md:flex-row justify-between items-start bg-gray-50 rounded p-3 shadow-sm">
                            <div class="space-y-1 md:mr-4">
                                <p class="font-medium">{item.inventory_item.herb.name} ({item.inventory_item.unit})</p>
                                <p class="text-gray-500 text-sm">
                                    Qty: {Number(item.quantity)} × {orderData.currency.symbol}{item.unit_price}
                                </p>
                                <p class="text-gray-500 text-sm">
                                    Country: {item.inventory_item.country}
                                </p>
                                <p class="text-gray-500 text-sm">
                                    Base: {item.inventory_item.base.name}
                                </p>
                            </div>
                            <div class="font-semibold text-gray-800 mt-2 md:mt-0">
                                {orderData.currency.symbol}{item.total_price}
                            </div>
                        </li>
                    {/each}
                </ul>
            {/if}
        </div>

        <!-- Shipment Info -->
        {#if orderData.shipment}
            <div class="bg-white shadow rounded-lg p-6 space-y-2">
                <h2 class="font-semibold text-lg">Shipment</h2>
                <p>Status: <span
                        class={`px-2 py-1 rounded-full text-sm font-medium ${statusColor(orderData.shipment.status)}`}>{orderData.shipment.status}</span>
                </p>
                <p>Carrier: {orderData.shipment.carrier || "-"}</p>
                <p>Tracking #: {orderData.shipment.tracking_number || "-"}</p>
                <p>Shipped At: {formatDate(orderData.shipment.shipped_at)}</p>
                <p>Delivered At: {formatDate(orderData.shipment.delivered_at)}</p>
                {#if orderData.shipment.notes}
                    <p>Notes: {orderData.shipment.notes}</p>
                {/if}
            </div>
        {/if}

        <!-- Payment Info -->
        {#if orderData.payment}
            <div class="bg-white shadow rounded-lg p-6 space-y-2">
                <h2 class="font-semibold text-lg">Payment</h2>
                <p>Method: {orderData.payment.method}</p>
                <p>Amount: {orderData.payment.currency.symbol}{orderData.payment.amount}</p>
                <p>Status: {orderData.payment.status}</p>
                <p>Transaction ID: {orderData.payment.transaction_id}</p>
                <p>Paid At: {formatDate(orderData.payment.paid_at)}</p>
            </div>
        {/if}
    {/if}
</div>
