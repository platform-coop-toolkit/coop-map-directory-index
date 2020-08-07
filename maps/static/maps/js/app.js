import Pinecone from '@platform-coop-toolkit/pinecone';
import { generateCards, generatePopupHtml, updateStore } from './cards.js';

const menu = document.querySelector('.menu');
const menuToggle = document.querySelector('.menu-toggle');

new Pinecone.Notification();

if (menu && menuToggle) {
  new Pinecone.Menu(menu, menuToggle);
}

const tabGroups = document.querySelectorAll( '.tabs' );
if ( tabGroups ) {
  Array.prototype.forEach.call( tabGroups, tabGroup => {
    new Pinecone.Tabs( tabGroup );
  } );
}

[...document.querySelectorAll('.accordion')].forEach(accordion => {
  new Pinecone.Accordion( accordion );
} );

const icons = document.querySelectorAll( 'svg' );
if (icons) {
  Array.prototype.forEach.call(icons, icon => {
    new Pinecone.Icon(icon);
  });
}

const dialogBtn = document.getElementById('cancel-profile-creation');
if (dialogBtn) {
    let labels = JSON.parse(document.getElementById('labels').innerHTML);
    new Pinecone.Dialog(dialogBtn, {
        title: labels.cancelTitle,
        question: labels.cancelQuestion,
        confirm: labels.cancelConfirm,
        dismiss: labels.cancelDismiss,
        callback: function() {
          window.location.href = `${window.location.origin}/my-profiles/`;
        }
    });
}

const coopsBtn = document.getElementById('coops-btn');
const clientsBtn = document.getElementById('clients-btn');
const coopFoundersAndMembersBtn = document.getElementById('founders-and-members-btn');
const toolsBtn = document.getElementById('tools-btn');

if (coopsBtn || clientsBtn || coopFoundersAndMembersBtn || toolsBtn) {
  document.addEventListener('click', (event) => {
    if (event.target.id == 'founded-by-coops-btn' || event.target.id == 'member-of-coops-btn') {
      coopsBtn.click();
    }
    
    if (event.target.id == 'worked-with-btn') {
      clientsBtn.click();
    }

    if (event.target.id == 'founders-btn' || event.target.id == 'members-btn') {
      coopFoundersAndMembersBtn.click();
    }

    if (event.target.id == 'more-tools-btn') {
      toolsBtn.click();
    }
  });
}

const searchToggle = document.querySelector('.search-toggle');
if (searchToggle) {
  new Pinecone.SearchToggle(searchToggle, searchToggle.nextElementSibling);
}

const scopeAndImpact = document.getElementById('scope-and-impact');

if (scopeAndImpact) {
  const showHideFieldsForValue = (value, form) => {
    switch(value) {
      case 'Local':
        form.classList.add('show-city');
        form.classList.add('show-region');
        form.classList.add('show-country');
        break;
      case 'Regional':
        form.classList.remove('show-city');
        form.classList.add('show-region');
        form.classList.add('show-country');
        break;
      case 'National':
        form.classList.remove('show-city');
        form.classList.remove('show-region');
        form.classList.add('show-country');
        break;
      case 'International':
      case '':
      default:
        form.classList.remove('show-city');
        form.classList.remove('show-region');
        form.classList.remove('show-country');
    }
  };

  const scopes = scopeAndImpact.querySelectorAll('[name$="geo_scope"]');
  const currentScope = scopeAndImpact.querySelector('[name$="geo_scope"]:checked').value;
  showHideFieldsForValue(currentScope, scopeAndImpact);
  const scopeList = Array.from(scopes);
  scopeList.forEach(scope => {
    scope.addEventListener('change', (event) => {
      showHideFieldsForValue(event.target.value, scopeAndImpact);
    });
  });
}

const dateWrapper = document.querySelector('.date-wrapper');

