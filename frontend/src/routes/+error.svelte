<script>
	import { page } from '$app/state';

	let status = page.status;
	let message = page.error?.message || 'Something went wrong.';
	let title = 'Error';
	let emoji = '💥';

	if (status === 404) {
		title = "Page Not Found";
		emoji = "🧭";
		message = message || "We couldn't find the page you're looking for.";
	} else if (status === 500) {
		title = "Server Error";
		emoji = "🔥";
		message = message || "Oops! Something went wrong on our side.";
	} else if (status === 403) {
		title = "Access Denied";
		emoji = "⛔";
		message = message || "You don’t have permission to access this page.";
	} else if (status === 400) {
		title = "Bad Request";
		emoji = "⚠️";
		message = message || "There was a problem with your request.";
	}
</script>

<div class="min-h-screen flex flex-col justify-center items-center px-6 text-center bg-white text-slate-800">
	<div class="text-7xl sm:text-9xl">{emoji}</div>
	<h1 class="text-4xl font-bold mt-4">{status} – {title}</h1>
	<p class="mt-2 text-lg text-slate-600 max-w-xl">{message}</p>

	<a href="/" class="btn btn-primary mt-6">Back to Home</a>
</div>
