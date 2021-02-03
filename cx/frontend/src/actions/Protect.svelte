<script>

    import { backendURL } from "../config.js";

    export let username;
    export let data;

    let loading = false;

    async function protect(toProtect) {
        loading = true;
        try {
            alert(await fetch(backendURL + "/protect/" + encodeURIComponent(username) + "/" + encodeURIComponent(toProtect)).then(resp => resp.text()));
        } catch (e) {
            alert("Das hat nicht geklappt :-( " + e);
        }
        loading = false;
    }

</script>

<h1>Jemanden beschützen</h1>
<p class="description">
    Der Pastor kann in der dritten Nacht bis zu 5 Personen beschützen, die dann nicht zu Zombies werden können. 
    Ist ein Zombie unter den Beschützten, opfert sich der Pastor.<br>
    Der Gärtner wird jede 2. Nacht automatisch beschützt.
</p>
{#if loading}
    <p>Einen Moment...</p>
{:else}
    <ul>
        {#each Object.keys(data.people) as toProtect}
        <li>{ toProtect } <button on:click={ () => protect(toProtect) }>Beschützen</button></li>
        {/each}
    </ul>
{/if}