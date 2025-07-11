<script>

    import Fa from "svelte-fa";
    import {
        faChevronLeft,
        faChevronRight,
        faLeaf,
        faMagnifyingGlass,
        faShoppingCart
    } from "@fortawesome/free-solid-svg-icons";
    import {register} from 'swiper/element/bundle';
    import {onMount} from "svelte";
    import HerbCard from "$lib/components/HerbCard.svelte";
    import CountdownCard from "$lib/components/CountdownCard.svelte";
    import BlogCard from "$lib/components/BlogCard.svelte";

    const categories = [
        {
            id: 1,
            name: "Medical Herbs",
            slug: "medical-herbs",
            image: null,
            description: "Herbs used for their healing properties to prevent or treat various health conditions."
        },
        {
            id: 2,
            name: "Culinary Herbs",
            slug: "culinary-herbs",
            image: null,
            description: "Herbs commonly used in cooking to add flavor, aroma, and nutritional value to dishes."
        },
        {
            id: 3,
            name: "Aromatic Herbs",
            slug: "aromatic-herbs",
            image: null,
            description: "Herbs valued for their strong fragrances, often used in perfumes, essential oils, and aromatherapy."
        },
        {
            id: 4,
            name: "Sacred & Ritual Herbs",
            slug: "sacred-ritual-herbs",
            image: null,
            description: "Herbs traditionally used in spiritual, religious, or ceremonial practices across various cultures."
        },
        {
            id: 5,
            name: "Herbal Teas",
            slug: "herbal-teas",
            image: null,
            description: "Herbs prepared as infusions or tisanes for drinking, often consumed for relaxation or health benefits."
        },
        {
            id: 6,
            name: "Ayurvedic Herbs",
            slug: "ayurvedic-herbs",
            image: null,
            description: "Herbs used in Ayurveda, the traditional system of medicine from India, aimed at balancing mind, body, and spirit."
        },
        {
            id: 7,
            name: "Traditional Chinese Herbs",
            slug: "traditional-chinese-herbs",
            image: null,
            description: "Herbs integral to Traditional Chinese Medicine, used to promote balance and treat a variety of health issues."
        },
        {
            id: 8,
            name: "Adaptogenic Herbs",
            slug: "adaptogenic-herbs",
            image: null,
            description: "Herbs that help the body resist stressors and maintain homeostasis by supporting adrenal function."
        },
        {
            id: 9,
            name: "Wildcrafted Herbs",
            slug: "wildcrafted-herbs",
            image: null,
            description: "Herbs harvested responsibly from their natural habitats without cultivation, ensuring ecological balance."
        },
        {
            id: 10,
            name: "Dried Herbs",
            slug: "dried-herbs",
            image: null,
            description: "Herbs that have been preserved through drying for long-term use in cooking, teas, or remedies."
        },
    ];

    const trendHerbs = [
        {
            id: 1,
            name: "Organic Chamomile",
            slug: "organic-chamomile",
            image: null,
            price: 8.99,
            description: "Soothing dried chamomile flowers, perfect for tea or relaxation.",
        },
        {
            id: 2,
            name: "Fresh Basil Leaves",
            slug: "fresh-basil-leaves",
            image: null,
            price: 3.49,
            description: "Aromatic and flavorful, ideal for Italian cooking and salads.",
        },
        {
            id: 3,
            name: "Dried Lavender",
            slug: "dried-lavender",
            image: null,
            price: 6.75,
            description: "Fragrant lavender buds used for calming teas or sachets.",
        },
        {
            id: 4,
            name: "Turmeric Root Powder",
            slug: "turmeric-root-powder",
            image: null,
            price: 9.99,
            description: "Golden turmeric powder with anti-inflammatory benefits.",
        },
        {
            id: 5,
            name: "Holy Basil (Tulsi)",
            slug: "holy-basil-tulsi",
            image: null,
            price: 5.95,
            description: "Adaptogenic herb used in Ayurveda to reduce stress.",
        },
        {
            id: 6,
            name: "Peppermint Leaves",
            slug: "peppermint-leaves",
            image: null,
            price: 4.25,
            description: "Refreshing and cooling, great for teas and digestion.",
        },
        {
            id: 7,
            name: "Lemongrass Stalks",
            slug: "lemongrass-stalks",
            image: null,
            price: 3.99,
            description: "Citrusy herb popular in Thai cooking and herbal infusions.",
        },
        {
            id: 8,
            name: "Milk Thistle Seeds",
            slug: "milk-thistle-seeds",
            image: null,
            price: 7.49,
            description: "Supports liver health and detoxification.",
        },
    ]

    const blogPosts = [
        {
            id: 1,
            title: "The Healing Power of Tulsi: Nature’s Stress Reliever",
            slug: "healing-power-of-tulsi",
            excerpt: "Discover how Tulsi, the Holy Basil, supports immunity, reduces stress, and enhances respiratory health.",
            content: "Tulsi, also known as Holy Basil, has been used in Ayurveda for centuries. Its adaptogenic properties help the body cope with stress, while its antimicrobial and anti-inflammatory benefits make it a staple in herbal medicine...",
            author: "Dr. Mira Kapoor",
            date: "2025-06-15",
            categories: ["Ayurveda", "Herbs", "Wellness"],
            image: "/images/blog/tulsi.jpg"
        },
        {
            id: 2,
            title: "5 Herbal Teas to Boost Your Immune System",
            slug: "herbal-teas-immune-boost",
            excerpt: "From echinacea to elderberry, these herbal teas can help your body fight off colds and flu naturally.",
            content: "Immunity starts in the gut, but herbs play a powerful supporting role. Echinacea stimulates white blood cell production, elderberry is packed with antioxidants, and ginger tea supports digestion and immunity...",
            author: "Emily Nguyen",
            date: "2025-06-20",
            categories: ["Herbal Teas", "Immunity", "Home Remedies"],
            image: "/images/blog/herbal-teas.jpg"
        },
        {
            id: 3,
            title: "Wildcrafting 101: How to Forage Herbs Responsibly",
            slug: "wildcrafting-101",
            excerpt: "Learn the ethics and techniques of foraging wild herbs sustainably without harming the ecosystem.",
            content: "Wildcrafting is the art of harvesting herbs from their natural habitats. It requires knowledge, respect, and restraint. Always identify plants with certainty, harvest in small amounts, and avoid endangered species...",
            author: "Jason Eldridge",
            date: "2025-05-30",
            categories: ["Wildcrafting", "Sustainability", "Herbalism"],
            image: "/images/blog/wildcrafting.jpg"
        },
        {
            id: 4,
            title: "A Beginner's Guide to Aromatic Herbs in Cooking",
            slug: "aromatic-herbs-cooking-guide",
            excerpt: "Enhance your meals with fresh, fragrant herbs like rosemary, thyme, and basil — and learn how to use them right.",
            content: "Aromatic herbs are more than garnish — they transform dishes. Basil pairs well with tomatoes, rosemary with roasted meats, and thyme adds depth to stews. The key is using them fresh and in the right amounts...",
            author: "Lina Morales",
            date: "2025-06-05",
            categories: ["Culinary", "Aromatic Herbs", "Cooking Tips"],
            image: "/images/blog/aromatic-herbs.jpg"
        },
        {
            id: 5,
            title: "Understanding Adaptogens: Herbs for Modern Stress",
            slug: "understanding-adaptogens",
            excerpt: "Adaptogens help your body adapt to stress. Learn about ashwagandha, rhodiola, and other powerful allies.",
            content: "Adaptogens are herbs that help the body resist physical, emotional, and environmental stressors. Ashwagandha is calming, rhodiola boosts stamina, and holy basil balances cortisol. These herbs are increasingly popular in functional wellness...",
            author: "Dr. Ayesha Thomas",
            date: "2025-06-25",
            categories: ["Adaptogens", "Mental Health", "Herbal Medicine"],
            image: "/images/blog/adaptogens.jpg"
        }
    ];

    register();
    let swiperTrendHerbs;
    const swiperTrendHerbsBreakPoints = {
        768: {
            slidesPerView: 2,
            grid: {
                rows: 2,
            },
            spaceBetween: 10,
        },
        1024: {
            slidesPerView: 2,
            grid: {
                rows: 2,
            },
            spaceBetween: 10,
        },
        1280: {
            slidesPerView: 3,
            grid: {
                rows: 2,
            },
            spaceBetween: 10,
        }

    }

    onMount(() => {
        Object.assign(swiperTrendHerbs, {
            slidesPerView: 2,
            spaceBetween: 10,
            grid: {rows: 2},
            breakpoints: swiperTrendHerbsBreakPoints,
        });
        swiperTrendHerbs.initialize();
    })


