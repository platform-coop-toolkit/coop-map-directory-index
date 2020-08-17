<script>
import { readable, get } from 'svelte/store';

import { features } from '../store.js';

import processOrganization from '../processOrganization.js';
import processIndividual from '../processIndividual.js';

import OrganizationCard from './OrganizationCard.svelte';
import IndividualCard from './IndividualCard.svelte';
</script>

<ul class="cards">
    {#each $features as feature}
        {#if feature.source === 'organizations'}
        <OrganizationCard organization={processOrganization(feature)} />
        {:else if feature.source === 'individuals'}
        <IndividualCard individual={processIndividual(feature)} />
        {/if}
    {/each}
</ul>
