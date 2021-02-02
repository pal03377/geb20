<script>

	import { backendURL } from "./config";

	import Action from "./Action.svelte";

	import ViewInfo from "./actions/ViewInfo.svelte";
	import Attack from "./actions/Attack.svelte";
	import Coma from "./actions/Coma.svelte";
	import ZombifiedPeople from "./actions/ZombifiedPeople.svelte";
	import Message from "./actions/Message.svelte";
	import Weapons from "./actions/Weapons.svelte";

	let data = {
		day: 0, 
		people: {}, 
		attacks: [], 
		messages: []
	};
	$: console.log(data);
	async function refreshData() {
		data = await fetch(backendURL + "/data").then(resp => resp.json());
	}
	refreshData();
	setInterval(refreshData, 2000);

	let username = localStorage.getItem("username");
	let tmpUsername = "";

	async function chooseUsername() {
		let resp = await fetch(backendURL + "/register_user/" + encodeURIComponent(tmpUsername)).then(resp => resp.json());
		if (!resp) {
			alert("Diesen Namen hat schon eine andere Person gewählt :-(");
		} else {
			localStorage.setItem("username", tmpUsername);
			username = tmpUsername;
		}
	}

	const actions = [
		{ text: "Tages-Info", forRoles: "alle", component: ViewInfo }, 
		{ text: "Jmd. angreifen", forRoles: "Zombies", component: Attack }, 
		{ text: "Koma-Patienten", forRoles: "Apothekerin und Pastor", component: Coma }, 
		{ text: "Zombifiziert", forRoles: "Inspektor und Pastor", component: ZombifiedPeople }, 
		{ text: "Waffen", forRoles: "Räuber und Detektiv als Zombie", component: Weapons }, 
		{ text: "Nachricht", forRoles: "kommunikative Rollen", component: Message }, 
	];

</script>

<main>
	{#if !username || !data.people[username]}
		<input bind:value={ tmpUsername } placeholder="Dein Name">
		<button on:click={ chooseUsername }>OK</button>
	{:else}
		<p>Name: { username }</p>
		{#if data.day === 0}
			Warte auf Spielstart...
		{:else}
			<p>Tag / Nacht: { data.day }</p>
			<p>Rolle: { data.people[username].role }</p>
			<p>Waffe: { data.people[username].weapon }</p>
		{/if}
		{#each actions as action}
			<Action { ...action } { username } { data } />
		{/each}
	{/if}
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>