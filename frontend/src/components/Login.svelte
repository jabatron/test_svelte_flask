<script>
    let email = '';
    let password = '';
    export let isLogin = false;

    async function login() {
        const response = await fetch('http://0.0.0.0:8080/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        console.log('Login response', response);
        const data = await response.json();

        if (response.ok) {
            isLogin = true;
        } else {
            alert('Login failed');
        }
    }
</script>
<form on:submit|preventDefault={login}>
    <input type="email" bind:value={email} placeholder="Email" required />
    <input type="password" bind:value={password} placeholder="Password" required />
    <button type="submit">Login</button>
</form>
