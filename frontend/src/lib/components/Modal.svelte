<script>
    import {fade} from "svelte/transition"

    let {
        open = false,
        onClose = () => {
            $inspect(open)
        },
        size = "md",
        children,
    } = $props()

    const sizeMap = {
        sm: 'sm',
        md: 'md',
        lg: 'lg',
        xl: '2xl'
    };

</script>

{#if open}
    <div class="fixed inset-0 z-50 flex items-center justify-center px-4" transition:fade>
        <button class="backdrop" onclick={onClose}></button>
        <div class={`bg-white rounded-xl shadow-lg relative w-full max-w-${sizeMap[size]} z-40 p-6`}>
            <button
                    class="absolute top-2 right-2 text-gray-400 hover:text-gray-700"
                    onclick={onClose}
                    aria-label="Close"
            >
                ✕
            </button>
            {@render children()}
        </div>
    </div>
{/if}
