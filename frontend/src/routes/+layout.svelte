<script>
    import '../app.css';
    import Fa from "svelte-fa";
    import {slide} from "svelte/transition"
    import {faBars, faMagnifyingGlass, faCartShopping, faUser, faLeaf} from "@fortawesome/free-solid-svg-icons";

    let {children} = $props();

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


</script>

{#snippet navItem(item, mobile = true)}
    <li class={mobile ? "hidden lg:inline-block" :"w-full"}>
        <a href={item.link}
           class={mobile ?"nav-link" : "nav-link px-5 py-3 w-full bg-gray-200 border-md hover:bg-gray-300 hover:text-slate-600"}
           title={item.title}>{item.title}</a>
    </li>
{/snippet}

<header class="container custom-container pb-0 sticky top-0 z-50 bg-white">
    <nav class="flex justify-between items-center border-b-2 border-b-gray-300 pb-4">
        <ul class="flex justify-start items-center space-x-5">
            <li class="flex space-x-2 justify-start items-center">
                <button class="btn lg:hidden" onclick={()=> openSideBar = !openSideBar}>
                    <Fa icon={faBars} size="lg"/>
                </button>
                <a href="/" class="nav-link">
                    <img src="/logo.png" alt="logo of terrapura" class="size-24"/>
                </a>
            </li>
            {#each navigationLinks as item }
                {@render navItem(item)}
            {/each}
        </ul>
        <div class="flex justify-between items-center space-x-1">
            <button class="btn">
                <Fa icon={faMagnifyingGlass} size="lg"/>
            </button>
            <button class="btn">
                <Fa icon={faCartShopping} size="lg"/>
            </button>
            <button class="btn">
                <Fa icon={faUser} size="lg"/>
            </button>
        </div>
    </nav>
</header>

{#if openSideBar}
    <div class="sidebar" transition:slide={{axis: "x", duration: 600}}>
        <div class="flex flex-col h-full w-full p-4">
            <div class="border-b-2 border-b-gray-300 text-center py-4">
                <a href="/" class="nav-logo">Terrapura</a>
            </div>
            <ul class="flex flex-col justify-start items-center space-y-2 my-4">
                {#each navigationLinks as item }
                    {@render navItem(item, false)}
                {/each}
            </ul>
        </div>
    </div>
    <div class="backdrop" onclick={()=> openSideBar = !openSideBar}></div>
{/if}

<main class="min-h-dvh container custom-container">
    {@render children()}
</main>

<footer class="bg-white container custom-container pt-0">
    <div class="flex items-center border-t-2 border-t-gray-300 pt-4">
        <ul>
            <li>
                <a href="/" class="nav-logo">
                    <img src="/logo-name.png" alt="logo of terrapura" class="aspect-video h-32"/>
                </a>
            </li>
        </ul>
    </div>
</footer>