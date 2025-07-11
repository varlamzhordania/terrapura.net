export function formatCurrency(amount, currency = 'USD', locale = 'en-US') {
    const num = parseFloat(amount);
    if (isNaN(num)) return amount;

    // Dynamic precision: 2 decimals for large numbers, up to 4 for small
    const minimumFractionDigits = num < 1 ? 2 : 0;
    const maximumFractionDigits = num < 1 ? 4 : 2;

    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency,
        minimumFractionDigits,
        maximumFractionDigits,
    }).format(num);
}
