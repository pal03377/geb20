<script>

    import { backendURL } from "../config.js";

    export let username;
    export let data;

    let loading = false;

    async function attack(toAttack) {
        loading = true;
        try {
            alert(await fetch(backendURL + "/attack/" + encodeURIComponent(username) + "/" + encodeURIComponent(toAttack)).then(resp => resp.text()));
        } catch (e) {
            alert("Das hat nicht geklappt :-( " + e);
        }
        loading = false;
    }

</script>

<h1>Jemanden angreifen</h1>
<p class="description">
    Zombies (und der Schlafwandler) können nachts Personen angreifen. Jeder darf pro Nacht nur eine Person einmal angreifen (Ausnahme: Gärtner).<br>
    Leute, die genauso oft angegriffen werden, wie ihre Waffenstärke angibt, fallen ins Koma und können von der Apothekerin gerettet werden (oder werden ansonsten zu Zombies).<br>
    Leute, die öfter angegriffen werden, als ihre Waffenstärke angibt, werden in der nächsten Nacht garantiert zu Zombies und müssen den Zombies ihre alte Rolle vermitteln.
</p>
{#if loading}
    <p>Einen Moment...</p>
{:else}
    <ul>
        {#each Object.keys(data.people) as toAttack}
        <li>{ toAttack } <button on:click={ () => attack(toAttack) }>Angriff</button></li>
        {/each}
    </ul>
{/if}