<script>

    let {children, onBackdropClick, open = false} = $props()

</script>

<div class="sidebar" class:open={open}>
    <div class="flex flex-col h-full w-full p-4">
        {@render children()}

    </div>
</div>
<button class="backdrop" class:hidden={!open} aria-label="backdrop" tabindex="backdrop"
        onclick={()=> onBackdropClick()}></button>


<style lang="postcss">
    @reference "tailwindcss";

    .sidebar {
        @apply fixed top-0 left-0 h-full w-[60%] z-50 bg-white -translate-x-full transition duration-500;
    }

    .sidebar.open {
        @apply -translate-x-0;
    }
</style>