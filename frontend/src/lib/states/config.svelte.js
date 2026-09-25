import {browser} from '$app/environment';

class ConfigStore {
    state = $state({
        currency: 'USD',
        language: 'en',
        locale: 'en-US',
        timezone: 'UTC',
        theme: 'light',
        measurementUnit: 'metric',
        currencySymbolPosition: 'before',
        decimalSeparator: '.',
        thousandSeparator: ',',
        numberOfDecimals: 2,
        dateFormat: 'MM/dd/yyyy',
        timeFormat: '24h',
    });

    static LOCAL_NAME = 'te-config';

    constructor() {
        this.loadLocal();
    }

    set(key, value) {
        if (key in this.state) {
            this.state[key] = value;
            this.saveLocal();
        } else {
            console.warn(`Config key "${key}" does not exist.`);
        }
    }

    get(key) {
        return this.state[key];
    }


    saveLocal() {
        if (!browser) return;
        try {
            localStorage.setItem(ConfigStore.LOCAL_NAME, JSON.stringify(this.state));
        } catch (e) {
            console.error('Failed to save config to localStorage', e);
        }
    }

    loadLocal() {
        if (!browser) return;
        try {
            const stored = localStorage.getItem(ConfigStore.LOCAL_NAME);
            if (stored) {
                const parsed = JSON.parse(stored);
                Object.entries(parsed).forEach(([k, v]) => {
                    if (k in this.state) this.state[k] = v;
                });
            }
        } catch (e) {
            console.error('Failed to load config from localStorage', e);
        }
    }


    reset() {
        Object.entries({
            currency: 'USD',
            language: 'en',
            locale: 'en-US',
            timezone: 'UTC',
            theme: 'light',
            measurementUnit: 'metric',
            currencySymbolPosition: 'before',
            decimalSeparator: '.',
            thousandSeparator: ',',
            numberOfDecimals: 2,
            dateFormat: 'MM/dd/yyyy',
            timeFormat: '24h',
        }).forEach(([k, v]) => {
            this.state[k] = v;
        });
        this.saveLocal();
    }
}

export const configState = new ConfigStore();