if (dateWrapper) {
  const year = document.getElementById('year_founded');
  const month = document.getElementById('month_founded');
  const day = document.getElementById('day_founded');
  const founded = document.getElementById('founded');
  const foundedMin = document.getElementById('founded_min_date');
  const foundedMax = document.getElementById('founded_max_date');

  if (year.value == '') {
    month.setAttribute('disabled', '');
  }
  if (month.value == '') {
    day.setAttribute('disabled', '');
  }

  const daysInMonth = (y, m) => {
    return new Date(y, m, 0).getDate();
  };

  const updateDaysField = (y, m) => {
    if (m == '') {
      day.value = '';
    } else {
      const days = daysInMonth(y, m);
      const none = day.querySelector('option[value=""]');
      const currentDay = day.value;
      day.innerHTML = '';
      day.appendChild(none);
      for ( let i = 1; i < days + 1; i++ ) {
				const option = document.createElement( 'option' );
				const val = 9 > i ? `0${i}` : i;
				option.setAttribute( 'value', val );
				option.innerText = i;
				day.appendChild( option );
			}
      if (currentDay > days) {
        day.value = '';
      } else {
        day.value = currentDay;
      }
    }
  };

  const updateDisabledStatus = () => {
    if (year.value == '') {
      month.setAttribute('disabled', '');
    } else {
      month.removeAttribute('disabled');
    }
    if (month.value == '') {
      day.setAttribute('disabled', '');
    } else {
      day.removeAttribute('disabled');
    }
  };

  const updateFoundedDates = () => {
    if (year.value && month.value && day.value) {
      founded.value = `${year.value}-${month.value}-${day.value}`;
      foundedMin.value = `${year.value}-${month.value}-${day.value}`;
      foundedMax.value = `${year.value}-${month.value}-${day.value}`;
    } else if (year.value && month.value) {
      const days = daysInMonth(year.value, month.value);
      founded.value = '';
      foundedMin.value = `${year.value}-${month.value}-01`;
      foundedMax.value = `${year.value}-${month.value}-${days}`;
    } else if (year.value) {
      founded.value = '';
      foundedMin.value = `${year.value}-01-01`;
      foundedMax.value = `${year.value}-12-31`;
    } else {
      month.value = '';
      day.value = '';
      founded.value = '';
      foundedMin.value = '';
      foundedMax.value = '';
    }
  };

  year.addEventListener('keyup', () => {
    updateDaysField(year.value, month.value);
    updateDisabledStatus();
    updateFoundedDates();
  });

  year.addEventListener('change', () => {
    updateDaysField(year.value, month.value);
    updateDisabledStatus();
    updateFoundedDates();
  });

  month.addEventListener('change', () => {
    updateDaysField(year.value, month.value);
    updateDisabledStatus();
    updateFoundedDates();
  });

  day.addEventListener('change', () => {
    updateDisabledStatus();
    updateFoundedDates();
  });
}

[...document.querySelectorAll('.card')].forEach(function (card) {
  new Pinecone.Card( card );
});

[...document.querySelectorAll( '.input-group__parent > li' )].forEach( (container) => {
  const input = container.querySelector( '.input--parent' );
  const subInputs = container.querySelectorAll( '.input-group__descendant input' );
  if ( 0 < subInputs.length ) {
    new Pinecone.NestedCheckbox( container, input, subInputs );
  }
} );
	
[...document.querySelectorAll( '.filter-disclosure-label' )].forEach( (label) => {
  new Pinecone.DisclosureButton( label, { buttonVariant: 'button--disc', visuallyHiddenLabel: true } );
} );

[...document.querySelectorAll('#id_detailed_info-license_type input')].forEach(element => {
  const license = document.getElementById('id_detailed_info-license');
  const licenseLabel = document.querySelector('[for="id_detailed_info-license"]');

  if (element.checked) {
    if (element.value === 'floss' || element.value === 'proprietary-with-floss-integration-tools') {   
      license.style.display = 'block';
      licenseLabel.style.display = 'block';
    } else {
      license.style.display = 'none';
      licenseLabel.style.display = 'none';
    }
  }

  element.addEventListener('change', () => {
    if (element.value === 'floss' || element.value === 'proprietary-with-floss-integration-tools') {   
      license.style.display = 'block';
      licenseLabel.style.display = 'block';
    } else {
      license.style.display = 'none';
      licenseLabel.style.display = 'none';
    }
  });
});

[...document.querySelectorAll('[name="detailed_info-sector"')].forEach(element => {
  element.addEventListener('change', () => {
    const sectors = document.getElementById('id_detailed_info-sectors');
    const sectorsLabel = document.querySelector('[for="id_detailed_info-sectors"]');
    if (element.value === 'yes') {   
      sectors.style.display = 'block';
      sectorsLabel.style.display = 'block';
    } else {
      sectors.style.display = 'none';
      sectorsLabel.style.display = 'none';
    }
  });
});

[...document.querySelectorAll('[role="checkbox"]')].forEach(checkbox => {
  checkbox.addEventListener('click', () => {
    if (checkbox.getAttribute('aria-checked') !== 'true') {
      const disclosureButton = checkbox.parentNode.querySelector('button');
      disclosureButton.setAttribute('aria-expanded', 'true');
    }
  });
});

