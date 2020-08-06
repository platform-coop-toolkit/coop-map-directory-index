<script>
import { readable, get } from 'svelte/store';

import Card from './Card.svelte';

import { features } from '../store.js';
</script>

<ul class="cards">
    {#each $features as feature}
    <Card organization={feature} />
    {/each}
</ul>
