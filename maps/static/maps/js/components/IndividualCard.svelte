<script>
import Icon from './Icon.svelte';

export let individual;

	let down, up, link;
	
    const downHandler = () => {
        down = +new Date();
    }

    const upHandler = () => {
        up = +new Date();
        if ( 200 > ( up - down ) ) {
            link.click();
        }
    }
</script>

<li class="card__wrapper">
    <div class="card card--individual" on:mousedown={downHandler} on:mouseup={upHandler}>
        <header>
            <h3 class="card__title">
                <a class="card__link" bind:this={link} href="/individuals/{individual.id}">{individual.name}</a>
            </h3>
        </header>
        {#if individual.roles.length > 0}
        <div class="card__meta card__roles">
            <span class="screen-reader-text">roles: </span>
            {#each individual.roles as role}
            <p class="card__role">
                <Icon name={role.icon} />
                {role.name}
            </p>
            {/each}
        </div>
        {/if}
        <div class="card__aside">
            {#if individual.city || individual.state || individual.country}
            <div class="card__meta">
                <span class="card__locality">
                    <span class="screen-reader-text">location: </span>
                    <Icon name={'location'} />
                    {#if individual.city}{individual.city}, {/if}
                    {#if individual.state}{individual.state}{#if individual.country},{/if} {/if}
                    {#if individual.country.name}{individual.country.name}{/if}
                </span>
            </div>
            {/if}
            {#if individual.languages.length > 0}
            <div class="card__meta">
                <span class="card__languages">
                    <span class="screen-reader-text">languages spoken: </span>
                    <Icon name={'language-small'} />
                    {#each individual.languages as language, index}
                        {language.iso_name}{#if index + 1 < individual.languages.length},&nbsp;{/if}
                    {/each}
                </span>
            </div>
            {/if}
        </div>
    </div>
</li>
