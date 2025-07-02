<script>
    let {data, shadow = false} = $props()

    const cardClasses = shadow ? "card p-0 h-full bg-gray-100 shadow" : "card p-0 h-full bg-gray-100"
</script>


<div class={cardClasses}>
<a href="/herbs/{data.slug}/">
    <img src="/herbs.jpg" alt={data.title} class="h-32 aspect-video"/>
</a>
<div class="card-body z-50">
    <h2 class="text-lg text-slate-900 font-semibold">{data.title}</h2>
    <p class="text-sm">{data.excerpt}</p>
    <div class="flex justify-start items-center space-x-2 mt-6">
        <span class="avatar">A</span>
        <p class="text-xs font-bold capitalize">Dr. Bigdeli</p>
    </div>

</div>

</div>


