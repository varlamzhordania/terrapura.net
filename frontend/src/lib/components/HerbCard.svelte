<script>
    let {data, limitToAddCart = false, shadow = false} = $props()

    const cardClasses = shadow ? "card p-0 h-full bg-gray-200 shadow" : "card p-0 h-full bg-gray-200"
</script>


<div class={cardClasses}>
    {#if limitToAddCart}
        <div class="card-backdrop ">
            <button class="btn bg-white text-black">
                Add to cart
            </button>
        </div>
    {/if}
    <a href="/herbs/{data.slug}/">
        <img src="/herbs.jpg" alt={data.name} class="h-48"/>
    </a>
    <div class="card-body z-50">
        <h2 class=" text-lg font-semibold">{data.name}</h2>
        <div class="text-xl mt-2 font-bold text-slate-900">
            ${data.price.toFixed(2)}
        </div>
    </div>

</div>


