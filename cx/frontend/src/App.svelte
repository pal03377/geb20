<script>

	import { backendURL } from "./config";

	import Action from "./Action.svelte";

	import ViewInfo from "./actions/ViewInfo.svelte";
	import Attack from "./actions/Attack.svelte";
	import Coma from "./actions/Coma.svelte";
	import ZombifiedPeople from "./actions/ZombifiedPeople.svelte";
	import Roles from "./actions/Roles.svelte";
	import Weapons from "./actions/Weapons.svelte";
	import Protect from "./actions/Protect.svelte";
	import Message from "./actions/Message.svelte";

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
	let tmpUsername = username || "";

	let loading = false;

	async function chooseUsername() {
		loading = true;
		let resp = await fetch(backendURL + "/register_user/" + encodeURIComponent(tmpUsername)).then(resp => resp.json());
		loading = false;
		if (!resp) {
			alert("Diesen Namen hat schon eine andere Person gewählt :-(");
		} else {
			localStorage.setItem("username", tmpUsername);
			username = tmpUsername;
		}
	}

	const actions = [
		{ text: "Tages-Info", forRoles: "alle", component: ViewInfo }, 
		{ text: "Angreifen", forRoles: "Zombies", component: Attack }, 
		{ text: "Koma-Patienten", forRoles: "Apothekerin und Pastor", component: Coma }, 
		{ text: "Zombifiziert", forRoles: "Inspektor und Pastor", component: ZombifiedPeople }, 
		{ text: "Rollen", forRoles: "Detektiv", component: Roles }, 
		{ text: "Waffen", forRoles: "Räuber, Erfinder und Detektiv als Zombie", component: Weapons }, 
		{ text: "Beschützen", forRoles: "Pastor", component: Protect }, 
		{ text: "Nachricht", forRoles: "kommunikative Rollen", component: Message }, 
	];

</script>

<main>
	{#if loading}
		Einen Moment...
	{:else}
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
				{#each actions as action}
					<Action { ...action } { username } { data } />
				{/each}
			{/if}
		{/if}
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