export const generateCards = (map, layers) => {
  let visibleFeatures = map.queryRenderedFeatures({layers: layers});
  if (visibleFeatures) {
    let htmlString = '<ul class="cards">\n';
    visibleFeatures.forEach(function (f) {
      htmlString += `<li class="card__wrapper"><article id="${f.id}" class="card"><header><h3 class="card___title"><span class="card__format">${f.properties.categories.replace('[', '').replace(']', '').replace(/","/g, ', ').replace(/"/g, '').toUpperCase()}</span><span class="screen-reader-text">: </span></h3></header><aside class="card__aside">\n<h4>${f.properties.name}</h4><br />`;
      if (f.properties.sectors) {
        htmlString += `<strong>${f.properties.sectors.replace('[', '').replace(']', '').replace(/","/g, ', ').replace(/"/g, '')}</strong><br />`;
      }
      if (f.properties.city) {
        htmlString += `${f.properties.city} `;
      }
      if (f.properties.state) {
        htmlString += `${f.properties.state} `;
      }
      if (f.properties.country) {
        htmlString += `${f.properties.country}`;
      }
      htmlString += '</aside></article></li>';
    });
    htmlString += '</ul>';
    document.getElementById('visibles').innerHTML = htmlString;

    [...document.getElementsByTagName('article')].forEach(function (article) {
      article.addEventListener('click', function () {
        window.location = `/organizations/${article.id}`;
      });
    });
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
    htmlString += `${f.properties.address}<br />`
  }
  if (f.properties.city) {
    htmlString += `${f.properties.city} `
  }
  if (f.properties.state) {
    htmlString += `${f.properties.state} `
  }
  if (f.properties.postal_code) {
    htmlString += `${f.properties.postal_code} `
  }
  if (f.properties.country) {
    htmlString += `${f.properties.country} `
  }
  if (f.properties.type || f.properties.categories || f.properties.sectors) {
    htmlString += '<hr>';
  }
  if (f.properties.type) {
    htmlString += `Type: ${f.properties.type}<br />`
  }
  if (f.properties.categories) {
    htmlString += `Category: ${f.properties.categories.replace('[', '').replace(']', '').replace(/","/g, ', ').replace(/"/g, '')}`;
  }
  if (f.properties.sectors) {
    htmlString += `Sectors: ${f.properties.sectors.replace('[', '').replace(']', '').replace(/","/g, ', ').replace(/"/g, '')}`;
  }
  return htmlString;
};
