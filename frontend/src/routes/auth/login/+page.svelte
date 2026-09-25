<script>
    import {goto} from '$app/navigation';
    import {authState, setAuth} from '$lib/states/auth.svelte.js';
    import Fa from "svelte-fa";
    import {faExclamationCircle} from "@fortawesome/free-solid-svg-icons";
    import {browser} from "$app/environment";
    import {onMount} from "svelte";
    import Spinner from "$lib/components/Spinner.svelte";

    if (authState.logged_in && browser) {
        goto('/')
    }

    let email = $state('');
    let password = $state('');
    let error = $state('');
    let loading = $state(false);
    let redirectTo = $state('/');

    async function handleLogin(event) {
        event.preventDefault();
        error = '';
        loading = true;

        try {
            const response = await fetch("/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({email, password})
            });
            const data = await response.json()
            if (!response.ok) {
                throw new Error(data.error)
            }

            const {access_token, expires_in, user} = data

            setAuth({access_token: access_token, expire_in: expires_in, user: user})

            goto(redirectTo)

        } catch (err) {
            error = err.message || 'Login failed';
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        const urlParams = new URLSearchParams(window.location.search)
        if (urlParams.has("redirectTo"))
            redirectTo = urlParams.get("redirectTo")
    })


</script>

<div class="max-w-md mx-auto mt-16 bg-white shadow-md p-8 rounded-md">

    {#if error}
        <div class="alert alert-danger mb-4">
            <div class="text-lg font-bold flex justify-start items-center gap-2">
                <Fa icon={faExclamationCircle} size="lg"/>
                <h2 class="font-heading">
                    Login Failed
                </h2>
            </div>
            <ul class="list-disc list-inside px-2">
                <li>
                    {error}
                </li>
            </ul>
        </div>
    {/if}


    <h1 class="text-3xl font-heading font-bold mb-6 text-center">Sign In</h1>

    <form onsubmit={handleLogin} class="space-y-4">
        <div>
            <label for="email" class="form-control-label">Email</label>
            <input
                    id="email"
                    type="text"
                    bind:value={email}
                    required
                    class="form-control-field"
            />
        </div>

        <div>
            <label for="password" class="form-control-label">Password</label>
            <input
                    id="password"
                    type="password"
                    bind:value={password}
                    required
                    class="form-control-field"
            />
        </div>
        <button
                type="submit"
                class="btn btn-primary w-full"
                disabled={loading}
        >
            {#if loading}
                <Spinner/>
            {:else}
                Sign In
            {/if}
        </button>
    </form>

    <div class="text-sm text-center mt-4 text-gray-500">
        Don’t have an account?
        <a href="/auth/register" class="text-primary-600 font-medium hover:underline">register</a>
    </div>
    <div class="text-sm text-center mt-4 text-gray-500">
        forgot password?
        <a href="/auth/forgot-password" class="text-primary-600 font-medium hover:underline">reset password</a>
    </div>
</div>
