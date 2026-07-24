<script lang="ts">
  import { page } from '$app/stores';
  import BrandLogo from '$lib/components/BrandLogo.svelte';
  export let user: { email: string } | null = null;
  let open = false;
  const links = [
    { href: '/pymes', label: 'Mapa' },
    { href: '/diagnostico', label: 'Diagnóstico' },
    { href: '/antenaTecnologica', label: 'Antena' }
  ];
</script>

<header class="app-header">
  <BrandLogo />
  <button class="mobile-menu" aria-label="Abrir navegación" on:click={() => open = !open}>☰</button>
  <nav class:open aria-label="Navegación principal">
    {#each links as link}
      <a class:active={$page.url.pathname.startsWith(link.href)} href={link.href}>{link.label}</a>
    {/each}
    {#if user}
      <span class="account" title={user.email}>{user.email}</span>
      <form method="POST" action="/logout"><button type="submit">Salir</button></form>
    {/if}
  </nav>
</header>

<style>
  .app-header { height:72px; padding:0 3.5vw; display:flex; align-items:center; gap:36px; background:#fff; border-bottom:1px solid #dce2e8; box-shadow:0 2px 8px #0a203a12; position:relative; z-index:1000; }
  nav { display:flex; align-items:center; gap:8px; margin-left:auto; }
  nav a, nav button { border:0; background:transparent; color:#5d6f85; font-weight:650; padding:10px 13px; border-radius:8px; }
  nav a:hover, nav a.active { color:var(--navy); background:#f1f5f7; }
  nav a.active { box-shadow:inset 0 -2px var(--lime); }
  .account { max-width:190px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; margin-left:12px; color:#718198; font-size:.8rem; }
  .mobile-menu { display:none; margin-left:auto; border:0; background:var(--navy); color:white; border-radius:8px; width:40px; height:40px; }
  @media(max-width:760px){
    .app-header{height:62px;padding:0 16px}.mobile-menu{display:block}nav{display:none;position:absolute;top:62px;left:0;right:0;background:white;padding:12px;box-shadow:0 10px 20px #0a203a22;align-items:stretch;flex-direction:column}nav.open{display:flex}.account{margin:8px 12px}nav form,nav button{width:100%}
  }
</style>
