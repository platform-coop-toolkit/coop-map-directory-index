mapboxgl.accessToken = 'pk.eyJ1IjoiZXJpY3RoZWlzZSIsImEiOiJjazVvNGNmM2wxaGhjM2pvMGc0ZmIyaXN3In0.Jrt9t5UrY5aCbndSpq5JWw';
var map = new mapboxgl.Map({
  container: 'map', // container id
  style: 'mapbox://styles/mapbox/dark-v10',
  center: [-74.5, 40], // starting position [lng, lat]
  zoom: 4,
  hash: true
});

let nav = new mapboxgl.NavigationControl();
map.addControl(nav, 'bottom-left');

map.on('load', function () {
  map.addSource('coops', {
    type: 'geojson',
    data: '/organizations/'
  });
  map.addLayer({
    'id': 'coops',
    'type': 'circle',
    'source': 'coops',
    'paint': {
      'circle-opacity': 0.8,
      'circle-radius': {
        'base': 1.75,
        'stops': [
          [12, 12],
          [22, 36]
        ]
      },
      'circle-color': [
        'match',
        ['get', 'category'],
        'platform co-op', '#a6cee3',
        'co-op-run platform', '#1f78b4',
        'shared platform', '#b2df8a',
        'supporter', '#33a02c',
        '#ccc'
      ]
    }
  });

  let popup = new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: false
  });

  map.on('mouseover', 'coops', function (e) {
    map.getCanvas().style.cursor = 'pointer';
    let
      htmlString = '';
      if (e.features[0].properties.url) {
        htmlString += '<b><a href="' + e.features[0].properties.url + '">' + e.features[0].properties.name + '</a></b><br />'
      } else {
        htmlString += '<b>' + e.features[0].properties.name + '</b><br />'
      }
      if (e.features[0].properties.address !== 'null') { htmlString += e.features[0].properties.address + '<br />' }
      if (e.features[0].properties.city !== 'null') { htmlString += e.features[0].properties.city + ' '}
      if (e.features[0].properties.state !== 'null') { htmlString += e.features[0].properties.state + ' ' }
      if (e.features[0].properties.postal_code !== 'null') { htmlString += e.features[0].properties.postal_code + ' ' }
      if (e.features[0].properties.country !== 'null') { htmlString += e.features[0].properties.country + ' ' }
      if (e.features[0].properties.type !== 'null' || e.features[0].properties.type !== 'null') { htmlString += '<hr>' }
      if (e.features[0].properties.type !== 'null') { htmlString += 'Type: ' + e.features[0].properties.type + '<br />'}
      if (e.features[0].properties.type !== 'null') { htmlString += 'Category: ' + e.features[0].properties.category + '<br />' }
      if (e.features[0].properties.activities !== 'null') {
        console.log(e.features[0].properties.activities, typeof(e.features[0].properties.activities));
        htmlString += 'Activities: ' + e.features[0].properties.activities.replace('[', '').replace(']', '').replace(/","/g, ', ').replace(/"/g, '');
      }

    popup.setLngLat(e.features[0].geometry.coordinates)
      .setHTML(htmlString)
      .addTo(map);
  });

  map.on('mouseleave', 'coops', function () {
    map.getCanvas().style.cursor = '';
    popup.remove();
  })

});
