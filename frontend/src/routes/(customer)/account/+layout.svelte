<script>
    import AccountDashboard from "$lib/layouts/AccountDashboard.svelte";

    let {children} = $props()
</script>

<AccountDashboard>
    {@render children()}
</AccountDashboard>