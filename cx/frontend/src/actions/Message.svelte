<script>

    import { backendURL } from "../config.js";

    export let username;
    export let data;

    let loading = false;

    async function sendMessage(toSendTo) {
        loading = true;
        let message = prompt("Nachricht an " + toSendTo + ":");
        try {
            alert(await fetch(backendURL + "/send/" + encodeURIComponent(toSendTo) + "/" + encodeURIComponent(message)).then(resp => resp.text()));
        } catch (e) {
            alert("Das hat nicht geklappt :-( " + e);
        }
        loading = false;
    }

</script>

<h1>Anonyme Nachricht</h1>
<p>Sende eine anonyme Nachricht an eine andere Person, z.B. wenn du als Apothekerin heilst.</p>
{#if loading}
    <p>Einen Moment...</p>
{:else}
    <ul>
        {#each Object.keys(data.people) as toSendTo}
        <li>{ toSendTo } <button on:click={ () => sendMessage(toSendTo) }>Schreiben</button></li>
        {/each}
    </ul>
{/if}