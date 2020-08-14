import Cards from './components/Cards.svelte';
import { features } from './store.js';

/**
 * Instantiate the Svelte container for organization and individual cards below the map.
 */
export const generateCards = () => {
  new Cards({
    target: document.getElementById('visibles')
  });
};

/**
 * 
 * @param {mapboxgl.Map} map The main map instance.
 * @param {Array} layers The layers to search for features in the current map view.
 */
export const updateStore = (map, layers) => {
  let visibleFeatures = map.queryRenderedFeatures({layers: layers});
  if (visibleFeatures) {
    features.set(visibleFeatures);
  }
};

export const generatePopupHtml = (f) => {
  let
    htmlString = '';
  if (f.properties.url) {
    htmlString += `<strong><a href="${f.properties.url}">${f.properties.name}</a></strong><br />`;
  } else {
    htmlString += `<strong>${f.properties.name}</strong><br />`;
  }
  if (f.properties.address) {
    htmlString += `${f.properties.address}<br />`;
  }
  if (f.properties.city) {
    htmlString += `${f.properties.city} `;
  }
  if (f.properties.state) {
    htmlString += `${f.properties.state} `;
  }
  if (f.properties.postal_code) {
    htmlString += `${f.properties.postal_code} `;
  }
  if (f.properties.country) {
    const c = JSON.parse(f.properties.country);
    htmlString += `${c.name} `;
  }
  if (f.properties.type || f.properties.categories || f.properties.sectors) {
    htmlString += '<hr>';
  }
  if (f.properties.type) {
    htmlString += `Type: ${f.properties.type}<br />`;
  }
  if (f.properties.categories) {
    htmlString += `Category: ${f.properties.categories.replace('[', '').replace(']', '').replace(/","/g, ', ').replace(/"/g, '')}`;
  }
  if (f.properties.sectors) {
    htmlString += `Sectors: ${f.properties.sectors.replace('[', '').replace(']', '').replace(/","/g, ', ').replace(/"/g, '')}`;
  }
  return htmlString;
};
