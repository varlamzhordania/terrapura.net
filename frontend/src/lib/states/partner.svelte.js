import {browser} from "$app/environment";

class PartnerStore {
    state = $state({
        partner: null,
        role: null,
    });

    static LOCAL_NAME = "te-ps";

    constructor() {
        // Load from local storage on init
        this.loadFromLocal();
    }

    saveToLocal() {
        localStorage.setItem(PartnerStore.LOCAL_NAME, JSON.stringify(this.state));
    }

    loadFromLocal() {
        try {
            let data ;
            if (browser) data = localStorage.getItem(PartnerStore.LOCAL_NAME);
            if (data) {
                const parsed = JSON.parse(data);
                this.state.partner = parsed.partner ?? null;
                this.state.role = parsed.role ?? null;
                return parsed;
            }
            return null;
        } catch (e) {
            console.error("Failed to load partner from localStorage", e);
            return null;
        }
    }

    get partner() {
        return this.state.partner
    }

    get role() {
        return this.state.role
    }

    set partner(partner) {
        this.state.partner = partner;
        this.saveToLocal();
    }

    set role(role) {
        this.state.role = role;
        this.saveToLocal();
    }

    reset() {
        this.state.partner = null;
        this.state.role = null;
        localStorage.removeItem(PartnerStore.LOCAL_NAME);
    }

}

// Export a singleton instance
export const partnerState = new PartnerStore();
