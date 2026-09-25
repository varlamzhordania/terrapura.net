<script>
  import { page } from "$app/state";
  import { goto } from "$app/navigation";
  import Toast from "$lib/toast.js";
  import { confirmPasswordReset } from "$lib/api/account.js";

  // URL params
  let uidb64 = $state(page.params.uidb64);
  let token = $state(page.params.token);

  let loading = $state(false);
  let form = $state({
    new_password: "",
    confirm_password: ""
  });

  const validate = () => {
    if (!form.new_password || !form.confirm_password) {
      Toast.error("Please fill in both fields.");
      return false;
    }
    if (form.new_password !== form.confirm_password) {
      Toast.error("Passwords do not match.");
      return false;
    }
    if (form.new_password.length < 8) {
      Toast.error("Password must be at least 8 characters.");
      return false;
    }
    return true;
  };

  const submit = async () => {
    if (!validate()) return;
    loading = true;
    try {
      await confirmPasswordReset({
        uidb64,
        token,
        new_password: form.new_password
      });
      Toast.success("Password reset successfully. Please sign in.");
      await goto("/auth/login");
    } catch (e) {
      // Show detailed server-side validation if present
      const msg =
        e?.data?.detail ||
        (Array.isArray(e?.data?.new_password) ? e.data.new_password.join(", ") : null) ||
        "Invalid or expired link.";
      Toast.error(msg);
    } finally {
      loading = false;
    }
  };
</script>

<div class="min-h-[60vh] flex items-center justify-center px-4">
  <div class="w-full max-w-md bg-white shadow rounded-xl p-6 space-y-5">
    <h1 class="text-2xl font-bold">Set a new password</h1>
    <p class="text-sm text-gray-600">
      Choose a strong password you don’t use elsewhere.
    </p>

    <div class="space-y-3">
      <label class="block text-sm font-medium text-gray-700">New password</label>
      <input
        type="password"
        class="input input-bordered w-full"
        bind:value={form.new_password}
        placeholder="••••••••"
        disabled={loading}
      />
    </div>

    <div class="space-y-3">
      <label class="block text-sm font-medium text-gray-700">Confirm new password</label>
      <input
        type="password"
        class="input input-bordered w-full"
        bind:value={form.confirm_password}
        placeholder="••••••••"
        disabled={loading}
      />
    </div>

    <!-- Optional: simple strength hint -->
    {#if form.new_password}
      <p class="text-xs text-gray-500">
        Use 8+ chars, include letters, numbers, and symbols.
      </p>
    {/if}

    <button
      class="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium disabled:opacity-60"
      onclick={submit}
      disabled={loading}
    >
      {loading ? "Updating..." : "Reset Password"}
    </button>

    <p class="text-xs text-gray-500 text-center">
      If this link is invalid or expired, request a new one on the
      <a href="/auth/forgot-password" class="text-blue-600 hover:underline">Forgot Password</a> page.
    </p>
  </div>
</div>
