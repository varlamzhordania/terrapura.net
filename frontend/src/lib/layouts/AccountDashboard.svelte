<script>
    import {
        faHome,
        faBox,
        faMapMarkerAlt,
        faCog,
        faSignOutAlt
    } from '@fortawesome/free-solid-svg-icons';
    import Fa from "svelte-fa";
    import {handleLogout} from "$lib/utils.svelte.js";
    import {page} from "$app/state";

    const navigations = [
        {
            title: "Dashboard",
            url: "/account",
            icon: faHome,
        },
        {
            title: "Orders",
            url: "/account/orders",
            icon: faBox,
        },
        {
            title: "Addresses",
            url: "/account/addresses",
            icon: faMapMarkerAlt,
        },
        {
            title: "Settings",
            url: "/account/settings",
            icon: faCog,
        },
        {
            title: "Sign out",
            icon: faSignOutAlt,
            todo: () => handleLogout(),
        }
    ];

    let {children} = $props()


</script>


{#snippet navItem(data)}
    <li class="p-2 rounded-md {page.url.pathname === data.url ? 'bg-gray-200' : ''} hover:bg-gray-200 cursor-pointer">
        {#if data.url}
            <a href={data.url} class="flex gap-1 justify-start items-center w-full">
                <Fa icon={data.icon} size="lg" style="min-width: 30px"/>
                <span class="font-heading font-medium capitalize">{data.title}</span>
            </a>
        {:else if data.todo}
            <button type="button" class="flex gap-1 justify-start items-center cursor-pointer w-full"
                    onclick={()=> data.todo()}>
                <Fa icon={data.icon} size="lg" style="min-width: 30px"/>
                <span class="font-heading font-medium capitalize">{data.title}</span>
            </button>
        {:else }
            <Fa icon={data.icon} size="lg" style="min-width: 30px"/>
            <span class="font-heading font-medium capitalize">{data.title}</span>
        {/if}
    </li>
{/snippet}

<div class="grid grid-cols-1 lg:grid-cols-10 xl:grid-cols-12 gap-8 lg:gap-16">
    <aside class="col-span-1 lg:col-span-5 xl:col-span-3">
        <div class="card bg-gray-100">
            <ul class="list-none space-y-2">
                {#each navigations as item}
                    {@render navItem(item)}
                {/each}
            </ul>
        </div>
    </aside>

    <section class="col-span-1 lg:col-span-7 xl:col-span-9">
        {@render children()}
    </section>


</div>