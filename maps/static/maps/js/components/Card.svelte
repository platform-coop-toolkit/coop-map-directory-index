<script>
import Icon from './Icon.svelte';

export let organization;

const type = (organization.properties.type === 'null') ? null : {
    name: organization.properties.type
};

if (type) {
    switch (type.name) {
        case 'Cooperative':
            type.icon = 'cooperative';
        break;
    case 'Potential cooperative':
        type.icon = 'converting';
        break;
    case 'Shared platform':
        type.icon = 'shared-platform';
        break;
    case 'Supporting organization':
        type.icon = 'support-organization';
        break;
    }
}

const categories = organization.properties.categories.replace('[', '').replace(']', '').replace(/","/g, ',').replace(/"/g, '').split(',').filter((el) => {
      return el != '';
});

const sectors = organization.properties.sectors.replace('[', '').replace(']', '').replace(/","/g, ',').replace(/"/g, '').split(',').filter((el) => {
      return el != '';
});

console.log(organization);
</script>

<li class="card__wrapper">
    <div class="card card--organization">
        <header>
            <h3 class="card__title">
                <a class="card__link" href="/organizations/{organization.id}">{organization.properties.name}</a>
            </h3>
        </header>
        {#if type}
        <p class="card__meta card__type">
            <span class="screen-reader-text">type: </span>
            {#if type.icon}<Icon name={type.icon} />{/if}
            {type.name}
        </p>
        {/if}
        <div class="card__aside">
            {#if organization.properties.city || organization.properties.state || organization.properties.country}
            <div class="card__meta">
                <span class="card__locality">
                    <span class="screen-reader-text">location: </span>
                    <Icon name={'location'} />
                        {#if organization.properties.city}{organization.properties.city}, {/if}
                        {#if organization.properties.state}{organization.properties.state}{#if organization.properties.country},{/if} {/if}
                        {#if organization.properties.country}{organization.properties.country}{/if}
                </span>
            </div>
            {/if}
            {#if organization.working_languages}
            <div class="card__meta">
                <span class="card__languages">
                    <span class="screen-reader-text">working languages: </span>
                    <Icon name={'language-small'} />
                    {#each organization.languages as language}{language}{/each}
                </span>
            </div>
            {/if}
            {#if categories.length > 0}
            <div class="card__meta">
                <span class="card__subtypes">
                    <span class="screen-reader-text">{#if type == 'Cooperative'}cooperative{:else}organization{/if} types: </span>
                    <Icon name={'coop-type'} />
                    {#each categories as type, index}
                        {type}{#if index + 1 < categories.length},&nbsp;{/if}
                    {/each}
                </span>
            </div>
            {/if}
            {#if sectors.length > 0}
            <div class="card__meta">
                <span class="card__subtypes">
                    <span class="screen-reader-text">sectors: </span>
                    <Icon name={'sector-small'} />
                    {#each sectors as sector, index}
                        {sector}{#if index + 1 < sectors.length},&nbsp;{/if}
                    {/each}
                </span>
            </div>
            {/if}
        </div>
    </div>
</li>
