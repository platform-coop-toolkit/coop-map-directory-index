<script>
    import { onMount } from 'svelte';
    import Pie from 'svelte-chartjs/src/Pie.svelte';

    let labels = JSON.parse(document.getElementById('labels').innerHTML);
    let colors = JSON.parse(document.getElementById('colors').innerHTML);

    let data, countries = [];

    data = JSON.parse(document.getElementById('data').innerHTML);
    Array.prototype.forEach.call(Object.entries(data), country => {
        countries.push({id: country[0], name: country[1].name});
    })
    
    let segments = [
        'coops',
        'coops_plus',
        'supporting_orgs'
    ]

    let chartOptions = {
        aspectRatio: 1,
        legend: {
            display: false,
            position: 'right',
            labels: {
                fontColor: '#203131',
                fontFamily: '"Noto Serif", sans-serif',
                fontSize: 16
            }   
        },
        tooltips: {
            backgroundColor: '#203131',
            bodyFontColor: '#f9f9f7',
            bodyFontFamily: '"Noto Sans", sans-serif',
            bodyFontStyle: 'bold',
            xPadding: 6,
            displayColors: false
        }
    };

    let country = 'ALL';
    let segment = 'coops';
</script>

<div class="form">
    <div class="input-group">
        <label for="country">{ labels['countries'] }</label>
        <select bind:value={ country } id="country">
            {#each countries as item}
            <option value="{ item.id }">{ item.name }</option>
            {/each}
        </select>
    </div>
    <div class="input-group radio">
        <p><strong>{ labels['org_type'] }</strong></p>
        {#each segments as item}
        <label><input type="radio" name="segment" value={item} bind:group={segment} /> { labels[item] }</label>
        {/each}
    </div>
</div>

<h2>{ labels[segment] }</h2>
<div class="summary">
    <div class="organizations">
    <span class="h2">{ data[country][segment].count }</span> { labels[segment].toLowerCase() }
    </div>
    <div class="impact">
    <span class="h2">{ data[country][segment].people_impacted ? data[country][segment].people_impacted : 0 }</span> { labels['impacted'] }
    </div>
    <div class="sectors">
    <span class="h2">{ data[country][segment].sectors ? data[country][segment].sectors : 0 }</span> { labels['sectors'] }
    </div>
    <div class="scope">
        <p class="h4">{ labels['geo_scope'] }</p>
        <figure>
            <div class="chart">
                <Pie data={data[country][segment].scope} options={chartOptions} />
            </div>
            <figcaption>
                <table>
                    <caption class="screen-reader-text">{ labels['geo_scope'] }</caption>
                    {#each data[country][segment].scope.datasets[0].data as point, i}
                    <tr>
                        <td><span class="dot" style="background-color: { colors[i] };"></span>{ data[country][segment].scope.labels[i] }</td>
                        <td class="screen-reader-text">{ point } organizations</td>
                    </tr>
                    {/each}
                </table>
            </figcaption>
        </figure>
    </div>
    <div class="workers">
    <span class="h4">{ data[country][segment].workers ? data[country][segment].workers : 0 }</span> { labels['workers'] }
    </div>
    <div class="members">
    <span class="h4">{ data[country][segment].members ? data[country][segment].members : 0 }</span> { labels['members'] }
    </div>
</div>
