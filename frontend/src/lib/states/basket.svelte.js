import {browser} from "$app/environment";

class BasketStore {
    state = $state({
        items: []
    });
    LOCAL_NAME = "te-basket"

    constructor() {
        this.loadLocal()
    }

    add(item) {
        const existing = this.state.items.find(
            i => i.price.id === item.price.id && i.herb.id === item.herb.id
        );
        if (existing) {
            existing.quantity += item.quantity;
        } else {
            this.state.items.push(item);
        }

        this.saveLocal()
    }

    remove(offerId, priceId) {
        this.state.items = this.state.items.filter(
            i => !(i.offerId === offerId && i.priceId === priceId)
        );
    }

    clear() {
        this.state.items = [];
    }

    saveLocal() {
        localStorage.setItem(this.LOCAL_NAME, JSON.stringify(this.state.items))
    }

    loadLocal() {
        this.set(browser && JSON.parse(localStorage.getItem(this.LOCAL_NAME)) || [])
    }

    get total_offer() {
        return this.state.items.length
    }

    get items() {
        return this.state.items;
    }

    set(items) {
        this.state.items = items;
    }
}

export const basket = new BasketStore();
