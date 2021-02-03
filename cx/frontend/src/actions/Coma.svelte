<script>

    import { backendURL } from "../config.js";
    import getNumberOfAttacks from "./attacks.js";

    export let username;
    export let data;

    let inComa = [];
    $: {
        inComa = [];
        for (let usr of Object.keys(data.people)) {
            let numberOfAttacks = getNumberOfAttacks(usr, data);
            if (numberOfAttacks > 0) {
                if (data.people[usr].weapon === numberOfAttacks) {
                    inComa.push(usr);
                }
            }
        }
        inComa = inComa.filter(p => data.protects.indexOf(p) < 0);
    }

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


<h1>Koma-Patienten</h1>
<p class="description">
    Koma-Patienten sind diejenigen Leute, die genauso oft angetippt wurden, wie ihre Waffenstärke anzeigt. 
    Die Apothekerin kann pro Nacht bis zu eine Person aus dem Koma befreien. Geschützte Personen werden nicht angezeigt.</p>

{#if getNumberOfAttacks(username, data) >= data.people[username].weapon}
    <b style="color: red;">Du befindest dich selbst im Koma oder bist überwältigt und kannst daher keine anderen Koma-Patienten sehen!</b><br>
{:else}
    {#if loading}
        <p>Einen Moment...</p>
    {:else}
        {#if inComa.length > 0}
            <ul>
                {#each inComa as toHeal}
                <li>{ toHeal } <button on:click={ () => protect(toHeal) }>Retten</button></li>
                {/each}
            </ul>
            {#if inComa.length > 2}
            Achtung: Die Apothekerin kann pro Nacht nur eine der Personen im Koma retten!
            {/if}
        {:else}
            <p>Es befindet sich niemand im Koma.</p>
        {/if}
    {/if}
{/if}