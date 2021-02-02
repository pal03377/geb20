<script>

    import getNumberOfAttacks from "./attacks.js";

    export let username;
    export let data;

    let inComa = [];
    $: {
        inComa = [];
        for (let usr of Object.keys(data.people)) {
            if (data.people[usr].weapon === getNumberOfAttacks(usr, data)) {
                inComa.push(usr);
            }
        }
    }

</script>


<h1>Koma-Patienten</h1>
<p>Koma-Patienten sind diejenigen Leute, die genauso oft angetippt wurden, wie ihre Waffenstärke anzeigt. Die Apothekerin kann pro Nacht bis zu eine Person aus dem Koma befreien.</p>

{#if getNumberOfAttacks(username, data) >= data.people[username].weapon}
    <b style="color: red;">Du befindest dich selbst im Koma oder bist überwältigt und kannst daher keine anderen Koma-Patienten sehen!</b>
{:else}
    {#if inComa.length > 0}
        <ul>
            {#each inComa as toHeal}
            <li>{ toHeal }</li>
            {/each}
        </ul>
        <p>Die Apothekerin rettet, indem sie eine anonyme Nachricht an die zu heilende Person schreibt (z.B. mit Text <code>Apothekerin hat gerettet</code>)</p>
        {#if inComa.length > 2}
        Achtung: Die Apothekerin kann pro Nacht nur eine der Personen im Koma retten!
        {/if}
    {:else}
        Es befindet sich niemand im Koma.
    {/if}
{/if}