<script>

    import Dialog from "./Dialog.svelte";

    export let username;
    export let data;

    export let text;
    export let component;
    export let forRoles;

    export let maybeRelevant = false;

    let open = false;

</script>

{#if username && data}
    <Dialog bind:open>
        <svelte:component this={ component } { username } { data } />
    </Dialog>
{/if}

<div class="action" class:relevant={ forRoles === true || forRoles.indexOf(data.people[username].role) >= 0 } class:maybeRelevant>
    <button on:click={ () => open = true }>{ text }</button>
    {#if forRoles === true}
        (alle)
    {:else}
        ({ forRoles.join(", ") })
    {/if}
</div>

<style>

    .action {
        width: 120px;
        height: 140px;
        padding: 6px;
        margin: 4px 2px;
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        border: 1px solid grey;
        border-radius: 6px;
    }

    .action.relevant {
        background: #D38312;
        background: linear-gradient(45deg, #A83279, #D38312);
    }

    .action.maybeRelevant {
        background: #485563;
        background: linear-gradient(45deg, #29323c, #485563);
    }

</style>