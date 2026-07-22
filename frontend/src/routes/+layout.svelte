<script lang="ts">
  import { page } from '$app/stores';
  import AppHeader from '$lib/components/AppHeader.svelte';
  import '../app.css';
  export let data;
  $: isAuthPage = ['/login', '/register'].includes($page.url.pathname);
</script>

{#if !isAuthPage}<AppHeader user={data.user ?? null} />{/if}
<slot />
