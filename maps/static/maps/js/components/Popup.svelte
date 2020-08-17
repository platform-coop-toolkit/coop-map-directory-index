<script>
export let feature;

import processOrganization from '../processOrganization.js';
import processIndividual from '../processIndividual.js';

import OrganizationPopup from './OrganizationPopup.svelte';
import IndividualPopup from './IndividualPopup.svelte';

</script>

{#if feature.source === 'organizations'}
<OrganizationPopup organization={processOrganization(feature)} />
{:else if feature.source === 'individuals'}
<IndividualPopup individual={processIndividual(feature)} />
{/if}
