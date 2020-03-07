mapboxgl.accessToken = 'pk.eyJ1IjoiZXJpY3RoZWlzZSIsImEiOiJjazVvNGNmM2wxaGhjM2pvMGc0ZmIyaXN3In0.Jrt9t5UrY5aCbndSpq5JWw';
var map = new mapboxgl.Map({
  container: 'map', // container id
  style: 'mapbox://styles/mapbox/dark-v10',
  center: [-74.5, 40], // starting position [lng, lat]
  zoom: 4,
  hash: true,
  scrollZoom: false
});

let nav = new mapboxgl.NavigationControl({ showCompass: false });
map.addControl(nav, 'top-right');

map.on('load', function () {
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

  map.addSource('organizations', {
    'type': 'geojson',
    'data': '/organizations/',
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

  map.addSource('individuals', {
    'type': 'geojson',
    'data': '/users/',
    'cluster': true,
    'clusterMaxZoom': 14,
    'clusterRadius': 50
  });

  map.addLayer({
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

  map.addLayer({
    id: 'cluster-count',
    type: 'symbol',
    source: 'organizations',
    filter: ['has', 'point_count'],
    layout: {
      'text-field': '{point_count_abbreviated}',
      'text-size': 12
    }
  });

  map.addLayer({
    id: 'unclustered-point',
    type: 'circle',
    source: 'organizations',
    filter: ['!', ['has', 'point_count']],
    paint: {
      'circle-color': '#11b4da',
      'circle-radius': 4,
      'circle-stroke-width': 1,
      'circle-stroke-color': '#fff'
    }
  });

  map.on('click', 'clusters', function (e) {
    var features = map.queryRenderedFeatures(e.point, {
      layers: ['clusters']
    });
    var clusterId = features[0].properties.cluster_id;
    map.getSource('organizations').getClusterExpansionZoom(
      clusterId,
      function (err, zoom) {
        if (err) return;

        map.easeTo({
          center: features[0].geometry.coordinates,
          zoom: zoom
        });
      }
    );
  });

  map.on('click', 'unclustered-point', function (e) {
    map.getCanvas().style.cursor = 'pointer';
    let
      htmlString = '';
      if (e.features[0].properties.url) {
        htmlString += '<strong><a href="' + e.features[0].properties.url + '">' + e.features[0].properties.name + '</a></strong><br />'
      } else {
        htmlString += '<strong>' + e.features[0].properties.name + '</strong><br />'
      }
      if (e.features[0].properties.address) { htmlString += e.features[0].properties.address + '<br />' }
      if (e.features[0].properties.city) { htmlString += e.features[0].properties.city + ' '}
      if (e.features[0].properties.state) { htmlString += e.features[0].properties.state + ' ' }
      if (e.features[0].properties.postal_code) { htmlString += e.features[0].properties.postal_code + ' ' }
      if (e.features[0].properties.country) { htmlString += e.features[0].properties.country + ' ' }
      if (e.features[0].properties.type || e.features[0].properties.category || e.features[0].properties.sectors) {
        htmlString += '<hr>'
      }
      if (e.features[0].properties.type) { htmlString += 'Type: ' + e.features[0].properties.type + '<br />'}
      if (e.features[0].properties.category) { htmlString += 'Category: ' + e.features[0].properties.category + '<br />' }
      if (e.features[0].properties.sectors) {
        htmlString += 'Sectors: ' + e.features[0].properties.sectors.replace('[', '').replace(']', '').replace(/","/g, ', ').replace(/"/g, '');
      }

    let popup = new mapboxgl.Popup({
      closeButton: true,
      closeOnClick: true
    });

    popup.setLngLat(e.features[0].geometry.coordinates)
      .setHTML(htmlString)
      .addTo(map);
  });

  map.on('mouseenter', 'clusters', function () {
    map.getCanvas().style.cursor = 'pointer';
  });
  map.on('mouseleave', 'clusters', function () {
    map.getCanvas().style.cursor = '';
  });

  let makeCardList = () => {
    let visibleFeatures = map.queryRenderedFeatures({layers: ['unclustered-point']});

    if (visibleFeatures) {
      htmlString = '<ul class="cards">\n';
      visibleFeatures.forEach(function (f) {
        htmlString += '<li class="card__wrapper"><article id="' + f.id + '" class="card"><header><h3 class="card___title"><span class="card__format">' + f.properties.category.toUpperCase() + '</span><span class="screen-reader-text">: </span></h3></header><aside class="card__aside">\n<h4>' +
          f.properties.name + '</h4><br />';
        if (f.properties.sectors) {
          htmlString += '<strong>' + f.properties.sectors.replace('[', '').replace(']', '').replace(/","/g, ', ').replace(/"/g, '') + '</strong><br />';
        }
        if (f.properties.city) {
          htmlString += f.properties.city + ' '
        }
        if (f.properties.state) {
          htmlString += f.properties.state + ' '
        }
        if (f.properties.country) {
          htmlString += f.properties.country
        }
        htmlString += '</aside></article></li>';
      });
      htmlString += '</ul>';
      document.getElementById('visibles').innerHTML = htmlString;

      [...document.getElementsByTagName('article')].forEach(function (article) {
        article.addEventListener('click', function () {
          window.location = '/maps/organizations/' + article.id;
        })
      })
    }
  };

  map.on('render', function () {
    makeCardList();
  });
  map.on('moveend', function () {
    makeCardList();
  })

  // map.addLayer({
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
  //   const features = map.querySourceFeatures('organizations');
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
  //       marker.addTo(map);
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

/*
  map.on('mouseover', 'organizations', function (e) {
    map.getCanvas().style.cursor = 'pointer';
    let
      htmlString = '';
      if (e.features[0].properties.url) {
        htmlString += '<strong><a href="' + e.features[0].properties.url + '">' + e.features[0].properties.name + '</a></strong><br />'
      } else {
        htmlString += '<strong>' + e.features[0].properties.name + '</strong><br />'
      }
      if (e.features[0].properties.address !== 'null') { htmlString += e.features[0].properties.address + '<br />' }
      if (e.features[0].properties.city !== 'null') { htmlString += e.features[0].properties.city + ' '}
      if (e.features[0].properties.state !== 'null') { htmlString += e.features[0].properties.state + ' ' }
      if (e.features[0].properties.postal_code !== 'null') { htmlString += e.features[0].properties.postal_code + ' ' }
      if (e.features[0].properties.country !== 'null') { htmlString += e.features[0].properties.country + ' ' }
      if (e.features[0].properties.type !== 'null' || e.features[0].properties.type !== 'null') { htmlString += '<hr>' }
      if (e.features[0].properties.type !== 'null') { htmlString += 'Type: ' + e.features[0].properties.type + '<br />'}
      if (e.features[0].properties.type !== 'null') { htmlString += 'Category: ' + e.features[0].properties.category + '<br />' }
      if (e.features[0].properties.sectors !== 'null') {
        htmlString += 'Sectors: ' + e.features[0].properties.sectors.replace('[', '').replace(']', '').replace(/","/g, ', ').replace(/"/g, '');
      }

    popup.setLngLat(e.features[0].geometry.coordinates)
      .setHTML(htmlString)
      .addTo(map);
  });

  map.on('mouseleave', 'organizations', function () {
    map.getCanvas().style.cursor = '';
    popup.remove();
  })
*/

});
