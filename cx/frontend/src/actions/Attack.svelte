<script>

    import { backendURL } from "../config";

    export let username;
    export let data;

    let loading = false;

    async function attack(toAttack) {
        loading = true;
        try {
            alert(await fetch(backendURL + "/attack/" + username + "/" + toAttack).then(resp => resp.text()));
        } catch (e) {
            alert("Das hat nicht geklappt :-( " + e);
        }
        loading = false;
    }

</script>

<h1>Jemanden angreifen</h1>
{#if loading}
    <p>Einen Moment...</p>
{:else}
    <ul>
        {#each Object.keys(data.people) as toAttack}
        <li>{ toAttack } <button on:click={ () => attack(toAttack) }>Angriff</button></li>
        {/each}
    </ul>
{/if}