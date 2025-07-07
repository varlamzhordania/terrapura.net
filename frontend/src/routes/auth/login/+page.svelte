<script>
    import {goto} from '$app/navigation';
    import {authState, setAuth} from '$lib/states/auth.svelte.js';
    import Fa from "svelte-fa";
    import {faExclamationCircle} from "@fortawesome/free-solid-svg-icons";

    if (authState.logged_in)
        goto('/')

    let email = '';
    let password = '';
    let error = '';
    let loading = false;

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

            goto("/")

        } catch (err) {
            error = err.message || 'Login failed';
        } finally {
            loading = false;
        }
    }

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


    <h1 class="text-2xl font-bold mb-6 text-center">Login</h1>

    <form on:submit|preventDefault={handleLogin} class="space-y-4">
        <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
            <input
                    id="email"
                    type="text"
                    bind:value={email}
                    required
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
            />
        </div>

        <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <input
                    id="password"
                    type="password"
                    bind:value={password}
                    required
                    class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 shadow-sm focus:outline-none focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
            />
        </div>
        <button
                type="submit"
                class="btn btn-primary w-full"
                disabled={loading}
        >
            {loading ? 'Logging in...' : 'Login'}
        </button>
    </form>

    <div class="text-sm text-center mt-4 text-gray-500">
        Don’t have an account?
        <a href="/register" class="text-primary-600 hover:underline">Register</a>
    </div>
</div>
