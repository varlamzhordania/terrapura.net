<script>
    import Fa from "svelte-fa";
    import {
        faChevronLeft, faChevronRight,
        faHandHoldingMedical, faHeadSideCough,
        faInfoCircle,
        faLink, faTags,
        faTriangleExclamation
    } from "@fortawesome/free-solid-svg-icons";
    import {register} from "swiper/element/bundle";
    import {onMount} from "svelte";

    let {data} = $props();
    const images = data?.medias?.filter(img => img.type === "IMAGE" && img.file)

    register();
    let swiperThumbnail;

    onMount(() => {
        Object.assign(swiperThumbnail, {
            slidesPerView: 1,
            spaceBetween: 10,
            autoplay: true,
            speed: 500,
            loop: true,
        });
        swiperThumbnail.initialize();
    })

</script>

<svelte:head>
    <title>{data.meta_title || data.name}</title>
    {#if data.meta_description}
        <meta name="description" content={data.meta_description}/>
    {/if}
    {#if data.meta_keywords}
        <meta name="keywords" content={data.meta_keywords}/>
    {/if}
</svelte:head>

<div class="max-w-6xl mx-auto p-6 grid grid-cols-1 md:grid-cols-3 gap-8">
    <div class="md:col-span-1 space-y-4">

        <swiper-container
                bind:this={swiperThumbnail}
                init="false"
                class="rounded-md"
        >
            <div slot="container-end">
                <button class="btn text-gray-200 absolute top-0 z-10 left-2 bottom-0 my-auto bg-black/60 h-[35px] w-[35px] rounded-full"
                        onclick="{() => swiperThumbnail.swiper.slidePrev()}">
                    <Fa icon={faChevronLeft} size="lg"/>
                </button>
                <button class="btn text-gray-200 absolute top-0 z-10 right-2 bottom-0 my-auto bg-black/60 h-[35px] w-[35px] rounded-full"
                        onclick="{() => swiperThumbnail.swiper.slideNext()}">
                    <Fa icon={faChevronRight} size="lg"/>
                </button>
            </div>
            {#each images as image}
                <swiper-slide loading="lazy">
                    <img
                            src={image.file || '/herbs.jpg'}
                            alt={data.name}
                            class="rounded-md w-full object-cover aspect-video h-64"
                            loading="lazy"
                    />
                </swiper-slide>
            {/each}
        </swiper-container>


        <div class="space-y-2">
            {#if data?.tags?.length > 0}
                <div class="border-b-2 border-b-gray-300 pb-4 space-y-1">
                    <div class="flex justify-start items-center gap-2">
                        <Fa icon={faTags}/>
                        <h2 class="font-medium font-heading">
                            Tags:
                        </h2>
                    </div>
                    <div class="flex justify-start items-center flex-wrap gap-2">
                        {#each data.tags as tag}
                            <a href="/herbs?tags={tag.slug}" class="badge-neutral  hover:underline">{tag.name}</a>
                        {/each}
                    </div>
                </div>
            {/if}
            {#if data?.sources?.length > 0}
                <div class="space-y-1 border-b-2 border-b-gray-300 pb-4 md:border-b-0">
                    <div class="flex justify-start items-center gap-2">
                        <Fa icon={faLink}/>
                        <h2 class="font-medium font-heading">
                            Sources:
                        </h2>
                    </div>

                    <div class="flex justify-start items-center flex-wrap gap-2">
                        {#each data.sources as source}
                            <a href={source.url} class="badge-neutral hover:underline">{source.name}</a>
                        {/each}
                    </div>
                </div>
            {/if}
        </div>
    </div>

    <!-- Description and Info -->
    <div class="md:col-span-2 space-y-2">
        <div class="border-b-2 border-b-gray-300 pb-4 mb-4">
            <div class="flex justify-between items-center">
                <h1 class="text-2xl font-bold text-slate-800">{data.name}</h1>
                {#if data.category}
                    <a href="/herbs?category={data.category.slug}" class="badge-info w-fit text-lg  hover:underline">
                        {data.category.name}
                    </a>
                {/if}
            </div>
            <p class="italic text-slate-600 font-medium">also known as: {data.latin_name}</p>
        </div>
        <div class="space-y-2 border-b-2 border-b-gray-300 pb-4 mb-4">
            <div class="prose prose-slate max-w-none">
                {@html data.description}
            </div>
            {#if data.ailments.length > 0}
                <div>
                    <div class="flex justify-start items-center gap-2 mb-2 text-slate-700 bg-gray-200 p-2 rounded-md">
                        <Fa icon={faHandHoldingMedical} size="lg"/>
                        <h2 class="text-lg font-bold font-heading">
                            Helps With
                        </h2>
                    </div>

                    <ul class="list-inside list-unstyled text-gray-700 space-y-2">
                        {#each data.ailments as ailment}
                            <li class="px-4 bg-primary-700/20 py-2 rounded-md flex justify-start items-start flex-wrap">
                                <h3 class="font-heading font-semibold">{ailment.name}: </h3>
                                <p class="px-2">
                                    {ailment.description}
                                </p>
                            </li>
                        {/each}
                    </ul>
                </div>
            {/if}
            {#if data.symptoms.length > 0}
                <div>
                    <div class="flex justify-start items-center gap-2 mb-2 text-slate-700 bg-gray-200 p-2 rounded-md">
                        <Fa icon={faHeadSideCough} size="lg"/>
                        <h2 class="text-lg font-bold font-heading">
                            Relieves Symptoms
                        </h2>
                    </div>
                    <ul class="list-inside list-unstyled text-gray-700 space-y-2">
                        {#each data.symptoms as symptom}
                            <li class="px-4 bg-indigo-700/20 py-2 rounded-md flex justify-start items-start flex-wrap">
                                <h3 class="font-heading font-semibold">{symptom.name}: </h3>
                                <p class="px-2">
                                    {symptom.description}
                                </p>
                            </li>
                        {/each}
                    </ul>
                </div>
            {/if}
        </div>


        {#if data.dosage}
            <div class="alert alert-info">
                <div class="flex justify-start items-center flex-wrap gap-2">
                    <Fa icon={faInfoCircle} size="lg"/>
                    <h2 class="text-lg font-medium font-heading">
                        Recommended Dosage :
                    </h2>
                    <p>{data.dosage}</p>
                </div>

            </div>
        {/if}


        {#if data.side_effects.length > 0}
            <div class="alert alert-danger">
                <div class="flex justify-start items-center flex-wrap gap-2">
                    <Fa icon={faTriangleExclamation} size="lg"/>
                    <h2 class="text-lg font-medium font-heading">Possible Side Effects</h2>
                </div>
                <ul class="list-disc list-inside px-2 text-sm">
                    {#each data.side_effects as effect}
                        <li>{effect.name}</li>
                    {/each}
                </ul>
            </div>
        {/if}
    </div>
</div>