</script>

{#snippet categoryCard(data)}
    <div class="col-span-1 h-full">
        <div class="card pt-6 pb-0 bg-primary-100 flex flex-col justify-between items-center shadow-none h-full">
            <h3 class="font-body font-bold text-lg capitalize text-center">{data.name}</h3>
            <div class="aspect-square w-full flex justify-center">
                <img src="/category-placeholder.png"
                     alt={data.name}
                     class="self-end my-auto object-contain object-bottom size-52"
                >
            </div>
        </div>
    </div>
{/snippet}

<!-- Hero Section -->
<section
        class="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-8 gap-4 min-h-dvh md:min-h-[600px] lg:min-h-[900px] xl:min-h-dvh">
    <div class="col-span-1 md:col-span-2 lg:col-span-4">
        <div class="w-full h-full flex flex-col justify-start items-start space-y-2">
            <h1 class="font-bold font-heading text-2xl lg:text-5xl w-full md:mt-44">
                Your Trusted Source for<br/>Medical Herbs
            </h1>
            <p class="text-slate-500 lg:text-2xl w-full">
                Browse herbal remedies by category or trusted sellers.
            </p>

            <form class="max-w-xl w-full mt-8 md:mt-14">
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
        <div class="md:mt-24 xl:mt-0">
            <img src="/basket.jpg" alt="a wooden basket filled with herbs" class="bubble object-cover"/>
        </div>
    </div>
</section>

<!-- Category Section -->
<section class="min-h-96">
    <h2 class="font-heading font-bold text-center text-2xl">
        Categories
    </h2>

    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 xl:grid-cols-6 gap-4  mt-10 min-h-64">
        {#each categories.slice(0, 6) as category}
            {@render categoryCard(category)}
        {/each}
    </div>
</section>

<!-- Featured Section -->
<section class="grid grid-cols-1 md:grid-cols-6 lg:grid-cols-10 xl:grid-cols-12 min-h-dvh gap-8 lg:gap-16 mt-64">
    <div class="col-span-1 md:col-span-2 lg:col-span-4 xl:col-span-3 flex flex-col gap-4">
        <div class="card bg-gray-200 text-slate-900 shadow-none flex items-center justify-start gap-2">
            <Fa icon={faLeaf} size="lg"/>
            <p class="text-2xl font-bold font-heading">Special offers</p>
        </div>
        <div class="card py-6 bg-primary-100 flex flex-col justify-between items-center max-h-[450px]">
            <h3 class="font-heading font-bold text-xl text-slate-900  capitalize text-center">Herbal</h3>
            <p class="text-sm font-medium capitalize">By Herbalist</p>
            <div class="w-full flex justify-center">
                <img src="/category-placeholder.png"
                     alt="special offer"
                     class="self-end mb-4 object-contain object-bottom size-44"
                >
            </div>

            <a href="/" class="btn btn-primary font-bold">Shop Now</a>


        </div>

        <div class="card py-6 bg-gray-200 flex flex-col justify-between items-center max-h-[450px]">
            <h3 class="font-heading font-bold text-xl text-slate-900  capitalize text-center">Herbal</h3>
            <p class="text-sm font-medium capitalize">By Herbalist</p>
            <div class="w-full flex justify-center">
                <img src="/category-placeholder.png"
                     alt="special offer"
                     class="self-end mb-4 object-contain object-bottom size-44"
                >
            </div>
            <a href="/" class="btn btn-primary font-bold">Shop Now</a>
        </div>

        <CountdownCard deadline={new Date('2025-07-04T18:00:00')} showSeconds="{false}"/>
    </div>
    <div class="col-span-1 md:col-span-4 lg:col-span-6 xl:col-span-9 flex flex-col gap-4">
        <div class="card bg-gray-200 text-slate-900 shadow-none flex justify-between items-center">
            <div class="flex items-center justify-start gap-2">
                <Fa icon={faLeaf} size="lg"/>
                <p class="text-2xl font-bold font-heading">
                    Trending herbs
                </p>
            </div>
            <div class="flex items-center justify-end">
                <button class="btn swiper-button-prev"
                        onclick={()=> swiperTrendHerbs.swiper.slidePrev()}
                >
                    <Fa icon={faChevronLeft} size="lg"/>
                </button>
                <button class="btn swiper-button-next"
                        onclick={()=> swiperTrendHerbs.swiper.slideNext()}
                >
                    <Fa icon={faChevronRight} size="lg"/>
                </button>
            </div>
        </div>

        <swiper-container
                bind:this={swiperTrendHerbs}
                init="false"
                class="max-h-[700px] md:max-h-[600px]"
        >
            {#each trendHerbs as product}
                <swiper-slide>
                    <HerbCard data={product} limitToAddCart/>
                </swiper-slide>
            {/each}
        </swiper-container>

        <div class="card bg-gray-200 text-slate-900 shadow-none flex items-center justify-start gap-2">
            <Fa icon={faShoppingCart} size="lg"/>
            <p class="text-2xl font-bold font-heading">
                Top Categories
            </p>
        </div>
        <div class="flex flex-wrap lg:flex-nowrap justify-between items-center gap-3">
            {#each categories.slice(0, 2) as category}
                <div class="card p-0 w-full h-[300px]">
                    <img src="/herbs.jpg" alt="{category.name}" class="h-full"/>
                    <div class="absolute p-5 w-full h-full top-0 left-0 bg-gray-900/50 rounded-md flex flex-col justify-center items-center gap-2">
                        <h3 class="text-2xl text-slate-200 font-bold font-heading text-center">{category.name}</h3>
                        <p class="text-lg text-slate-300 font-medium text-center">{category.description}</p>
                        <a href="/" class="btn btn-primary font-bold">Shop Now</a>
                    </div>
                </div>
            {/each}
        </div>
    </div>
</section>

<!-- Blog Section -->
<section class="min-h-96 bg-primary-100 rounded-md mt-32 pt-16 pb-20 px-16">
    <h2 class="font-heading font-bold text-center text-2xl mb-10">
        Visit our blog
    </h2>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 justify-center items-center gap-6">
        {#each blogPosts.slice(0, 4) as post}
            <BlogCard data={post} shadow/>
        {/each}
    </div>

</section>