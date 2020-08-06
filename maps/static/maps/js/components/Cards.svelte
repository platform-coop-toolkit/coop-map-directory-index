<script>
import Card from './Card.svelte';

export let features;
</script>

<ul class="cards">
    {#each features as feature}
    <Card organization={feature} />
    {/each}
</ul>
