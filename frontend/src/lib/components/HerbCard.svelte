<script>
    let {data, limitToAddCart = false, shadow = false} = $props();

    const cardClasses = shadow
        ? "card p-0 h-full bg-gray-200 shadow hover:shadow-lg hover:-translate-y-0.5"
        : "card p-0 h-full bg-gray-200";

    const images = data?.medias?.filter(img => img.type === "IMAGE" && img.file)
    const thumbnailSrc = images?.filter(img => img.is_featured)
    const alternativeImageSrc = images?.length > 0 ? images[0]?.file : data.image_link || "/herbs.jpg";

</script>

<div class={cardClasses}>
    {#if limitToAddCart}
        <div class="card-backdrop absolute top-0 right-0 z-10 ">
            <button class="btn bg-white text-black text-sm">
                Add to cart
            </button>
        </div>
    {/if}

    <a href={`/herbs/${data.slug}/`}>
        <img
                src={thumbnailSrc?.length > 0 ? thumbnailSrc[0]?.file : alternativeImageSrc}
                alt={data.name}
                class="h-48 w-full object-cover rounded-t-xl"
                loading="lazy"
        />
    </a>

    <div class="card-body p-4">
        <div class="flex justify-between items-center">
            <a href={`/herbs/${data.slug}/`}>
                <h2 class="text-lg font-semibold font-heading text-slate-900">
                    {data.name}
                </h2>
            </a>
            {#if data.category}
            <span class="badge-info">
                {data.category}
            </span>
            {/if}
        </div>
        {#if data.latin_name}
            <p class="text-sm text-gray-600 italic">
                also known as: <span>{data.latin_name}</span>
            </p>
        {/if}


        <!--{#if data.dosage}-->
        <!--    <p class="text-sm text-gray-700 mt-2">-->
        <!--        Typical dosage: <strong>{data.dosage}</strong>-->
        <!--    </p>-->
        <!--{/if}-->
    </div>
</div>
