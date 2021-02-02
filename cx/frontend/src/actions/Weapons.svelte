<script>

    import { backendURL } from "../config.js";

    export let username;
    export let data;

    let loading = false;

    async function switchWeapons(switchWith) {
        loading = true;
        try {
            alert(await fetch(backendURL + "/switch_weapons/" + encodeURIComponent(username) + "/" + encodeURIComponent(switchWith)).then(resp => resp.text()));
        } catch (e) {
            alert("Das hat nicht geklappt :-( " + e);
        }
        loading = false;
    }

</script>

<h1>Waffen</h1>
<p>Der Räuber kann jede Nacht zwei Waffenkarten ansehen und mit seiner eigenen tauschen. Ein Zombie-Detektiv kann jede Nacht eine anschauen.</p>
{#if loading}
    <p>Einen Moment...</p>
{:else}
    <ul>
        {#each Object.keys(data.people) as usr}
        <li>
            { usr } 
            <button on:click={ () => alert(usr + " hat Waffenstärke " + data.people[usr].weapon) }>Ansehen</button>
            <button on:click={ () => switchWeapons(usr) }>Tauschen</button>
        </li>
        {/each}
    </ul>
{/if}