<script>
    import {onMount} from "svelte";
    import {page} from "$app/state";
    import {slide} from "svelte/transition";
    import {authState} from "$lib/states/auth.svelte.js";
    import {partnerState} from "$lib/states/partner.svelte.js";
    import {
        faBars,
        faBox,
        faBoxesStacked, faCartShopping, faChevronDown, faChevronRight, faCubes, faDoorOpen,
        faGear, faHouse, faSackDollar,
        faUsers, faUserTie, faWarehouse
    } from '@fortawesome/free-solid-svg-icons'
    import Fa from "svelte-fa";
    import {onNavigate} from "$app/navigation";

    let selectPartnerRole = $derived(partnerState.role);

    let openSidebar = $state(false)

    let {children} = $props()


    let menuItems = $state([
        {
            label: "Dashboard",
            href: "/seller",
            icon: faHouse,
        },
        {
            label: "Inventory",
            icon: faBoxesStacked,
            open: false,
            children: [
                {
                    label: "Bases",
                    href: "/seller/inventory/base",
                    icon: faWarehouse,
                },
                {
                    label: "Stock",
                    href: "/seller/inventory/stocks",
                    icon: faCubes,
                },
            ],
        },
        {
            label: "Orders",
            href: "/seller/orders",
            icon: faCartShopping,
        },
        {
            label: "Customers",
            href: "/seller/customers",
            icon: faUsers,
        },
        {
            label: "Staffs",
            href: "/seller/staffs",
            icon: faUserTie,
        },
        {
            label: "Financial",
            href: "/seller/financial",
            icon: faSackDollar,
        },
        {
            label: "Settings",
            href: "/seller/settings",
            icon: faGear,
        },
    ]);
    const menuItemPathMatch = (data) => {
        const currentPath = page.url.pathname
        if (data.href) {
            return data.href === currentPath
        }
        if (data.children) {
            return data.children.find(x => x.href === currentPath)
        }

        return false

    }


    const handleSidebar = () => openSidebar = !openSidebar


    function handleSelectPartnerRole(e) {
        partnerState.role = authState.user.partner_staff.find(
            (x) => x.partner_id === parseInt(e.target.value)
        )
    }

    onMount(() => {
        if (partnerState.role === null && authState.user.partner_staff !== null) {
            partnerState.role = authState.user.partner_staff[0];
        }

        menuItems = menuItems.map(item => ({
            ...item,
            open: menuItemPathMatch(item)
        }));
    });

    onNavigate(() => {
        if (!document.startViewTransition) return
        return new Promise(fulfill => {
            document.startViewTransition(() => new Promise(fulfill))
        })
    })


</script>

{#snippet navItem(data, isChild = false)}
    {#if data.children}
        <ul class="list-none space-y-2">
            <li class="bordered-nav-item" aria-current={menuItemPathMatch(data) ? "page" : "none"}>
                <button class="w-full flex justify-between items-center gap-2 cursor-pointer"
                        onclick={() => data.open = !data.open}>
                    <div class="flex justify-start items-center gap-3">
                        <Fa icon={data.icon} size="lg" class="min-w-8"/>
                        <span class="font-semibold text-sm capitalize">{data.label}</span>
                    </div>
                    <Fa icon={data.open ? faChevronRight :faChevronDown } size="xs"/>
                </button>
            </li>
            {#if data.open}
                <div class="space-y-2" transition:slide>
                    {#each data.children as child}
                        {@render navItem(child, true)}
                    {/each}
                </div>
            {/if}
        </ul>
    {:else}
        <li class:nested-nav-item={isChild} class:bordered-nav-item={!isChild}
            aria-current={menuItemPathMatch(data) ? "page" : "none"}>
            <a href={data.href}
               class="w-full flex justify-between items-center ">
                <div class="flex justify-start items-center gap-3">
                    <Fa icon={data.icon} size="lg" class="min-w-8"/>
                    <span class="font-semibold text-sm capitalize">{data.label}</span>
                </div>
            </a>
        </li>
    {/if}

{/snippet}

<main class="flex h-dvh">
    <div class="dashboard-sidebar" class:open={openSidebar}>
        <div class="dashboard-sidebar-wrapper">
            <div class="text-center border-b border-b-gray-300 pb-2 flex justify-center items-center">
                <enhanced:img src="/static/logo-name.png" alt="logo" class="w-32"/>
            </div>

            <ul class="list-none space-y-2 grow">
                {#each menuItems as item}
                    {@render navItem(item)}
                {/each}
            </ul>

            <ul class="list-none space-y-2">
                <li class="bordered-nav-item">
                    <a href="/" class="flex justify-between items-center">
                        <div class="flex justify-start items-center gap-3">
                            <Fa icon={faDoorOpen} size="lg" class="min-w-8"/>
                            Exit
                        </div>
                    </a>
                </li>
            </ul>
        </div>
    </div>
    <button class="backdrop" class:hidden={!openSidebar} aria-label="backdrop" tabindex="backdrop"
            onclick={handleSidebar}></button>

    <div class="dashboard-content">
        <div class="dashboard-header">
            <div>
                <button class="btn lg:hidden" onclick={handleSidebar}>
                    <Fa icon={faBars} size="lg"/>
                </button>
            </div>
            <div class="flex justify-start items-center space-x-2">
                <div class="min-w-28">
                    <select
                            class="form-control-field"
                            id="select-partner"
                            name="select-partner"
                            onchange={handleSelectPartnerRole}
                    >
                        {#each authState.user.partner_staff as partner}
                            <option value={partner.partner_id}
                                    selected={partner.partner_id === selectPartnerRole?.partner_id}>
                                {partner.partner_name}
                            </option>
                        {/each}
                    </select>
                </div>

                <button class="btn ">
                    <Fa icon={faGear} size="lg"/>
                </button>

            </div>

        </div>

        <div class="p-4">
            {@render children()}
        </div>
    </div>
</main>

<style lang="postcss">
    @reference "tailwindcss";

    .dashboard-sidebar {
        scrollbar-gutter: stable both-edges;
        @apply fixed lg:relative z-50 top-0 left-0 bg-white h-full w-[60%] lg:w-[220px] overflow-y-auto border-r border-r-gray-300 -translate-x-full lg:-translate-x-0 transition duration-500;
    }

    .dashboard-sidebar.open {
        @apply -translate-x-0;
    }

    .dashboard-sidebar-wrapper {
        @apply py-2 h-full flex flex-col space-y-4;
    }

    .dashboard-content {
        @apply w-full bg-gray-100/80;
    }

    .dashboard-header {
        @apply w-full bg-white px-4 py-1.5 border-b border-b-gray-300 flex justify-between items-center;
    }

</style>
