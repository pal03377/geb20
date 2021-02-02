<script>

    import getNumberOfAttacks from "./attacks.js";

    export let username;
    export let data;

    let numberOfAttacks = 0;
    $: numberOfAttacks = getNumberOfAttacks(username, data);

</script>


<h1>Tages-Info</h1>
<p>
    {#if numberOfAttacks <= 0}
    Du wurdest nicht attackiert.
    {:else}
    <b style="color: red;">Du wurdest { numberOfAttacks } mal attackiert!</b>
    {/if}
</p>
{#if data.messages[username]}
Außerdem wurden dir folgende anonyme Nachrichten gesendet:
<code>{ data.messages[username] }</code>
{/if}