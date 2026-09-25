<script>
    import Toast from "$lib/toast.js";
    import {requestPasswordReset} from "$lib/api/account.js";
    import Spinner from "$lib/components/Spinner.svelte";
    import {faExclamationCircle} from "@fortawesome/free-solid-svg-icons";
    import Fa from "svelte-fa";

    let form = $state({email: ""});
    let loading = $state(false);
    let sent = $state(false);

    const submit = async (e) => {
        e.preventDefault()

        if (!form.email) {
            Toast.error("Please enter your email address.");
            return;
        }
        loading = true;
        try {
            await requestPasswordReset({email: form.email});
            sent = true;
            Toast.success("If your email exists, we’ve sent a reset link.");
        } catch (e) {
            // Backend should return 200 for both existing/non-existing emails,
            // but in case of errors (e.g. malformed email) we show messages:
            Toast.error(e?.data?.detail || "Could not process request.");
        } finally {
            loading = false;
        }
    };
</script>

<div class="max-w-md mx-auto mt-16 bg-white shadow-md p-8 rounded-md">

    <div class="mb-6 space-y-2">
        <h1 class="text-3xl font-heading font-bold text-center">Forgot password</h1>
        <p class="text-xs ">
            Enter your email and we’ll send you a link to reset your password.
        </p>

    </div>

    {#if sent}
        <div class="alert alert-success mb-4">
            <div class="text-lg font-bold flex justify-start items-center gap-2">
                <Fa icon={faExclamationCircle} size="lg"/>
                <h2 class="font-heading">
                    Email sent
                </h2>
            </div>
            <ul class="list-disc list-inside px-2">
                <li>
                    <p>
                        If the email is associated with an account, a reset link has been sent.
                        Please check your inbox (and spam folder).
                    </p>

                </li>
            </ul>
        </div>
    {/if}

    <form onsubmit={submit} class="space-y-4">
        <div>
            <label for="email" class="form-control-label">Email</label>
            <input
                    id="email"
                    type="text"
                    bind:value={form.email}
                    placeholder="example@gmail.com"
                    required
                    class="form-control-field"
                    disabled={loading || sent}
            />
        </div>
        <button
                type="submit"
                class="btn btn-primary w-full"
                disabled={loading || sent}
        >
            {#if loading}
                <Spinner/>
            {:else if sent}
                Link Sent
            {:else}
                Send Reset Link
            {/if}

        </button>


    </form>

    <div class="text-sm text-center mt-4 text-gray-500">
        Don’t have an account?
        <a href="/auth/register" class="text-primary-600 font-medium hover:underline">register</a>
    </div>
</div>