[...document.querySelectorAll('.delete-organization')].forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
  });
  const btn = form.querySelector('[type="submit"]');
  new Pinecone.Dialog(btn, {
    title: 'Delete profile?',
    question: 'Are you sure you want to delete this profile? All your information will be lost.',
    confirm: 'Yes, delete',
    dismiss: 'No, don&rsquo;t delete',
    callback: function callback() {
      form.submit();
    }
  });
});

[...document.querySelectorAll('[name="roles"]')].forEach((checkbox) => {
  checkbox.addEventListener('change', () => {
    const checkboxClass = `role-${event.target.value}`;
    if (event.target.checked) {
      document.querySelector('.form__content').classList.add(checkboxClass);
    } else {
      document.querySelector('.form__content').classList.remove(checkboxClass);
    }
  });
});

const deleteIndividual = document.querySelector('.delete-individual');
if (deleteIndividual) {
  const form = deleteIndividual;
  form.addEventListener('submit', (event) => {
    event.preventDefault();
  });
  const btn = form.querySelector('[type="submit"]');
  new Pinecone.Dialog(btn, {
    title: 'Delete profile?',
    question: 'Are you sure you want to delete your profile?',
    confirm: 'Yes, delete',
    dismiss: 'No, don&rsquo;t delete',
    callback: function callback() {
      form.submit();
    }
  });
}

/* TODO: allow map to be reset to contact info
document.addEventListener('click', (event) => {
  if (!event.target.id === 'set-to-contact-info') return;
  const address = document.getElementById('id_address').value;
  const city = document.getElementById('id_city').value;
  const state = document.getElementById('id_state').value;
  const country = document.getElementById('id_country').value;
  const postalCode = document.getElementById('id_postal_code').value;
  let addressString = '';
  if (address != '') {
    addressString = address;
  }
  if (city != '') {
    addressString = `${addressString}, ${city}`;
  }
  if (state != '') {
    addressString = `${addressString}, ${state}`;
  }
  if (country != '') {
    addressString = `${addressString}, ${country}`;
  }
  if (postalCode != '') {
    addressString = `${addressString}, ${postalCode}`;
  }
  // TODO: Post to Here API endpoint
});
*/

const geolocationMapContainer = document.getElementById('geolocation-map');

if (geolocationMapContainer) {
  let
    lng = document.getElementById('id_geolocation-lng').value,
    lat = document.getElementById('id_geolocation-lat').value
  ;
  mapboxgl.accessToken = 'pk.eyJ1IjoiZXJpY3RoZWlzZSIsImEiOiJjazVvNGNmM2wxaGhjM2pvMGc0ZmIyaXN3In0.Jrt9t5UrY5aCbndSpq5JWw';
  var geolocationMap = new mapboxgl.Map({
    container: 'geolocation-map',
    style: 'mapbox://styles/mapbox/light-v10',
    center: [lng, lat],
    zoom: 17,
    hash: false,
    rotate: false,
    scrollZoom: false
  });

  let nav = new mapboxgl.NavigationControl({showCompass: false});
  geolocationMap.addControl(nav, 'top-right');

  let geo = new mapboxgl.GeolocateControl({
    fitBoundsOptions: {
      maxZoom: 10
    }
  });
  geolocationMap.addControl(geo, 'top-right');

  const
    crosshairs = document.getElementById('crosshairs'),
    ctx = crosshairs.getContext('2d'),
    openingDimension = 40;

  const drawCrosshairs = () => {
    const x = geolocationMap.getCanvas().width / 2,
      y = geolocationMap.getCanvas().height / 2;
    crosshairs.width = x;
    crosshairs.height = y;
    ctx.clearRect(0, 0, crosshairs.width, crosshairs.height);
    ctx.strokeStyle = '#203131'; // dark-mint-500
    ctx.beginPath();
    ctx.moveTo(x/2, 0);
    ctx.lineTo(x/2, (y - openingDimension)/2);
    ctx.moveTo(x/2, (y + openingDimension)/2);
    ctx.lineTo(x/2, y);
    ctx.stroke();
  
    ctx.beginPath();
    ctx.moveTo(0, y/2);
    ctx.lineTo((x - openingDimension)/2, y/2);
    ctx.moveTo((x + openingDimension)/2, y/2);
    ctx.lineTo(x, y/2);
    ctx.stroke();
  };

  drawCrosshairs();

  geolocationMap.on('moveend', function () {
    document.getElementById('id_geolocation-lng').value = geolocationMap.getCenter().lng;
    document.getElementById('id_geolocation-lat').value = geolocationMap.getCenter().lat;

    drawCrosshairs();
  });
}

