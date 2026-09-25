<script>
    import {authState} from "$lib/states/auth.svelte.js";
    import Fa from "svelte-fa";
    import {faBell, faFloppyDisk, faUser} from "@fortawesome/free-solid-svg-icons";
    import {updateAccount} from "$lib/api/account.js";
    import Toast from "$lib/toast.js";
    import Spinner from "$lib/components/Spinner.svelte";

    let user = $state({
        email: authState.user.email,
        first_name: authState.user.first_name,
        last_name: authState.user.last_name,
        phone_number: authState.user.phone_number,
    });
    let loading = $state({
        account: false,
        notification: false,
    })


    const handleSubmitAccount = async (e) => {
        e.preventDefault()

        try {
            loading = {...loading, account: true}
            await updateAccount(user)
            Toast.success("Account information updated successfully.")
        } catch (e) {
            return;
        } finally {
            loading = {...loading, account: false}
        }


    }

</script>
<div class="container space-y-4 ">
    <section class="space-y-2">
        <div class="card bg-gray-100 text-slate-900 shadow-none flex justify-start items-center gap-2">
            <Fa icon={faUser} size="lg"/>
            <h2 class="text-2xl font-heading font-bold">Account</h2>
        </div>
        <form class="space-y-2" onsubmit={handleSubmitAccount}>
            <div class="flex flex-col md:flex-row gap-2">
                <div class="w-full">
                    <label class="form-control-label" for="email-input">
                        Email
                    </label>
                    <input type="email" id="email-input" name="email" disabled class="form-control-field"
                           placeholder="example@gmail.com"
                           bind:value={user.email}>
                </div>
                <div class="w-full">
                    <label class="form-control-label" for="phone_number-input">
                        Phone number
                    </label>
                    <input type="tel" id="phone_number-input" name="phone_number" class="form-control-field"
                           placeholder="+1 212 5552 368"
                           bind:value={user.phone_number}>
                </div>
            </div>

            <div class="flex flex-col md:flex-row gap-2">
                <div class="w-full">
                    <label class="form-control-label" for="first_name-input">
                        First Name
                    </label>
                    <input type="text" id="first_name-input" name="first_name" class="form-control-field"
                           placeholder="Enter your first name"
                           bind:value={user.first_name}>
                </div>
                <div class="w-full">
                    <label class="form-control-label" for="last_name-input">
                        Last Name
                    </label>
                    <input type="text" id="last_name-input" name="last_name" class="form-control-field"
                           placeholder="Enter your last name"
                           bind:value={user.last_name}>
                </div>
            </div>

            <button type="submit" class="btn btn-primary">
                {#if loading.account}
                    <Spinner size="xs"/>
                    Saving...
                {:else }
                    <Fa icon={faFloppyDisk} size="lg"/>
                    Save
                {/if}
            </button>
        </form>
    </section>

    <section>
        <div class="card bg-gray-100 text-slate-900 shadow-none flex justify-start items-center gap-2">
            <Fa icon={faBell} size="lg"/>
            <h2 class="text-2xl font-heading font-bold">Notification</h2>
        </div>
    </section>
</div>
