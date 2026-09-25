import {browser} from "$app/environment";
import {deleteBasketItem, fetchBasketData, fetchBasketPricesUpdate, postBasketData} from "$lib/api/checkout.js";
import {authState} from "$lib/states/auth.svelte.js";
import {configState} from "$lib/states/config.svelte.js";

class BasketStore {
    state = $state({
        items: [],
        taxRate: 0.18, // example: 18% VAT
    });
    static LOCAL_NAME = "te-basket"

    async init() {
        await this.load()
    }

    async add(item) {
        const existing = this.state.items.find(
            i => i.price.id === item.price.id && i.herb.id === item.herb.id
        );
        if (existing) {
            existing.quantity += item.quantity;
        } else {
            this.state.items.push(item);
        }

        await this.save()
    }

    async increment(item, number) {
        const existing = this.state.items.find(
            i => i.price.id === item.price.id && i.herb.id === item.herb.id
        );

        if (existing) {
            const newQuantity = existing.quantity + number;

            // Keep precision while avoiding floating-point drift
            existing.quantity = Math.round(newQuantity * 1e10) / 1e10;

            await this.save();
        }
    }


    async decrement(item, number) {
        const existing = this.state.items.find(i => i.price.id === item.price.id && i.herb.id === item.herb.id)
        if (existing) {
            existing.quantity = parseFloat((existing.quantity - number).toFixed(10));
            if (existing.quantity <= 0) {
                await this.remove(existing.price.id, existing.herb.id);
            }
            await this.save();
        }
    }

    async remove(priceId, herbId) {
        this.state.items = this.state.items.filter(
            i => !(i.price.id === priceId && i.herb.id === herbId)
        );
        await this.save(false)
        await deleteBasketItem({price_id: priceId})
    }

    async clear() {
        this.state.items = [];
        await this.save();
    }

    async updatePrices(currency) {
        if (!currency) return;

        // Collect all price IDs in the basket
        const priceIds = this.state.items.map(item => item.price.id);
        if (!priceIds.length) return;

        try {
            // Fetch updated prices from API
            const updatedPrices = await fetchBasketPricesUpdate(priceIds, currency);

            // Create a lookup map for quick access
            const priceMap = Object.fromEntries(updatedPrices.map(p => [p.id, p]));

            // Update basket items in-place
            this.state.items = this.state.items.map(item => ({
                ...item,
                price: priceMap[item.price.id] || item.price // fallback to old price if not found
            }));

            this.save(false);
        } catch (err) {
            console.error("Failed to update basket prices:", err);
        }
    }

    async save(forceDB = true) {
        localStorage.setItem(BasketStore.LOCAL_NAME, JSON.stringify(this.state.items))

        if (browser && authState.logged_in && forceDB) {
            try {
                await this.saveDB()
            } catch (e) {
                console.error('Failed to save basket to DB:', e)
            }
        }
    }


    async load(forceDB = false) {
        // Load local storage first
        if (browser) {
            const localItems = JSON.parse(localStorage.getItem(BasketStore.LOCAL_NAME)) || []
            this.set(localItems)
        }

        if ((browser && authState.logged_in) || forceDB)
            await this.loadDB()

    }

    async saveDB() {
        await postBasketData(this.items)
    }

    async loadDB() {
        const data = await fetchBasketData(configState.get("currency"));
        if (data && data.items) {
            const parsedItems = data.items.map(item => ({
                ...item,
                quantity: parseFloat(item.quantity),
                // price: {
                //     ...item.price,
                //     price: parseFloat(item.price.price)
                // }
            }));

            this.set(parsedItems);
            await this.save(false);
        }
    }

    get total_offer() {
        return this.state.items.length
    }

    get items() {
        return this.state.items;
    }

    get subtotal() {
        const total = this.items.reduce((acc, item) => {
            const price = parseFloat(item.price.converted_price ?? item.price.price);
            const quantity = parseFloat(item.quantity);
            if (isNaN(price) || isNaN(quantity)) return acc;

            const itemTotal = price * quantity;
            return acc + itemTotal;
        }, 0);

        // Final rounding
        return total;
    }


    get tax() {
        return this.state.taxRate
    }

    get taxAmount() {
        return this.subtotal * this.tax
    }

    get total() {
        return this.subtotal + this.taxAmount;
    }

    set(items) {
        this.state.items = items;
    }
}

export const basket = new BasketStore();
await basket.init()