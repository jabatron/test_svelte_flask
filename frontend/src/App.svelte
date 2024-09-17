<script>
    import Login from './components/Login.svelte';

    let login = false;

    $: data = ''
    async function flask_protected() {
        const response = await fetch('http://0.0.0.0:8080/protected', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
        });
        data = await response.json();
    }
</script>

<main>
  {#if !login}
  <h1>Login</h1>
  <div>
    <Login bind:isLogin={login} />
    <button on:click={flask_protected}>Protected</button>
  </div>
  {:else}
  <h1>Protected</h1>
  <div>
    <p>This is a protected route. You need to be logged in to access it.</p>
    <button on:click={flask_protected}>Protected</button>
    { data.message }
  </div>
  {/if}
</main>

<style>

</style>
