import Pinecone from '@platform-coop-toolkit/pinecone';
import * as d3 from 'd3';
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
    style: `${process.env.MAP_ASSETS_BASE_URL}/static/maps/dist/styles/pcc/style.json`,
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
    style: `${process.env.MAP_ASSETS_BASE_URL}/static/maps/dist/styles/pcc/style.json`,
    center: [-74.5, 40],
    minZoom: 1.0,
    maxZoom: 15.0,
    zoom: 4,
    hash: true,
    rotate: false,
    scrollZoom: true
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
      coop = ['==', ['get', 'type'], 'Cooperative'],
      potentialCoop = ['==', ['get', 'type'], 'Potential cooperative'],
      sharedPlatform = ['==', ['get', 'type'], 'Shared platform'],
      supportingOrganization = ['==', ['get', 'type'], 'Supporting organization'],
      other = ['any',
        ['==', ['get', 'type'], 'Company'],
        ['==', ['get', 'type'], 'Individual'],
        ['==', ['get', 'type'], 'Resource']
      ];

    mainMap.addSource('organizations', {
      'type': 'geojson',
      'data': '/api/organizations/',
      'cluster': true,
      'clusterMaxZoom': 14,
      'clusterRadius': 50,
      'clusterProperties': {
        'coop': ['+', ['case', coop, 1, 0]],
        'potentialCoop': ['+', ['case', potentialCoop, 1, 0]],
        'sharedPlatform': ['+', ['case', sharedPlatform, 1, 0]],
        'supportingOrganization': ['+', ['case', supportingOrganization, 1, 0]]
      }
    });

    mainMap.addSource('individuals', {
      'type': 'geojson',
      'data': '/api/users/',
      'cluster': true,
      'clusterMaxZoom': 14,
      'clusterRadius': 50
    });

    mainMap.addLayer({
      id: 'organization-clusters',
      type: 'circle',
      source: 'organizations',
      filter: ['has', 'point_count'],
      'paint': {
        'circle-color': [
          'step',
          ['get', 'point_count'],
          '#1d7c79',
          50,
          '#16605d',
          100,
          '#18514f',
          200,
          '#1c4342',
          500,
          '#203131'
        ],
        'circle-radius': [
          'step',
          ['get', 'point_count'],
          20,
          10,
          30,
          50,
          40,
          100,
          50,
          200,
          60,
          500,
          70
        ],
        'circle-opacity': 0.9,
      }
    });

    mainMap.addLayer({
      id: 'individual-clusters',
      type: 'circle',
      source: 'individuals',
      filter: ['has', 'point_count'],
      'paint': {
        'circle-color': [
          'step',
          ['get', 'point_count'],
          '#fdc2a7',
          50,
          '#ffa47a',
          100,
          '#ff621a',
          200,
          '#973102',
          500,
          '#531A00'
        ],
        'circle-radius': [
          'step',
          ['get', 'point_count'],
          20,
          10,
          30,
          50,
          40,
          100,
          50,
          200,
          60,
          500,
          70
        ],
        'circle-opacity': 0.9,
        'circle-stroke-width': 1,
        'circle-stroke-color': '#203131'
      }
    });

    mainMap.addLayer({
      id: 'organization-cluster-count',
      type: 'symbol',
      source: 'organizations',
      filter: ['has', 'point_count'],
      layout: {
        'text-font': ['Noto Sans Regular'],
        'text-field': '{point_count_abbreviated}',
        'text-size': 12
      },
      paint: {
        'text-color': '#ffffff'
      }
    });

    mainMap.addLayer({
      id: 'individual-cluster-count',
      type: 'symbol',
      source: 'individuals',
      filter: ['has', 'point_count'],
      layout: {
        'text-font': ['Noto Sans Regular'],
        'text-field': '{point_count_abbreviated}',
        'text-size': 12
      },
      paint: {
        'text-color': [
          'step',
          ['get', 'point_count'],
          '#000000',
          200,
          '#ffffff'
        ]
      }
    });

    mainMap.addLayer({
      id: 'unclustered-individuals',
      type: 'circle',
      source: 'individuals',
      filter: ['!', ['has', 'point_count']],
      paint: {
        'circle-color': '#ff621a',
        'circle-radius': 8,
        'circle-stroke-width': 1,
        'circle-stroke-color': '#294040'
      }
    });

    mainMap.addLayer({
      id: 'unclustered-organizations',
      type: 'circle',
      source: 'organizations',
      filter: ['!', ['has', 'point_count']],
      paint: {
        'circle-color': [
          'case',
          coop, '#0b8441',
          potentialCoop, '#c9f8db',
          sharedPlatform, '#face00',
          supportingOrganization, '#30cfc9',
          other, '#585850',
          '#585850'
        ],
        'circle-radius': [
          'case',
          coop, 8,
          potentialCoop, 8,
          sharedPlatform, 8,
          supportingOrganization, 8,
          other, 3,
          3
        ],
        'circle-stroke-width': [
          'case',
          coop, 1,
          potentialCoop, 1,
          sharedPlatform, 1,
          supportingOrganization, 1,
          other, 6,
          6
        ],
        'circle-stroke-color': [
          'case',
          coop, '#294040',
          potentialCoop, '#294040',
          sharedPlatform, '#294040',
          supportingOrganization, '#294040',
          other, '#b2b2a7',
          '#b2b2a7'
        ]
      }
    });

    mainMap.on('click', 'organization-clusters', function (e) {
      var features = mainMap.queryRenderedFeatures(e.point, {
        layers: ['organization-clusters']
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

    mainMap.on('click', 'unclustered-organizations', function (e) {
      mainMap.getCanvas().style.cursor = 'pointer';
      let popup = new mapboxgl.Popup({
        closeButton: true,
        closeOnClick: true
      });

      popup.setLngLat(e.features[0].geometry.coordinates)
        .setHTML(generatePopupHtml(e.features[0]))
        .addTo(mainMap);
    });

    mainMap.on('mouseenter', 'organization-clusters', function () {
      mainMap.getCanvas().style.cursor = 'pointer';
    });
    mainMap.on('mouseleave', 'organization-clusters', function () {
      mainMap.getCanvas().style.cursor = '';
    });

    generateCards();
    updateStore(mainMap, ['unclustered-organizations', 'unclustered-individuals']);

    mainMap.on('render', function () {
      updateStore(mainMap, ['unclustered-organizations', 'unclustered-individuals']);
    });
    mainMap.on('moveend', function () {
      updateStore(mainMap, ['unclustered-organizations', 'unclustered-individuals']);
    });
  });
}
