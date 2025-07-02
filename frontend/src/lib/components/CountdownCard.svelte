<script>
    import {onMount, onDestroy} from 'svelte';

    let {
        title = "limited time",
        description = "Hurry, ends soon",
        deadline = null,
        showSeconds = true
    } = $props();

    if (deadline === null) {
        deadline = new Date(Date.now() + 12 * 60 * 60 * 1000 + 57 * 60 * 1000);
    }

    let timeLeft = $state('00:00:00');
    let interval;

    function formatTime(ms) {
        const totalSeconds = Math.max(0, Math.floor(ms / 1000));
        const hours = String(Math.floor(totalSeconds / 3600)).padStart(2, '0');
        const minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, '0');
        const seconds = String(totalSeconds % 60).padStart(2, '0');
        return `${hours}:${minutes}:${seconds}`;
    }

    function updateTime() {
        const now = new Date();
        const diff = deadline - now;
        timeLeft = formatTime(diff);

        if (diff <= 0) {
            clearInterval(interval);
        }
    }

    onMount(() => {
        updateTime();
        interval = setInterval(updateTime, 1000);
    });

    onDestroy(() => {
        clearInterval(interval);
    });

    function getSegments() {
        const [hh, mm, ss] = timeLeft.split(':');
        return showSeconds
            ? [...hh, ':', ...mm, ':', ...ss]
            : [...hh, ':', ...mm];
    }
</script>

{#snippet segment(content)}
    <span
            class="inline-block bg-black/20 px-2 py-1 rounded shadow"
    >
        {content}
    </span>
{/snippet}


<div class="card py-6 bg-primary-100 flex flex-col justify-between items-center max-h-[450px]">
    <h3 class="font-heading font-bold text-xl text-slate-900 uppercase text-center">{title}</h3>
    <p class="text-sm font-medium">{description}</p>

    <!-- Countdown rendered as separate spans -->
    <p class="text-2xl font-bold text-slate-900 mt-4 flex items-center gap-1">
        {#each getSegments() as char (char + Math.random())}
            {#if char === ':'}
                <span class="mx-1 text-slate-700">:</span>
            {:else}
                {@render segment(char)}
            {/if}
        {/each}
    </p>
</div>
