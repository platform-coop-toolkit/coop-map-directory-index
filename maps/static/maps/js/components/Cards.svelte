<script>
import { readable, get } from 'svelte/store';

import { features } from '../store.js';

import OrganizationCard from './OrganizationCard.svelte';
import IndividualCard from './IndividualCard.svelte';

function processOrganization(feature) {
    const props = feature.properties;

    props.id = feature.id;

    props.type = (props.type === 'null') ? null : props.type;

    if (props.country !== '') {
        props.country = JSON.parse(props.country);
    }

    props.city = props.city.trim();
    props.state = props.state.trim();

    props.categories = JSON.parse(props.categories);
    props.languages = JSON.parse(props.languages);
    props.sectors = JSON.parse(props.sectors);
    props.socialnetworks = JSON.parse(props.socialnetworks);
    props.tools = JSON.parse(props.tools);

    return props;
}

function processIndividual(feature) {
    const props = feature.properties;

    props.id = feature.id;

    props.name = `${props.first_name} ${props.last_name}`;

    props.roles = JSON.parse(props.roles);

    if (props.country !== '') {
        props.country = JSON.parse(props.country);
    }

    props.city = props.city.trim();
    props.state = props.state.trim();

    props.languages = JSON.parse(props.languages);

    return props;
}
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