const mainMapContainer = document.getElementById('main-map');

if (mainMapContainer) {
  mapboxgl.accessToken = 'pk.eyJ1IjoiZXJpY3RoZWlzZSIsImEiOiJjazVvNGNmM2wxaGhjM2pvMGc0ZmIyaXN3In0.Jrt9t5UrY5aCbndSpq5JWw';
  var mainMap = new mapboxgl.Map({
    container: 'main-map',
    style: 'mapbox://styles/mapbox/dark-v10',
    center: [-74.5, 40],
    zoom: 4,
    hash: true,
    rotate: false,
    scrollZoom: false
  });

  let nav = new mapboxgl.NavigationControl({ showCompass: false });
  mainMap.addControl(nav, 'top-right');

  let geo = new mapboxgl.GeolocateControl({
    fitBoundsOptions: {
      maxZoom: 10
    }
  });
  mainMap.addControl(geo, 'top-right');

  mainMap.on('load', function () {
    const
      platformCoop = ['==', ['get', 'category'], 'platform co-op'],
      coopRunPlatform = ['==', ['get', 'category'], 'co-op-run platform'],
      sharedPlatform = ['==', ['get', 'category'], 'shared platform'],
      supporter = ['==', ['get', 'category'], 'supporter'],
      other = ['==', ['get', 'category'], ''],
      colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00']
    ;

    const colorScale = d3.scaleOrdinal()
      .domain('platformCoop', 'coopRunPlatform', 'sharedPlatform', 'supporter', 'other')
      .range(colors)
    ;

    let
      markers = {},
      markersOnScreen = {},
      point_counts = [],
      totals
    ;

    mainMap.addSource('organizations', {
      'type': 'geojson',
      'data': '/api/organizations/',
      'cluster': true,
      'clusterMaxZoom': 14,
      'clusterRadius': 50 //,
      // 'clusterProperties': {
      //   'platformCoop': ['+', ['case', platformCoop, 1, 0]],
      //   'coopRunPlatform': ['+', ['case', coopRunPlatform, 1, 0]],
      //   'sharedPlatform': ['+', ['case', sharedPlatform, 1, 0]],
      //   'supporter': ['+', ['case', supporter, 1, 0]],
      //   'other': ['+', ['case', other, 1, 0]]
      // }
    });

    mainMap.addSource('individuals', {
      'type': 'geojson',
      'data': '/api/users/',
      'cluster': true,
      'clusterMaxZoom': 14,
      'clusterRadius': 50
    });

    mainMap.addLayer({
      id: 'clusters',
      type: 'circle',
      source: 'organizations',
      filter: ['has', 'point_count'],
      // 'filter': ['!=', ['get', 'cluster'], true],
      'paint': {
        'circle-color': [
          'step',
          ['get', 'point_count'],
          '#51bbd6',
          100,
          '#f1f075',
          750,
          '#f28cb1'
        ],
        'circle-radius': [
          'step',
          ['get', 'point_count'],
          20,
          100,
          30,
          750,
          40
        ], //[
        //   'case',
        //   platformCoop, colorScale('platformCoop'),
        //   coopRunPlatform, colorScale('coopRunPlatform'),
        //   sharedPlatform, colorScale('sharedPlatform'),
        //   supporter, colorScale('supporter'),
        //   other, colorScale('other'),
        //   '#999'
        // ],
        'circle-opacity': 0.8,
      }
    });

    mainMap.addLayer({
      id: 'cluster-count',
      type: 'symbol',
      source: 'organizations',
      filter: ['has', 'point_count'],
      layout: {
        'text-field': '{point_count_abbreviated}',
        'text-size': 12
      }
    });

    mainMap.addLayer({
      id: 'unclustered-point',
      type: 'circle',
      source: 'organizations',
      filter: ['!', ['has', 'point_count']],
      paint: {
        'circle-color': [
          'match',
          ['get', 'category'],
          'platform co-op', colorScale('platformCoop'),
          'co-op-run platform', colorScale('coopRunPlatform'),
          'shared platform', colorScale('sharedPlatform'),
          'supporter', colorScale('supporter'),
          'other', colorScale('other'),
          '#999'
        ],
        'circle-radius': 8,
        'circle-stroke-width': 1,
        'circle-stroke-color': '#fff'
      }
    });

    mainMap.on('click', 'clusters', function (e) {
      var features = mainMap.queryRenderedFeatures(e.point, {
        layers: ['clusters']
      });
      var clusterId = features[0].properties.cluster_id;
      mainMap.getSource('organizations').getClusterExpansionZoom(
        clusterId,
        function (err, zoom) {
          if (err) return;

          mainMap.easeTo({
            center: features[0].geometry.coordinates,
            zoom: zoom
          });
        }
      );
    });

    mainMap.on('click', 'unclustered-point', function (e) {
      mainMap.getCanvas().style.cursor = 'pointer';
      let popup = new mapboxgl.Popup({
        closeButton: true,
        closeOnClick: true
      });

      popup.setLngLat(e.features[0].geometry.coordinates)
        .setHTML(generatePopupHtml(e.features[0]))
        .addTo(mainMap);
    });

    mainMap.on('mouseenter', 'clusters', function () {
      mainMap.getCanvas().style.cursor = 'pointer';
    });
    mainMap.on('mouseleave', 'clusters', function () {
      mainMap.getCanvas().style.cursor = '';
    });

    generateCards();
    updateStore(mainMap, ['unclustered-point']);

    mainMap.on('render', function () {
      updateStore(mainMap, ['unclustered-point']);
    });
    mainMap.on('moveend', function () {
      updateStore(mainMap, ['unclustered-point']);
    });

    // mainMap.addLayer({
    //   'id': 'organizations_individual_outer',
    //   'type': 'circle',
    //   'source': 'organizations',
    //   'filter': ['!=', ['get', 'cluster'], true],
    //   'paint': {
    //     'circle-color': [
    //       'case',
    //       platformCoop, colorScale('platformCoop'),
    //       coopRunPlatform, colorScale('coopRunPlatform'),
    //       sharedPlatform, colorScale('sharedPlatform'),
    //       supporter, colorScale('supporter'),
    //       other, colorScale('other'),
    //       '#999'
    //     ],
    //     'circle-opacity': 1.0,
    //     'circle-stroke-width': 2,
    //     'circle-radius': 10,
    //     'circle-color': "rgba(0, 0, 0, 0)"
    //   }
    // });

    // const updateMarkers = () => {
    //   // keep track of new markers
    //   let newMarkers = {};
    //   // get the features whether or not they are visible (https://docs.mapbox.com/mapbox-gl-js/api/#map#queryrenderedfeatures)
    //   const features = mainMap.querySourceFeatures('organizations');
    //   totals = getPointCount(features);
    //   // loop through each feature
    //   features.forEach((feature) => {
    //     const coordinates = feature.geometry.coordinates;
    //     // get our properties, which include our clustered properties
    //     const props = feature.properties;
    //     // continue only if the point is part of a cluster
    //     if (!props.cluster) {
    //       return;
    //     }
    //     // if yes, get the cluster_id
    //     const id = props.cluster_id;
    //     // create a marker object with the cluster_id as a key
    //     let marker = markers[id];
    //     // if that marker doesn't exist yet, create it
    //     if (!marker) {
    //       // create an html element (more on this later)
    //       const el = createDonutChart(props, totals);
    //       // create the marker object passing the html element and the coordinates
    //       marker = markers[id] = new mapboxgl.Marker({
    //         element: el
    //       }).setLngLat(coordinates);
    //     }
    //
    //     // create an object in our newMarkers object with our current marker representing the current cluster
    //     newMarkers[id] = marker;
    //
    //     // if the marker isn't already on screen then add it to the map
    //     if (!markersOnScreen[id]) {
    //       marker.addTo(mainMap);
    //     }
    //   });
    //
    //   // check if the marker with the cluster_id is already on the screen by iterating through our markersOnScreen object, which keeps track of that
    //   for (id in markersOnScreen) {
    //     // if there isn't a new marker with that id, then it's not visible, therefore remove it.
    //     if (!newMarkers[id]) {
    //       markersOnScreen[id].remove();
    //     }
    //   }
    //   // otherwise, it is visible and we need to add it to our markersOnScreen object
    //   markersOnScreen = newMarkers;
    // };
    //
    // const getPointCount = (features) => {
    //   features.forEach(f => {
    //     if (f.properties.cluster) {
    //       point_counts.push(f.properties.point_count)
    //     }
    //   });
    //   return point_counts;
    // };

  });
}
