import {API_ENDPOINTS} from "$lib/config.js";
import {fetchWithAuth} from "$lib/api/index.svelte.js";

export async function fetchCurrencies() {
    const res = await fetch(API_ENDPOINTS.checkout.currencies);

    if (!res.ok) {
        let errDetail = `Failed to fetch available currencies`;
        try {
            const data = await res.json();
            if (data.detail) errDetail = data.detail;
        } catch (_) {
            // Fallback to default message if response isn't JSON
        }

        const err = new Error(errDetail);
        err.status = res.status;
        throw err;
    }

    return await res.json();
}

export async function fetchPaymentMethods(currency = 'usd') {
    return await fetchWithAuth(API_ENDPOINTS.checkout.paymentMethods(currency), {method: "GET"});
}


export async function fetchBasketPricesUpdate(priceIds, currency) {
    const idsParam = Array.isArray(priceIds) ? priceIds.join(',') : priceIds;
    const res = await fetch(API_ENDPOINTS.checkout.basketPricesUpdate(idsParam, currency));

    if (!res.ok) {
        let errDetail = `Failed to update basket prices`;
        try {
            const data = await res.json();
            if (data.detail) errDetail = data.detail;
        } catch (_) {
            // fallback to default message
        }

        const err = new Error(errDetail);
        err.status = res.status;
        throw err;
    }

    return await res.json();
}

export async function postBasketData(data) {
    return await fetchWithAuth(API_ENDPOINTS.checkout.basket, {
        method: "POST", body: data,
    })
}

export async function fetchBasketData(currency) {
    return await fetchWithAuth(API_ENDPOINTS.checkout.basketWithCurrency(currency), {
        method: "GET"
    })
}

export async function deleteBasketItem(item) {
    return await fetchWithAuth(API_ENDPOINTS.checkout.basket, {
        method: "DELETE", body: item
    })
}

export async function postOrder(data) {
    return await fetchWithAuth(API_ENDPOINTS.checkout.orderCreate, {
        method: "POST",
        body: data
    })
}

export async function fetchOrders({page = 1, page_size = 25}) {
    return await fetchWithAuth(API_ENDPOINTS.checkout.orderList(page, page_size), {
        method: "GET"
    })
}

export async function fetchOrderDetail(id) {
    return await fetchWithAuth(API_ENDPOINTS.checkout.orderDetail(id), {
        method: "GET"
    })
}

export async function stripeOrderPayment(data) {
    return await fetchWithAuth(API_ENDPOINTS.checkout.stripe, {
        method: "POST",
        body: data
    })
}