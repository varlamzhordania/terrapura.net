<script>
    import {onMount} from 'svelte';
    import {page} from "$app/state";

    let error = $state(null);

    // Parse query params from URL
    let query = page.url.searchParams

    let success = $derived(query.get('success') === 'true')
    let orderId = $derived(query.get('order_id'))
    let sessionId = $derived(query.get('session_id'));


    let orderDetails = null;

    onMount(async () => {
        if (success && orderId) {
            try {
                // Example: fetch order details from your API (optional)
                const res = await fetch(`/api/orders/${orderId}`);
                if (res.ok) {
                    orderDetails = await res.json();
                } else {
                    error = 'Failed to load order details.';
                }
            } catch (e) {
                error = 'Network error while loading order details.';
            }
        }
    });
</script>

<div class="max-w-md mx-auto p-6 border rounded shadow mt-8">
    {#if success}
        <h1 class="text-2xl font-bold mb-4 text-green-600">Payment Successful!</h1>
        <p>Thank you for your order #{orderId}.</p>
        {#if sessionId}
            <p>Your payment session ID: <code>{sessionId}</code></p>
        {/if}
        {#if orderDetails}
            <div class="mt-4 p-4 bg-gray-100 rounded">
                <h2 class="font-semibold mb-2">Order Summary:</h2>
                <p><strong>Order ID:</strong> {orderDetails.id}</p>
                <p><strong>Total:</strong> {orderDetails.total_price} {orderDetails.currency.code}</p>
                <!-- Add more order details if you want -->
            </div>
        {/if}
    {:else}
        <h1 class="text-2xl font-bold mb-4 text-red-600">Payment Cancelled</h1>
        <p>Your payment for order #{orderId} was cancelled.</p>
    {/if}

    {#if error}
        <p class="text-red-500 mt-4">{error}</p>
    {/if}

    <a href="/" class="inline-block mt-6 text-blue-600 hover:underline">
        Return to home
    </a>
</div>

<style>
    /* Add your styling here */
</style>
