<script>

    import Dialog from "./Dialog.svelte";

    export let username;
    export let data;

    export let text;
    export let component;
    export let forRoles;

    let open = false;

</script>

{#if username && data}
    <Dialog bind:open>
        <svelte:component this={ component } { username } { data } />
    </Dialog>
{/if}

<div class="action">
    <button on:click={ () => open = true }>{ text }</button>
    (für { forRoles })
</div>

<style>

    .action {
        width: fit-content;
        padding: 6px;
        display: inline-flex;
        flex-direction: column;
        align-items: center;
        border: 1px solid grey;
        border-radius: 6px;
    }

</style>