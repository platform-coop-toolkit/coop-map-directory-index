import Cards from './components/Cards.svelte';
import Popup from './components/Popup.svelte';
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
  const popup = document.createElement('div');
  new Popup({
    target: popup,
    props: {
      feature: f
    }
  });
  return popup.innerHTML;
};
