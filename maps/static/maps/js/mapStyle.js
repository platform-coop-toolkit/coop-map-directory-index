module.exports = {
    'version': 8,
    'name': 'OS Open Zoomstack - Light',
    'metadata': {
      'mapbox:automapbox-streets': true,
      'mapbox:type': 'template',
      'mapbox:sdk-support': {'js': '0.50.0', 'android': '6.7.0', 'ios': '4.6.0'},
      'mapbox:groups': {
        'e196265c0e550aaddd2885dc32fdb674': {
          'name': 'Names Group',
          'collapsed': true
        },
        '2a680f24b0d35061ed7d21fd33c9cf08': {
          'name': 'Road Level 0 Group',
          'collapsed': true
        },
        '52c81d2ff926c87a0714f2697b2f3694': {
          'name': 'Road Level 1 Group',
          'collapsed': true
        },
        '0845f59ef0d52359da6fd788b079f747': {
          'name': 'Road Level 2 Group',
          'collapsed': true
        },
        'beaf4956fb8a63410ecf80abdebcdfb5': {
          'name': 'Road Names Group',
          'collapsed': true
        }
      },
      'maputnik:renderer': 'mbgljs'
    },
    'center': [-1.464858786792547, 50.939150779110975],
    'zoom': 13.12365211904204,
    'bearing': -0.44200633613297663,
    'pitch': 0,
    'light': {'intensity': 0.25, 'color': 'hsl(0, 0%, 100%)'},
    'sources': {
      'mapbox_streets': {
        'url': 'mapbox://mapbox.mapbox-streets-v8',
        'type': 'vector'
      }
    },
    'sprite': `${process.env.BASE_URL}/static/maps/dist/styles/pcc/sprites`,
    'glyphs': `${process.env.BASE_URL}/glyphs/{fontstack}/{range}.pbf`,
    'layers': [
      {
        'id': 'background',
        'type': 'background',
        'paint': {'background-color': '#fceeb0', 'background-opacity': 0.6}
      },
      {
        'id': 'waterway',
        'type': 'line',
        'source': 'mapbox_streets',
        'source-layer': 'waterway',
        'layout': {'line-join': 'round'},
        'paint': {
          'line-color': '#30cfc9',
          'line-width': [
            'match',
            ['get', 'type'],
            ['national', 'regional', 'district', 'local'],
            1,
            ['MHW'],
            1.2,
            ['MLW'],
            0.7,
            1
          ],
          'line-opacity': 0.8
        }
      },
      {
        'id': 'water',
        'type': 'fill',
        'source': 'mapbox_streets',
        'source-layer': 'water',
        'layout': {},
        'paint': {'fill-color': '#30cfc9', 'fill-opacity': 0.8}
      },
      {
        'id': 'landuse_overlay',
        'type': 'fill',
        'source': 'mapbox_streets',
        'source-layer': 'landuse_overlay',
        'maxzoom': 12,
        'layout': {'visibility': 'none'},
        'paint': {
          'fill-color': '#d8ddd4',
          'fill-opacity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.6,
            9,
            0.5,
            12,
            0.1
          ]
        }
      },
      {
        'id': 'national-parks',
        'type': 'fill',
        'source': 'mapbox_streets',
        'source-layer': 'landuse_overlay',
        'maxzoom': 12,
        'filter': [
          'all',
          ['match', ['get', 'class'], ['national_park'], true, false]
        ],
        'layout': {'visibility': 'visible'},
        'paint': {
          'fill-color': '#45d385',
          'fill-opacity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.075,
            9,
            0.15,
            12,
            0
          ]
        }
      },
      {
        'id': 'urban-areas',
        'type': 'fill',
        'source': 'mapbox_streets',
        'source-layer': 'urban_areas',
        'maxzoom': 11,
        'layout': {'visibility': 'none'},
        'paint': {
          'fill-color': '#e6e5e1',
          'fill-opacity': ['interpolate', ['linear'], ['zoom'], 6, 0.4, 11, 0.6]
        }
      },
      {
        'id': 'sites',
        'type': 'fill',
        'source': 'mapbox_streets',
        'source-layer': 'sites',
        'layout': {'visibility': 'none'},
        'paint': {'fill-color': '#eee7dd', 'fill-opacity': 0.7}
      },
      {
        'id': 'park',
        'type': 'fill',
        'source': 'mapbox_streets',
        'source-layer': 'landuse',
        'filter': ['match', ['get', 'class'], ['park'], false, true],
        'layout': {'visibility': 'visible'},
        'paint': {
          'fill-color': '#0b8441',
          'fill-antialias': false,
          'fill-opacity': 0.15,
          'fill-outline-color': '#294040'
        }
      },
      {
        'id': 'greenspace outlines',
        'type': 'line',
        'source': 'mapbox_streets',
        'source-layer': 'greenspaces',
        'layout': {'visibility': 'none', 'line-join': 'round'},
        'paint': {
          'line-color': '#d5ddd0',
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            10,
            0.1,
            15,
            0.3,
            18,
            0.6
          ]
        }
      },
      {
        'id': 'wood',
        'type': 'fill',
        'source': 'mapbox_streets',
        'source-layer': 'landuse',
        'filter': ['all', ['match', ['get', 'class'], ['wood'], true, false]],
        'layout': {'visibility': 'visible'},
        'paint': {
          'fill-color': '#973102',
          'fill-opacity': ['interpolate', ['linear'], ['zoom'], 6, 0.05, 12, 0.1]
        }
      },
      {
        'id': 'foreshore',
        'type': 'fill',
        'source': 'mapbox_streets',
        'source-layer': 'foreshore',
        'layout': {'visibility': 'none'},
        'paint': {'fill-color': '#e9e7e2'}
      },
      {
        'id': 'buildings',
        'type': 'fill',
        'source': 'mapbox_streets',
        'source-layer': 'building',
        'layout': {'visibility': 'visible'},
        'paint': {
          'fill-color': '#ff621a',
          'fill-translate': [0, 0],
          'fill-opacity': 0.5
        }
      },
      {
        'id': 'roads 0 Restricted Road',
        'type': 'line',
        'metadata': {'mapbox:group': '2a680f24b0d35061ed7d21fd33c9cf08'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['==', ['get', 'level'], 0],
          ['match', ['get', 'type'], ['restricted'], true, false]
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-color': '#ffffff',
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            12,
            1,
            14,
            2.5,
            15,
            4,
            16,
            7,
            18,
            24,
            22,
            85
          ],
          'line-opacity': 1,
          'line-dasharray': [2, 0.5]
        }
      },
      {
        'id': 'roads 0 Local Road',
        'type': 'line',
        'metadata': {'mapbox:group': '2a680f24b0d35061ed7d21fd33c9cf08'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['==', ['get', 'level'], 0],
          ['match', ['get', 'type'], ['local'], true, false]
        ],
        'layout': {
          'line-cap': 'round',
          'line-join': 'round',
          'visibility': 'visible'
        },
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            12,
            1.4,
            14,
            3.5,
            15,
            5,
            16,
            12,
            18,
            35,
            22,
            100
          ],
          'line-color': '#ffffff'
        }
      },
      {
        'id': 'roads 0 Guided Busway Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '2a680f24b0d35061ed7d21fd33c9cf08'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['==', ['get', 'level'], 0],
          ['match', ['get', 'type'], ['Guided Busway'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            1.5,
            12,
            1.7,
            14,
            3.5,
            15,
            5,
            16,
            12,
            18,
            35,
            22,
            100
          ],
          'line-color': '#ffffff'
        }
      },
      {
        'id': 'roads 0 Guided Busway Centreline',
        'type': 'line',
        'metadata': {'mapbox:group': '2a680f24b0d35061ed7d21fd33c9cf08'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['==', ['get', 'level'], 0],
          ['match', ['get', 'type'], ['Guided Busway'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            8,
            0.1,
            10,
            0.2,
            12,
            0.2,
            14,
            0.4,
            15,
            0.6,
            16,
            0.75,
            18,
            3,
            22,
            10
          ],
          'line-color': '#e1e1e1'
        }
      },
      {
        'id': 'roads 0 Motorway',
        'type': 'line',
        'metadata': {'mapbox:group': '2a680f24b0d35061ed7d21fd33c9cf08'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': ['all', ['match', ['get', 'class'], ['motorway'], true, false]],
        'layout': {
          'line-cap': 'round',
          'line-join': 'round',
          'visibility': 'visible'
        },
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.75,
            10,
            2,
            12,
            2.75,
            14,
            4.5,
            15,
            8,
            16,
            17,
            18,
            48,
            22,
            140
          ],
          'line-color': '#ffffff'
        }
      },
      {
        'id': 'roads 0 Minor Road',
        'type': 'line',
        'metadata': {'mapbox:group': '2a680f24b0d35061ed7d21fd33c9cf08'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['==', ['get', 'level'], 0],
          ['match', ['get', 'type'], ['Minor'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            1.5,
            12,
            1.7,
            14,
            3.5,
            15,
            6.5,
            16,
            15,
            18,
            44,
            22,
            120
          ],
          'line-color': 'hsl(0, 0%, 100%)'
        }
      },
      {
        'id': 'roads 0 B Road',
        'type': 'line',
        'metadata': {'mapbox:group': '2a680f24b0d35061ed7d21fd33c9cf08'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['==', ['get', 'level'], 0],
          ['match', ['get', 'type'], ['B Road'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            1.5,
            12,
            1.7,
            14,
            3.5,
            15,
            6.5,
            16,
            15,
            18,
            44,
            22,
            120
          ],
          'line-color': 'hsl(0, 0%, 100%)'
        }
      },
      {
        'id': 'roads 0 A Road',
        'type': 'line',
        'metadata': {'mapbox:group': '2a680f24b0d35061ed7d21fd33c9cf08'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['==', ['get', 'level'], 0],
          ['match', ['get', 'type'], ['A Road'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            1.5,
            12,
            1.7,
            14,
            3.5,
            15,
            6.5,
            16,
            15,
            18,
            44,
            22,
            120
          ],
          'line-color': 'hsl(0, 0%, 100%)'
        }
      },
      {
        'id': 'roads 0 Primary Road',
        'type': 'line',
        'metadata': {'mapbox:group': '2a680f24b0d35061ed7d21fd33c9cf08'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['==', ['get', 'level'], 0],
          ['match', ['get', 'type'], ['Primary'], true, false]
        ],
        'layout': {
          'line-cap': 'round',
          'line-join': 'round',
          'visibility': 'visible'
        },
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.5,
            10,
            1.75,
            12,
            2,
            14,
            4,
            15,
            7.5,
            16,
            16,
            18,
            46,
            22,
            130
          ],
          'line-color': '#ffffff',
          'line-opacity': ['interpolate', ['linear'], ['zoom'], 5, 0.6, 9, 1]
        }
      },
      {
        'id': 'roads 1 Local Road Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [1], true, false],
          ['match', ['get', 'type'], ['Local'], true, false]
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            12,
            2.2,
            14,
            5,
            15,
            7,
            16,
            18,
            18,
            48,
            22,
            140
          ],
          'line-color': '#f2f0ed'
        }
      },
      {
        'id': 'roads 1 Minor Road Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [1], true, false],
          ['match', ['get', 'type'], ['Minor'], true, false]
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            2,
            12,
            3,
            14,
            6.5,
            15,
            10,
            16,
            23,
            18,
            58,
            22,
            160
          ],
          'line-color': '#f2f0ed'
        }
      },
      {
        'id': 'roads 1 B Road Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [1], true, false],
          ['match', ['get', 'type'], ['B Road'], true, false]
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            2,
            12,
            3,
            14,
            6.5,
            15,
            10,
            16,
            23,
            18,
            58,
            22,
            160
          ],
          'line-color': '#f2f0ed'
        }
      },
      {
        'id': 'roads 1 A Road Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [1], true, false],
          ['match', ['get', 'type'], ['A Road'], true, false]
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            2,
            12,
            3,
            14,
            6.5,
            15,
            10,
            16,
            23,
            18,
            58,
            22,
            160
          ],
          'line-color': '#f2f0ed'
        }
      },
      {
        'id': 'roads 1 Primary Road Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [1], true, false],
          ['match', ['get', 'type'], ['Primary'], true, false]
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            2,
            12,
            3,
            14,
            6.5,
            15,
            10,
            16,
            23,
            18,
            58,
            22,
            160
          ],
          'line-color': '#f2f0ed',
          'line-opacity': ['interpolate', ['linear'], ['zoom'], 5, 0.4, 9, 1]
        }
      },
      {
        'id': 'roads 1 Motorway Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': ['all', ['match', ['get', 'class'], ['motorway'], true, false]],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            2,
            12,
            3,
            14,
            6.5,
            15,
            10,
            16,
            23,
            18,
            58,
            22,
            160
          ],
          'line-color': '#f2f0ed'
        }
      },
      {
        'id': 'roads 1 Restricted Road',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [1], true, false],
          ['match', ['get', 'type'], ['Restricted'], true, false]
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-color': 'hsl(0, 0%, 100%)',
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            12,
            1,
            14,
            2.5,
            15,
            4,
            16,
            7,
            18,
            24,
            22,
            85
          ],
          'line-opacity': 1,
          'line-dasharray': [2, 0.5]
        }
      },
      {
        'id': 'roads 1 Local Road',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [1], true, false],
          ['match', ['get', 'type'], ['Local'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            12,
            1.4,
            14,
            3.5,
            15,
            5,
            16,
            12,
            18,
            35,
            22,
            100
          ],
          'line-color': '#ffffff'
        }
      },
      {
        'id': 'roads 1 Guided Busway Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [1], true, false],
          ['match', ['get', 'type'], ['Guided Busway'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            1.5,
            12,
            1.7,
            14,
            3.5,
            15,
            5,
            16,
            12,
            18,
            35,
            22,
            100
          ],
          'line-color': '#ffffff'
        }
      },
      {
        'id': 'roads 1 Guided Busway Centreline',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [1], true, false],
          ['match', ['get', 'type'], ['Guided Busway'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            8,
            0.1,
            10,
            0.2,
            12,
            0.2,
            14,
            0.4,
            15,
            0.6,
            16,
            0.75,
            18,
            3,
            22,
            10
          ],
          'line-color': '#e1e1e1'
        }
      },
      {
        'id': 'roads 1 Motorway',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': ['all', ['match', ['get', 'class'], ['motorway'], true, false]],
        'layout': {
          'line-cap': 'round',
          'line-join': 'round',
          'visibility': 'visible'
        },
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.75,
            10,
            2,
            12,
            2.75,
            14,
            4.5,
            15,
            8,
            16,
            17,
            18,
            48,
            22,
            140
          ],
          'line-color': '#ffffff'
        }
      },
      {
        'id': 'roads 1 Minor Road',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [1], true, false],
          ['match', ['get', 'type'], ['Minor'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            1.5,
            12,
            1.7,
            14,
            3.5,
            15,
            6.5,
            16,
            15,
            18,
            44,
            22,
            120
          ],
          'line-color': 'hsl(0, 0%, 100%)'
        }
      },
      {
        'id': 'roads 1 B Road',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [1], true, false],
          ['match', ['get', 'type'], ['B Road'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            1.5,
            12,
            1.7,
            14,
            3.5,
            15,
            6.5,
            16,
            15,
            18,
            44,
            22,
            120
          ],
          'line-color': 'hsl(0, 0%, 100%)'
        }
      },
      {
        'id': 'roads 1 A Road',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [1], true, false],
          ['match', ['get', 'type'], ['A Road'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            1.5,
            12,
            1.7,
            14,
            3.5,
            15,
            6.5,
            16,
            15,
            18,
            44,
            22,
            120
          ],
          'line-color': 'hsl(0, 0%, 100%)'
        }
      },
      {
        'id': 'roads 1 Primary Road',
        'type': 'line',
        'metadata': {'mapbox:group': '52c81d2ff926c87a0714f2697b2f3694'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [1], true, false],
          ['match', ['get', 'type'], ['Primary'], true, false]
        ],
        'layout': {
          'line-join': 'round',
          'line-cap': 'round',
          'visibility': 'visible'
        },
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.5,
            10,
            1.75,
            12,
            2,
            14,
            4,
            15,
            7.5,
            16,
            16,
            18,
            46,
            22,
            130
          ],
          'line-color': '#ffffff',
          'line-opacity': ['interpolate', ['linear'], ['zoom'], 5, 0.6, 9, 1]
        }
      },
      {
        'id': 'roads 2 Local Road Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [2], true, false],
          ['match', ['get', 'type'], ['Local'], true, false]
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            12,
            2.2,
            14,
            5,
            15,
            7,
            16,
            18,
            18,
            48,
            22,
            140
          ],
          'line-color': '#f2f0ed'
        }
      },
      {
        'id': 'roads 2 Minor Road Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [2], true, false],
          ['match', ['get', 'type'], ['Minor'], true, false]
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            2,
            12,
            3,
            14,
            6.5,
            15,
            10,
            16,
            23,
            18,
            58,
            22,
            160
          ],
          'line-color': '#f2f0ed'
        }
      },
      {
        'id': 'roads 2 B Road Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [2], true, false],
          ['match', ['get', 'type'], ['B Road'], true, false]
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            2,
            12,
            3,
            14,
            6.5,
            15,
            10,
            16,
            23,
            18,
            58,
            22,
            160
          ],
          'line-color': '#f2f0ed'
        }
      },
      {
        'id': 'roads 2 A Road Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [2], true, false],
          ['match', ['get', 'type'], ['A Road'], true, false]
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            2,
            12,
            3,
            14,
            6.5,
            15,
            10,
            16,
            23,
            18,
            58,
            22,
            160
          ],
          'line-color': '#f2f0ed'
        }
      },
      {
        'id': 'roads 2 Primary Road Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [2], true, false],
          ['match', ['get', 'type'], ['Primary'], true, false]
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            2,
            12,
            3,
            14,
            6.5,
            15,
            10,
            16,
            23,
            18,
            58,
            22,
            160
          ],
          'line-color': '#f2f0ed',
          'line-opacity': ['interpolate', ['linear'], ['zoom'], 5, 0.4, 9, 1]
        }
      },
      {
        'id': 'roads 2 Motorway Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': ['all', ['match', ['get', 'class'], ['motorway'], true, false]],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            2,
            12,
            3,
            14,
            6.5,
            15,
            10,
            16,
            23,
            18,
            58,
            22,
            160
          ],
          'line-color': '#f2f0ed'
        }
      },
      {
        'id': 'roads 2 Restricted Road',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [2], true, false],
          ['match', ['get', 'type'], ['Restricted'], true, false]
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-color': 'hsl(0, 0%, 100%)',
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            12,
            1,
            14,
            2.5,
            15,
            4,
            16,
            7,
            18,
            24,
            22,
            85
          ],
          'line-opacity': 1,
          'line-dasharray': [2, 0.5]
        }
      },
      {
        'id': 'roads 2 Local Road',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [2], true, false],
          ['match', ['get', 'type'], ['Local'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            12,
            1.4,
            14,
            3.5,
            15,
            5,
            16,
            12,
            18,
            35,
            22,
            100
          ],
          'line-color': '#ffffff'
        }
      },
      {
        'id': 'roads 2 Guided Busway Casing',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [2], true, false],
          ['match', ['get', 'type'], ['Guided Busway'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            1.5,
            12,
            1.7,
            14,
            3.5,
            15,
            5,
            16,
            12,
            18,
            35,
            22,
            100
          ],
          'line-color': '#ffffff'
        }
      },
      {
        'id': 'roads 2 Guided Busway Centreline',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [2], true, false],
          ['match', ['get', 'type'], ['Guided Busway'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            8,
            0.1,
            10,
            0.2,
            12,
            0.2,
            14,
            0.4,
            15,
            0.6,
            16,
            0.75,
            18,
            3,
            22,
            10
          ],
          'line-color': '#e1e1e1'
        }
      },
      {
        'id': 'roads 2 Motorway',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': ['all', ['match', ['get', 'class'], ['motorway'], true, false]],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.75,
            10,
            2,
            12,
            2.75,
            14,
            4.5,
            15,
            8,
            16,
            17,
            18,
            48,
            22,
            140
          ],
          'line-color': '#ffffff'
        }
      },
      {
        'id': 'roads 2 Minor Road',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [2], true, false],
          ['match', ['get', 'type'], ['Minor'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            1.5,
            12,
            1.7,
            14,
            3.5,
            15,
            6.5,
            16,
            15,
            18,
            44,
            22,
            120
          ],
          'line-color': 'hsl(0, 0%, 100%)'
        }
      },
      {
        'id': 'roads 2 B Road',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [2], true, false],
          ['match', ['get', 'type'], ['B Road'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            1.5,
            12,
            1.7,
            14,
            3.5,
            15,
            6.5,
            16,
            15,
            18,
            44,
            22,
            120
          ],
          'line-color': 'hsl(0, 0%, 100%)'
        }
      },
      {
        'id': 'roads 2 A Road',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [2], true, false],
          ['match', ['get', 'type'], ['A Road'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.35,
            10,
            1.5,
            12,
            1.7,
            14,
            3.5,
            15,
            6.5,
            16,
            15,
            18,
            44,
            22,
            120
          ],
          'line-color': 'hsl(0, 0%, 100%)'
        }
      },
      {
        'id': 'roads 2 Primary Road',
        'type': 'line',
        'metadata': {'mapbox:group': '0845f59ef0d52359da6fd788b079f747'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'all',
          ['match', ['get', 'level'], [2], true, false],
          ['match', ['get', 'type'], ['Primary'], true, false]
        ],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            5,
            0.5,
            10,
            1.75,
            12,
            2,
            14,
            4,
            15,
            7.5,
            16,
            16,
            18,
            46,
            22,
            130
          ],
          'line-color': '#ffffff',
          'line-opacity': ['interpolate', ['linear'], ['zoom'], 5, 0.6, 9, 1]
        }
      },
      {
        'id': 'road Tunnels',
        'type': 'line',
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': ['match', ['get', 'type'], ['Tunnels'], true, false],
        'layout': {'line-cap': 'round', 'line-join': 'round'},
        'paint': {
          'line-width': ['interpolate', ['linear'], ['zoom'], 9, 0.5, 17, 2],
          'line-color': '#4b4444',
          'line-opacity': ['interpolate', ['linear'], ['zoom'], 9, 0.1, 14, 0.35],
          'line-dasharray': [3, 2.5]
        }
      },
      {
        'id': 'rail',
        'type': 'line',
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'filter': [
          'match',
          ['get', 'class'],
          ['major_rail', 'minor_rail'],
          false,
          true
        ],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-color': '#a7a39b',
          'line-opacity': ['interpolate', ['linear'], ['zoom'], 10, 0.2, 14, 1],
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            10,
            [
              'match',
              ['get', 'type'],
              ['Multi Track'],
              0.6,
              ['Single Track'],
              0.5,
              ['Narrow Gauge'],
              0.4,
              1
            ],
            17,
            [
              'match',
              ['get', 'type'],
              ['Multi Track'],
              2,
              ['Single Track'],
              1.5,
              ['Narrow Gauge'],
              1,
              1
            ]
          ]
        }
      },
      {
        'id': 'rail tunnel',
        'type': 'line',
        'source': 'mapbox_streets',
        'source-layer': 'rail',
        'filter': ['match', ['get', 'type'], ['Tunnel'], true, false],
        'layout': {'line-join': 'round'},
        'paint': {
          'line-color': '#a7a39b',
          'line-opacity': ['interpolate', ['linear'], ['zoom'], 10, 0.2, 14, 0.6],
          'line-width': ['interpolate', ['linear'], ['zoom'], 10, 0.6, 17, 1.5],
          'line-dasharray': [5, 3]
        }
      },
      {
        'id': 'admin',
        'type': 'line',
        'source': 'mapbox_streets',
        'source-layer': 'admin',
        'layout': {'line-join': 'round'},
        'paint': {'line-color': '#cfcfcf'}
      },
      {
        'id': 'etl',
        'type': 'line',
        'source': 'mapbox_streets',
        'source-layer': 'etl',
        'layout': {'line-join': 'round'},
        'paint': {
          'line-color': '#b2b2a7',
          'line-opacity': 0.25,
          'line-dasharray': [10, 5]
        }
      },
      {
        'id': 'road numbers',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'beaf4956fb8a63410ecf80abdebcdfb5'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'minzoom': 10,
        'filter': [
          'match',
          ['get', 'type'],
          ['primary', 'motorway'],
          false,
          true
        ],
        'layout': {
          'text-field': ['to-string', ['get', 'number']],
          'symbol-placement': 'line',
          'text-max-angle': 45,
          'text-size': [
            'interpolate',
            ['linear'],
            ['zoom'],
            10,
            8,
            15,
            11,
            22,
            28
          ],
          'text-font': ['Noto Sans Regular']
        },
        'paint': {
          'text-halo-color': 'hsl(0, 0%, 100%)',
          'text-halo-width': 1,
          'text-halo-blur': 1,
          'text-color': '#6a6f73'
        }
      },
      {
        'id': 'road names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'beaf4956fb8a63410ecf80abdebcdfb5'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'minzoom': 10,
        'filter': [
          'match',
          ['get', 'class'],
          ['primary', 'motorway'],
          false,
          true
        ],
        'layout': {
          'text-field': ['to-string', ['get', 'name']],
          'symbol-placement': 'line',
          'text-font': ['Noto Sans Regular'],
          'text-size': [
            'interpolate',
            ['linear'],
            ['zoom'],
            10,
            8,
            15,
            10,
            22,
            25
          ],
          'symbol-spacing': [
            'interpolate',
            ['linear'],
            ['zoom'],
            10,
            25,
            15,
            97,
            17,
            250
          ],
          'text-max-angle': 82,
          'text-padding': 1
        },
        'paint': {
          'text-halo-color': 'hsl(0, 0%, 100%)',
          'text-halo-width': 1,
          'text-halo-blur': 1,
          'text-color': '#6a6f73'
        }
      },
      {
        'id': 'primary road numbers',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'beaf4956fb8a63410ecf80abdebcdfb5'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'minzoom': 9,
        'filter': ['match', ['get', 'type'], ['Primary'], true, false],
        'layout': {
          'text-field': ['to-string', ['get', 'number']],
          'symbol-placement': 'line',
          'text-max-angle': 65,
          'text-size': [
            'interpolate',
            ['linear'],
            ['zoom'],
            9,
            8.5,
            15,
            12,
            22,
            28
          ],
          'text-font': ['Noto Semi Bold'],
          'text-letter-spacing': 0.1,
          'symbol-spacing': ['interpolate', ['linear'], ['zoom'], 9, 50, 15, 250],
          'visibility': 'visible'
        },
        'paint': {
          'text-halo-color': '#ffffff',
          'text-halo-width': 1.25,
          'text-halo-blur': 0,
          'text-color': '#6a6f73'
        }
      },
      {
        'id': 'motorway numbers',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'beaf4956fb8a63410ecf80abdebcdfb5'},
        'source': 'mapbox_streets',
        'source-layer': 'road',
        'minzoom': 8,
        'filter': ['match', ['get', 'class'], ['motorway'], true, false],
        'layout': {
          'text-field': ['to-string', ['get', 'number']],
          'symbol-placement': 'line',
          'text-max-angle': 45,
          'text-size': [
            'interpolate',
            ['linear'],
            ['zoom'],
            8,
            8.5,
            10,
            9,
            15,
            12,
            22,
            28
          ],
          'text-font': ['Noto Semi Bold'],
          'text-letter-spacing': 0.1,
          'symbol-spacing': ['interpolate', ['linear'], ['zoom'], 8, 50, 15, 250]
        },
        'paint': {
          'text-halo-color': '#ffffff',
          'text-halo-width': 1.25,
          'text-halo-blur': 0,
          'text-color': '#6a6f73'
        }
      },
      {
        'id': 'motorway junction numbers',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'names',
        'minzoom': 13,
        'filter': ['match', ['get', 'type'], ['Motorway Junctions'], true, false],
        'layout': {
          'text-field': ['to-string', ['get', 'name']],
          'text-size': [
            'interpolate',
            ['linear'],
            ['zoom'],
            13,
            11,
            16,
            16,
            22,
            30
          ],
          'text-font': ['Noto Bold']
        },
        'paint': {
          'text-color': '#ffffff',
          'text-halo-color': '#9c9c9c',
          'text-halo-width': 10
        }
      },
      {
        'id': 'greenspace names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'names',
        'minzoom': 13,
        'filter': ['match', ['get', 'type'], ['Greenspace'], true, false],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 13, 9, 14, 11],
          'text-font': ['Noto Sans Regular'],
          'text-line-height': 1
        },
        'paint': {
          'text-color': '#89a489',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1
        }
      },
      {
        'id': 'sites names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'poi_label',
        'minzoom': 13,
        'filter': ['match', ['get', 'class'], ['landmark'], false, true],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 13, 9, 14, 11],
          'text-font': ['Noto Sans Regular'],
          'text-line-height': 1
        },
        'paint': {
          'text-color': '#6a6f73',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1
        }
      },
      {
        'id': 'landform names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'names',
        'minzoom': 5,
        'filter': ['match', ['get', 'type'], ['Landform'], true, false],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 11, 9, 14, 11],
          'text-font': ['Noto Sans Regular'],
          'text-line-height': 1
        },
        'paint': {
          'text-color': '#6a6f73',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1
        }
      },
      {
        'id': 'landcover names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'names',
        'minzoom': 5,
        'filter': ['match', ['get', 'type'], ['Landcover'], true, false],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 11, 9.5, 14, 12],
          'text-font': ['Noto Sans Regular'],
          'text-line-height': 1
        },
        'paint': {
          'text-color': '#6a6f73',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1
        }
      },
      {
        'id': 'water names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'water',
        'minzoom': 12,
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 11, 9, 14, 11],
          'text-font': ['Noto Sans Italic'],
          'text-line-height': 1
        },
        'paint': {
          'text-color': '#6c8499',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1
        }
      },
      {
        'id': 'woodland names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'names',
        'minzoom': 5,
        'filter': ['match', ['get', 'type'], ['Woodland'], true, false],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 11, 9.5, 14, 11.5],
          'text-font': ['Noto Sans Regular'],
          'text-line-height': 1,
          'text-padding': ['interpolate', ['linear'], ['zoom'], 14, 10, 16, 2]
        },
        'paint': {
          'text-color': '#89a489',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1
        }
      },
      {
        'id': 'small settlement names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'names',
        'minzoom': 5,
        'filter': ['match', ['get', 'type'], ['Small Settlements'], true, false],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 12, 9, 14, 11],
          'text-font': ['Noto Sans Regular'],
          'text-line-height': 1
        },
        'paint': {
          'text-color': '#6a6f73',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1
        }
      },
      {
        'id': 'suburban area names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'names',
        'minzoom': 10,
        'filter': ['match', ['get', 'type'], ['Suburban Area'], true, false],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 10, 10.5, 14, 14],
          'text-font': ['Noto Sans Regular'],
          'text-line-height': 1,
          'text-padding': ['interpolate', ['linear'], ['zoom'], 10, 10, 14, 2]
        },
        'paint': {
          'text-color': '#6a6f73',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1,
          'text-opacity': ['interpolate', ['linear'], ['zoom'], 10, 0.8, 14, 1]
        }
      },
      {
        'id': 'railwaystations',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'transit_stop_label',
        'filter': [
          'all',
          ['match', ['get', 'stop_type'], ['station'], true, false]
        ],
        'layout': {
          'text-line-height': 1,
          'text-size': ['interpolate', ['linear'], ['zoom'], 12, 9, 15, 13],
          'icon-image': [
            'match',
            ['get', 'ma'],
            ['Railway Station'],
            'RS',
            ['London Underground Station'],
            'UG',
            ['Light Rapid Transit Station'],
            'LRTS',
            ['Light Rapid Transit Station And London Underground Station'],
            'LRTS-UG',
            ['Light Rapid Transit Station And Railway Station'],
            'RS-LRTS',
            ['Railway Station And London Underground Station'],
            'RS-UG',
            ''
          ],
          'text-font': ['Noto Sans Regular'],
          'text-justify': 'left',
          'text-offset': [
            'match',
            ['get', 'stop_type'],
            ['station'],
            ['literal', [1, 0]],
            ['Light Rapid Transit Station'],
            ['literal', [1, 0]],
            ['London Underground Station'],
            ['literal', [1, 0]],
            ['Railway Station And London Underground Station'],
            ['literal', [1.7, 0]],
            ['Light Rapid Transit Station And London Underground Station'],
            ['literal', [1.5, 0]],
            ['Light Rapid Transit Station And Railway Station'],
            ['literal', [1.7, 0]],
            ['literal', [0, 0]]
          ],
          'icon-size': ['interpolate', ['linear'], ['zoom'], 12, 0.5, 15, 1],
          'text-anchor': 'left',
          'text-field': ['to-string', ['get', 'name_en']]
        },
        'paint': {
          'text-halo-color': '#ffffff',
          'text-halo-width': 1,
          'text-halo-blur': 1,
          'text-color': '#6a6f73'
        }
      },
      {
        'id': 'airports',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'aeroway',
        'filter': ['match', ['get', 'type'], ['runway'], true, false],
        'layout': {
          'visibility': 'visible',
          'icon-image': 'Airport',
          'icon-size': ['interpolate', ['linear'], ['zoom'], 10, 0.8, 15, 1],
          'text-field': ['to-string', ['get', 'name_en']],
          'text-font': ['Noto Sans Regular'],
          'text-size': ['interpolate', ['linear'], ['zoom'], 10, 9, 15, 13],
          'text-justify': 'left',
          'text-anchor': 'left',
          'text-offset': [0.8, 0]
        },
        'paint': {
          'text-color': '#6a6f73',
          'text-halo-color': 'hsl(0, 0%, 100%)',
          'text-halo-width': 1,
          'text-halo-blur': 1
        }
      },
      {
        'id': 'village and hamlet names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'place_label',
        'minzoom': 11,
        'filter': [
          'all',
          ['match', ['get', 'type'], ['village', 'hamlet'], true, false]
        ],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 9, 9, 14, 15],
          'text-font': ['Noto Sans Regular'],
          'text-line-height': 1,
          'text-padding': 2,
          'visibility': 'visible'
        },
        'paint': {
          'text-color': '#203131',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1,
          'text-opacity': 1
        }
      },
      {
        'id': 'town names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'place_label',
        'minzoom': 9,
        'filter': ['all', ['match', ['get', 'type'], ['town'], true, false]],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 7, 10, 14, 18],
          'text-font': ['Noto Sans Regular'],
          'text-line-height': 1,
          'text-padding': 2,
          'visibility': 'visible'
        },
        'paint': {
          'text-color': '#203131',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1,
          'text-opacity': 1
        }
      },
      {
        'id': 'city names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'place_label',
        'minzoom': 5,
        'filter': ['all', ['match', ['get', 'type'], ['city'], true, false]],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 6, 10, 14, 20],
          'text-font': ['Noto Semi Bold'],
          'text-line-height': 1,
          'text-padding': 2,
          'text-letter-spacing': 0.05,
          'visibility': 'visible'
        },
        'paint': {
          'text-color': '#55595c',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1,
          'text-opacity': 1
        }
      },
      {
        'id': 'national park names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'landuse_overlay',
        'minzoom': 5,
        'filter': ['match', ['get', 'class'], ['national_park'], true, false],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 6, 8, 14, 15],
          'text-font': ['Noto Semi Bold'],
          'text-line-height': 1,
          'text-padding': 2,
          'text-letter-spacing': 0.06
        },
        'paint': {
          'text-color': '#89a489',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1,
          'text-opacity': 0.8
        }
      },
      {
        'id': 'capital-city-names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'place_label',
        'minzoom': 4,
        'filter': ['all', ['has', 'capital'], ['<=', 'capital', 4]],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 5, 10, 14, 22],
          'text-font': ['Noto Sans Regular'],
          'text-line-height': 1,
          'text-padding': 2,
          'text-letter-spacing': 0.1,
          'text-transform': 'uppercase'
        },
        'paint': {
          'text-color': '#203131',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1,
          'text-opacity': 0.7
        }
      },
      {
        'id': 'state-names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'place_label',
        'minzoom': 3,
        'maxzoom': 10,
        'filter': ['all', ['match', ['get', 'type'], ['state'], true, false]],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': ['interpolate', ['linear'], ['zoom'], 5, 12, 10, 36],
          'text-font': ['Noto Serif'],
          'text-line-height': 1,
          'text-padding': 16,
          'text-letter-spacing': 0.3,
          'text-transform': 'uppercase',
          'visibility': 'visible'
        },
        'paint': {
          'text-color': '#203131',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1,
          'text-opacity': 0.6
        }
      },
      {
        'id': 'country-names',
        'type': 'symbol',
        'metadata': {'mapbox:group': 'e196265c0e550aaddd2885dc32fdb674'},
        'source': 'mapbox_streets',
        'source-layer': 'place_label',
        'minzoom': 1,
        'maxzoom': 9,
        'filter': ['all', ['match', ['get', 'type'], ['country'], true, false]],
        'layout': {
          'text-field': ['to-string', ['get', 'name_en']],
          'text-size': [
            'interpolate',
            ['linear'],
            ['zoom'],
            2,
            12,
            6,
            32,
            10,
            36
          ],
          'text-font': ['Noto Serif Bold'],
          'text-line-height': 1,
          'text-letter-spacing': 0.3,
          'text-transform': 'uppercase',
          'visibility': 'visible',
          'text-max-width': 14,
          'text-padding': 8
        },
        'paint': {
          'text-color': '#203131',
          'text-halo-color': '#f1efec',
          'text-halo-width': 1,
          'text-halo-blur': 1,
          'text-opacity': 0.6
        }
      }
    ],
    'id': 'hquacmmep'
  }
;
