import {clearAuth} from "$lib/states/auth.svelte.js";
import {goto} from "$app/navigation";

export function formatCurrency(amount, currency = 'USD', locale = 'en-US') {
    const num = parseFloat(amount);
    if (isNaN(num)) return amount;

    const rounded = Math.round(num * 100) / 100; // round to 2 decimals

    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(rounded);
}


export function inputSteps(unit) {
    const WHOLE_UNITS = ['unit', 'bag', 'box', 'pack'];

    // Set input constraints based on unit type
    let step = $state(WHOLE_UNITS.includes(unit) ? 1 : 0.01);
    let min = $state(step);

    return [step, min]
}

export const handleLogout = async () => {
    const response = await fetch("/api/auth/logout")
    if (response.ok) {
        clearAuth()
        goto("/auth/login")
    }
}