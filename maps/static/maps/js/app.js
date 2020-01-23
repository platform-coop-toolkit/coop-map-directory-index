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
      htmlString = '<b>' + e.features[0].properties.name + '</b><br />' +
        e.features[0].properties.address + '<br />' +
        e.features[0].properties.city;

    popup.setLngLat(e.features[0].geometry.coordinates)
      .setHTML(htmlString)
      .addTo(map);
  });

  map.on('mouseleave', 'coops', function () {
    map.getCanvas().style.cursor = '';
    popup.remove();
  })

});
