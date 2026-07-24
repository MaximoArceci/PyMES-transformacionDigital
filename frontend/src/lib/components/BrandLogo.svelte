<script lang="ts">
  export let href = '/pymes';
  export let variant: 'header' | 'auth' | 'hero' = 'header';
</script>

<a class:header={variant === 'header'} class:auth={variant === 'auth'} class:hero={variant === 'hero'} {href} aria-label="Tecnológica del Sur">
  <img src="/logo.png" alt="Tecnológica del Sur" />
</a>

<style>
  a { display:inline-flex; align-items:center; flex:0 0 auto; }
  img { display:block; width:100%; height:auto; object-fit:contain; }
  .header { width:132px; }
  .auth { width:min(230px,70vw); }
  .hero { width:min(290px,70%); }
  @media(max-width:760px) {
    .header { width:108px; }
  }
</style>
