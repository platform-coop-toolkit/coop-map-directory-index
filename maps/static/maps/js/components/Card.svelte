<script>
import Icon from './Icon.svelte';

export let organization;

if (organization.properties.type === 'null') {
    organization.properties.type = null;
}

organization.properties.categories = organization.properties.categories.replace('[', '').replace(']', '').replace(/","/g, ',').replace(/"/g, '').split(',').filter((el) => {
  return el != '';
});
organization.properties.sectors = organization.properties.sectors.replace('[', '').replace(']', '').replace(/","/g, ',').replace(/"/g, '').split(',').filter((el) => {
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
        {#if organization.properties.type}
        <p class="card__meta card__type">
            <span class="screen-reader-text">type: </span>
            {#if organization.properties.type.icon}<Icon name={organization.properties.type.icon} />{/if}
            {organization.properties.type}
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
            {#if organization.properties.categories.length > 0}
            <div class="card__meta">
                <span class="card__subtypes">
                    <span class="screen-reader-text">{#if organization.properties.type == 'Cooperative'}cooperative{:else}organization{/if} types: </span>
                    <Icon name={'coop-type'} />
                    {#each organization.properties.categories as type, index}
                        {type}{#if index + 1 < organization.properties.categories.length},&nbsp;{/if}
                    {/each}
                </span>
            </div>
            {/if}
            {#if organization.properties.sectors.length > 0}
            <div class="card__meta">
                <span class="card__subtypes">
                    <span class="screen-reader-text">sectors: </span>
                    <Icon name={'sector-small'} />
                    {#each organization.properties.sectors as sector, index}
                        {sector}{#if index + 1 < organization.properties.sectors.length},&nbsp;{/if}
                    {/each}
                </span>
            </div>
            {/if}
        </div>
    </div>
</li>
