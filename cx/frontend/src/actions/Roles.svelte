<script>
    
    export let username;
    export let data;

</script>

<h1>Rollen</h1>
<p>Der Detektiv kann jede Nacht die ursprüngliche Rolle einer Person sehen..</p>
<ul>
    {#each Object.keys(data.people) as usr}
    <li>
        { usr } 
        <button on:click={ () => alert(usr + " ist " + data.people[usr].role) }>Ansehen</button>
    </li>
    {/each}
</ul>