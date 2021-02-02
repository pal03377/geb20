<script>

    export let open = false;

</script>


<div class="dialog" class:open>

    <div class="bg" on:click={ () => open = false }></div>
    <div class="popup">
        <slot />
        <button on:click={ () => open = false }>schließen</button>
    </div>

</div>


<style>

    .dialog {
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        display: none;
    }

    .dialog.open {
        display: block;
    }

    .popup {
        position: absolute;
        width: 300px;
        height: 100%;
        margin: 0 auto;
        left: 0;
        right: 0;
        background-color: white;
    }

    .bg {
        position: absolute;
        width: 100%;;
        height: 100%;
        left: 0;
        top: 0;
        background-color: black;
        opacity: .7;
    }

</style>