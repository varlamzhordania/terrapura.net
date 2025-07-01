<script>

    import Fa from "svelte-fa";
    import {faMagnifyingGlass} from "@fortawesome/free-solid-svg-icons";




</script>

<!-- Hero Section -->
<section class="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-8 min-h-dvh">
    <div class="col-span-1 md:col-span-2 lg:col-span-4">
        <div class="w-full h-full flex flex-col justify-start items-start space-y-2">
            <h1 class="font-bold font-heading text-2xl lg:text-5xl w-full mt-44">
                Your Trusted Source for<br/>Medical Herbs
            </h1>
            <p class="text-slate-500 lg:text-2xl w-full">
                Browse herbal remedies by category or trusted sellers.
            </p>

            <form class="max-w-xl w-full mt-14">
                <label for="default-search" class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
                <div class="relative">
                    <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                        <Fa icon={faMagnifyingGlass} class="text-gray-400"/>
                    </div>
                    <input type="search" id="default-search"
                           class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-primary-600 focus:border-primary-600 "
                           placeholder="Search Mockups, Logos..." required/>
                    <button type="submit"
                            class="absolute end-2.5 bottom-2.5 btn btn-primary">
                        Search
                    </button>
                </div>
            </form>
        </div>
    </div>
    <div class="col-span-1 md:col-span-2 lg:col-span-4">
        <div class="">
            <img src="/basket.jpg" alt="a wooden basket filled with herbs" class="bubble object-cover"/>
        </div>
    </div>
</section>

<section class="min-h-dvh">
    <h2 class="font-heading font-bold text-center text-2xl">
        Categories
    </h2>

    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 xl:grid-cols-6">
        {#each }
    </div>

</section>