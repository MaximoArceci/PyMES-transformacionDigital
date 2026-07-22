<script lang="ts">
  import { enhance } from '$app/forms';
  export let form;
  let submitting = false;
</script>

<svelte:head><title>Iniciar sesión · PyMEs</title></svelte:head>
<main class="auth-page">
  <section class="auth-art" aria-hidden="true"><div class="glow"></div><div class="art-copy"><span>PYMES</span><h1>Información que impulsa empresas.</h1></div></section>
  <section class="auth-form-wrap">
    <form method="POST" use:enhance={() => { submitting = true; return async ({ update }) => { await update(); submitting = false; }; }}>
      <div class="auth-logo"><span>P</span> PyMEs</div>
      <h1>Bienvenido de vuelta</h1>
      <p>Iniciá sesión en tu cuenta</p>
      {#if form?.error}<div class="form-error" role="alert">{form.error}</div>{/if}
      <label><span>Correo electrónico</span><div class="input-wrap"><i>✉</i><input name="email" type="email" autocomplete="email" value={form?.email ?? ''} required /></div></label>
      <label><span>Contraseña</span><div class="input-wrap"><i>♙</i><input name="password" type="password" autocomplete="current-password" required /></div></label>
      <button class="login-button" type="submit" disabled={submitting}>{submitting ? 'Ingresando…' : 'Iniciar sesión'} <b>→</b></button>
      <p class="account-link">¿No tenés una cuenta? <a href="/register">Crear cuenta</a></p>
    </form>
  </section>
</main>

<style>
  .auth-page{min-height:100vh;display:grid;grid-template-columns:1fr 1fr;background:#fff}.auth-art{position:relative;overflow:hidden;background:linear-gradient(135deg,#1d3d2d 0%,#0a203a 60%,#07182c 100%)}.glow{position:absolute;width:70%;height:70%;left:-20%;bottom:-20%;background:#77a53555;filter:blur(100px);border-radius:50%}.art-copy{position:absolute;left:9%;bottom:9%;max-width:380px;color:white}.art-copy span{color:var(--lime);font-weight:800;letter-spacing:.18em}.art-copy h1{font-size:2.5rem;line-height:1.06;margin:14px 0}.auth-form-wrap{display:grid;place-items:center;padding:50px}.auth-form-wrap form{width:min(100%,440px)}.auth-logo{display:none;font-weight:850;margin-bottom:48px}.auth-logo span{background:var(--lime);padding:7px 11px;border-radius:8px}.auth-form-wrap h1{margin:0;color:var(--navy);font-size:1.5rem}.auth-form-wrap>form>p{margin:6px 0 32px;color:#5d6f85}.form-error{background:#fff1f0;border:1px solid #f7b4ad;color:#a1261c;padding:12px;border-radius:9px;margin-bottom:18px}label{display:block;margin:0 0 18px}label>span{display:block;color:#8294aa;text-transform:uppercase;font-size:.75rem;font-weight:800;margin-bottom:7px}.input-wrap{height:46px;border:1px solid var(--border);border-radius:10px;display:flex;align-items:center;padding:0 12px;box-shadow:0 2px 4px #0a203a12}.input-wrap:focus-within{outline:3px solid #0a203a12;border-color:var(--navy)}.input-wrap i{font-style:normal;width:26px}.input-wrap input{border:0;outline:0;width:100%;height:100%;background:transparent}.login-button{width:100%;height:48px;border:0;border-radius:11px;background:#d9ef82;color:var(--navy);font-weight:800;display:flex;align-items:center;justify-content:center;gap:20px;margin-top:8px}.login-button:disabled{opacity:.65}.account-link{text-align:center!important;font-size:.8rem!important;color:var(--navy)!important;margin-top:20px!important}.account-link a{color:var(--lime-dark);font-weight:700}@media(max-width:760px){.auth-page{grid-template-columns:1fr}.auth-art{display:none}.auth-form-wrap{padding:28px 22px}.auth-logo{display:block}}
</style>
