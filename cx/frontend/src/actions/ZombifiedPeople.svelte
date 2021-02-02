<script>

    import getNumberOfAttacks from "./attacks.js";

    export let username;
    export let data;

    let zombified = [];
    $: {
        zombified = [];
        for (let usr of Object.keys(data.people)) {
            if (data.people[usr].weapon < getNumberOfAttacks(usr, data)) {
                zombified.push(usr);
            }
        }
        zombified = zombified.filter(p => data.protects.indexOf(p) < 0);
    }

</script>


<h1>Zombifizierte Personen</h1>
<p>Zombifizierte Personen sind diejenigen Leute, die öfter angetippt wurden, als ihre Waffenstärke anzeigt. Geschützte Personen werden nicht angezeigt.</p>

{#if zombified.length > 0}
    <ul>
        {#each zombified as zombifiedPerson}
        <li>{ zombifiedPerson }</li>
        {/each}
    </ul>
    <p>Diese Personen sind (außer evtl. durch den Pastor) nicht zu retten. Sie werden nächste Runde zu Zombies.</p>
{:else}
    <p>Es wurde niemand zombifiziert.</p>
{/if}