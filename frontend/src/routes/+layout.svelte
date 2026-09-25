<script>
    import '../app.css';
    import {authState, setAuth} from "$lib/states/auth.svelte.js";
    import Root from "$lib/layouts/Root.svelte";
    import {page} from "$app/state";
    import {basket} from "$lib/states/basket.svelte.js";
    import SellerDashboard from "$lib/layouts/SellerDashboard.svelte";
    import {onNavigate} from "$app/navigation";

    let {children, data} = $props();

    if (data.access_token) {
        setAuth({access_token: data.access_token, user: data.user})
    }
    let path = $derived(page.url.pathname);

    $effect(() => {
        if (authState.logged_in) {
            basket.load(true)
        }
    })


</script>

{#if path.startsWith('/seller')}
    <SellerDashboard>
        {@render children()}
    </SellerDashboard>
{:else }
    <Root>
        {@render children()}
    </Root>
{/if}