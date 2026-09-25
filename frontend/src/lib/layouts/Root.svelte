<script>
    import Fa from "svelte-fa";
    import {slide} from "svelte/transition"
    import {faBars, faMagnifyingGlass, faCartShopping, faUser} from "@fortawesome/free-solid-svg-icons";
    import {authState} from "$lib/states/auth.svelte.js";
    import {basket} from "$lib/states/basket.svelte.js";
    import {handleLogout} from "$lib/utils.svelte.js";
    import Sidebar from "$lib/components/Sidebar.svelte";
    import InternationalSelector from "$lib/components/InternationalSelector.svelte";

    let {children} = $props()

    const navigationLinks = [
        {
            link: "/",
            title: "home",
        },
        {
            link: "/herbs",
            title: "herbs",
        },
        {
            link: "/blog",
            title: "blog",
        },
        {
            link: "/contact",
            title: "contact",
        },
    ]

    let openSideBar = $state(false)
    let openUserDropDown = $state(false)
    let dropDownEl = $state(null);


    const handleClickOutside = (event) => {
        if (openUserDropDown && dropDownEl && !dropDownEl.contains(event.target)) {
            openUserDropDown = false;
        }
    }


</script>

<svelte:document onclick={handleClickOutside}/>

{#snippet navItem(item, mobile = true)}
    <li class={mobile ? "hidden lg:inline-block" :"w-full"}>
        <a href={item.link}
           class={mobile ?"nav-link" : "nav-link px-5 py-3 w-full bg-gray-200 border-md hover:bg-gray-300 hover:text-slate-600"}
           title={item.title}>{item.title}</a>
    </li>
{/snippet}

<header class="container custom-container pb-0 sticky top-0 z-30 bg-white">
    <nav class="flex justify-between items-center border-b-2 border-b-gray-300 pb-4">
        <ul class="flex justify-start items-center space-x-5">
            <li class="flex space-x-2 justify-start items-center">
                <button class="btn lg:hidden" onclick={()=> openSideBar = !openSideBar}>
                    <Fa icon={faBars} size="lg"/>
                </button>
                <a href="/" class="nav-link">
                    <enhanced:img src="/static/logo.png" alt="logo of terrapura" class="w-12"/>
                </a>
            </li>
            {#each navigationLinks as item }
                {@render navItem(item)}
            {/each}
        </ul>
        <div class="flex justify-between items-center space-x-1">

            <InternationalSelector/>

            <button class="btn">
                <Fa icon={faMagnifyingGlass} size="lg"/>
            </button>
            <a href="/cart" class="btn relative">
                <Fa icon={faCartShopping} size="lg"/>
                <span class="absolute right-1 -top-0.5 bg-primary-700 text-white text-center rounded-full text-xs font-light min-w-4 w-auto h-4 px-0.5 ring-2 ring-white">
                    {basket.total_offer}
                </span>
            </a>
            {#if authState.logged_in}
                <div class="relative" bind:this={dropDownEl}>
                    <button
                            class="btn"
                            onclick={() => openUserDropDown = !openUserDropDown}

                    >
                        <Fa icon={faUser} size="lg"/>
                    </button>
                    <!-- User Dropdown menu -->
                    {#if openUserDropDown}
                        <div transition:slide
                             class="absolute inset-0 inset-auto -translate-x-3/4 m-auto z-10 bg-white divide-y divide-gray-100 rounded-md border border-gray-300 shadow-lg w-44">
                            <div class="px-4 py-3 text-sm">
                                <div>{authState.user.first_name} {authState.user.last_name}</div>
                                <div class="font-medium truncate text-slate-700">{authState.user.email}</div>
                            </div>
                            <ul class="p-2 text-sm " aria-labelledby="avatarButton">
                                <li>
                                    <a href="/account" class="block px-4 py-2 rounded-md hover:bg-gray-200">
                                        Dashboard
                                    </a>
                                </li>
                                {#if authState.user.partner_staff}
                                    <li>
                                        <a href="/seller/" class="block px-4 py-2 rounded-md hover:bg-gray-200">
                                            Seller Dashboard
                                        </a>
                                    </li>
                                {/if}
                                <li>
                                    <button class="block w-full text-start px-4 py-2 cursor-pointer rounded-md  hover:bg-gray-200"
                                            onclick={() =>handleLogout()}>
                                        Sign out
                                    </button>
                                </li>
                            </ul>
                        </div>
                    {/if}
                </div>
            {:else }
                <a href="/auth/login" class="btn btn-primary">Sign In</a>
            {/if}

        </div>
    </nav>
</header>

<Sidebar onBackdropClick={() => openSideBar = !openSideBar} open={openSideBar}>
    <div class="border-b-2 border-b-gray-300 text-center py-4">
        <a href="/" class="nav-logo">Terrapura</a>
    </div>
    <ul class="flex flex-col justify-start items-center space-y-2 my-4">
        {#each navigationLinks as item }
            {@render navItem(item, false)}
        {/each}
    </ul>
</Sidebar>

<main class="min-h-dvh container custom-container">
    {@render children()}
</main>

<footer class="bg-white container custom-container pt-0">
    <div class="flex items-center border-t-2 border-t-gray-300 pt-4">
        <ul class="flex gap-3 items-center w-full">
            <li class="grow">
                <a href="/" class="nav-logo">
                    <enhanced:img src="/static/logo-name.png" alt="logo of terrapura" class="w-32" />
                </a>
            </li>
            <li>
                <a href="/terms-of-sale" class="nav-link normal-case hover:underline">
                    Terms of Sale
                </a>
            </li>
            <li>
                <a href="/refund-policy" class="nav-link normal-case hover:underline">
                    Refund policy
                </a>
            </li>
        </ul>
    </div>
</footer>

<style lang="postcss">
    @reference tailwindcss

</style>