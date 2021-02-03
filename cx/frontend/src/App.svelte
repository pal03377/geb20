<script>

	import { backendURL } from "./config.js";

	import Action from "./Action.svelte";

	import RoleInfo from "./actions/RoleInfo.svelte";
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
		{ text: "Rollen-Info", forRoles: true, component: RoleInfo }, 
		{ text: "Tages-Info", forRoles: true, component: ViewInfo }, 
		{ text: "Angreifen", forRoles: ["Zombie"], maybeRelevant: true, component: Attack }, 
		{ text: "Koma", forRoles: ["Apothekerin", "Pastor"], component: Coma }, 
		{ text: "Zombifiziert", forRoles: ["Inspektor", "Pastor"], component: ZombifiedPeople }, 
		{ text: "Rollen", forRoles: ["Detektiv"], component: Roles }, 
		{ text: "Waffen", forRoles: ["Raeuber", "Erfinder", "Detektiv"], component: Weapons }, 
		{ text: "Beschützen", forRoles: ["Pastor"], component: Protect }, 
		{ text: "Nachricht", forRoles: ["Lehrerin"], component: Message }, 
	];

</script>

<main>
	{#if loading}
		Einen Moment...
	{:else}
		{#if !username || !data.people[username]}
			<h1>Citizen X</h1>
			<span>Wie heißt du? </span>
			<input bind:value={ tmpUsername } placeholder="Dein Name">
			<button on:click={ chooseUsername }>OK</button>
		{:else}
			<p class="name">{ username }</p>
			{#if data.day === 0}
				Warte auf Spielstart...
			{:else}
				<div class="infoBlock">
					<div class="card currentDay">
						<h2>Tag / Nacht</h2>
						<span>{ data.day }</span>
					</div>
					<div class="card role">
						<h2>Rolle</h2>
						<span>{ data.people[username].role }</span>
					</div>
					<div class="card weapon">
						<h2>Waffe</h2>
						<span>{ data.people[username].weapon }</span>
					</div>
				</div>
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

	.name {
		position: absolute;
		top: 8px;
		right: 16px;
	}

	.infoBlock {
		display: flex;
		justify-content: center;
		margin-bottom: 16px;
	}

	.infoBlock>.card {
		margin: 0 16px;
		text-align: left;

	}

	.infoBlock>.card h2 {
		margin: 0;
		font-weight: normal;
		font-size: 18px;
	}

	.infoBlock>.card span {
		margin: 0;
		font-weight: bold;
		font-size: 22px;
	}

</style>