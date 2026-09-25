import tailwindcss from '@tailwindcss/vite';
import {sveltekit} from '@sveltejs/kit/vite';
import {defineConfig} from 'vite';
import {enhancedImages} from '@sveltejs/enhanced-img';
import devtoolsJson from 'vite-plugin-devtools-json';

export default defineConfig({
    plugins: [
        tailwindcss(),
        enhancedImages(),
        sveltekit(),
        devtoolsJson(),
    ]
});
