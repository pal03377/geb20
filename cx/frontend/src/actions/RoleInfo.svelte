<script>

    import { onMount } from "svelte";

    import { backendURL } from "../config.js";

    export let username;
    export let data;

    let showRole = data.people[username].role;

    let allRoles = [];
    onMount(async () => {
        allRoles = await fetch(backendURL + "/all_roles").then(resp => resp.json());
    });

</script>


<h1>Rollen-Info</h1>
<p>
    {#if data.people[username].role === showRole}
        Informations-Karte zu deiner Rolle:
    {:else}
        Informations-Karte zur Rolle "{ showRole }":
    {/if}
</p>
<img src="img/roles/{ showRole }.jpg" alt={ showRole } >

<p class="description">
    <i>Andere Rollen: </i>
    {#each allRoles as role}
        <button class:selected={ showRole === role } class:me={ data.people[username].role === role } on:click={ () => showRole = role }>
            { role }
        </button>
    {/each}
</p>


<style>

    img {
        width: 100%;
    }

    button {
        border: none;
        text-decoration: underline;
    }

    button.selected {
        font-weight: bold;
    }
    button.me {
        color: red;
    }

</style>