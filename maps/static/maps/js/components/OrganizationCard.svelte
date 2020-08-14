<script>
import Icon from './Icon.svelte';

export let organization;

let typeIcon = false;

if (organization.type) {
    switch(organization.type) {
        case 'Cooperative':
            typeIcon = 'cooperative';
            break;
        case 'Potential cooperative':
            typeIcon = 'converting';
            break;
        case 'Shared platform':
            typeIcon = 'shared-platform';
            break;
        case 'Supporting organization':
            typeIcon = 'support-organization';
            break;
    }
}
</script>

<li class="card__wrapper">
    <div class="card card--organization">
        <header>
            <h3 class="card__title">
                <a class="card__link" href="/organizations/{organization.id}">{organization.name}</a>
            </h3>
        </header>
        {#if organization.type}
        <p class="card__meta card__type">
            <span class="screen-reader-text">type: </span>
            {#if typeIcon}<Icon name={typeIcon} />{/if}
            {organization.type}
        </p>
        {/if}
        <div class="card__aside">
            {#if organization.city || organization.state || organization.country}
            <div class="card__meta">
                <span class="card__locality">
                    <span class="screen-reader-text">location: </span>
                    <Icon name={'location'} />
                    {#if organization.city}{organization.city}, {/if}
                    {#if organization.state}{organization.state}{#if organization.country},{/if} {/if}
                    {#if organization.country.name}{organization.country.name}{/if}
                </span>
            </div>
            {/if}
            {#if organization.languages.length > 0}
            <div class="card__meta">
                <span class="card__languages">
                    <span class="screen-reader-text">working languages: </span>
                    <Icon name={'language-small'} />
                    {#each organization.languages as language, index}
                        {language.iso_name}{#if index + 1 < organization.languages.length},&nbsp;{/if}
                    {/each}
                </span>
            </div>
            {/if}
            {#if organization.categories.length > 0}
            <div class="card__meta">
                <span class="card__subtypes">
                    <span class="screen-reader-text">{#if organization.type == 'Cooperative'}cooperative{:else}organization{/if} types: </span>
                    <Icon name={'coop-type'} />
                    {#each organization.categories as type, index}
                        {type}{#if index + 1 < organization.categories.length},&nbsp;{/if}
                    {/each}
                </span>
            </div>
            {/if}
            {#if organization.sectors.length > 0}
            <div class="card__meta">
                <span class="card__subtypes">
                    <span class="screen-reader-text">sectors: </span>
                    <Icon name={'sector-small'} />
                    {#each organization.sectors as sector, index}
                        {sector}{#if index + 1 < organization.sectors.length},&nbsp;{/if}
                    {/each}
                </span>
            </div>
            {/if}
        </div>
    </div>
</li>
