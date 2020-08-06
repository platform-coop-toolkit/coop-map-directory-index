const mix = require('laravel-mix');
const globby = require('globby');
const CopyPlugin = require('copy-webpack-plugin');

require('laravel-mix-svelte');

const distDir = './maps/static/maps/dist';

mix.setPublicPath(distDir);

mix.browserSync({
    proxy: 'localhost:8000',
    open: false
});

mix.sass('maps/static/maps/css/app.scss', `${distDir}/css/`, {
    sassOptions: {
        includePaths: [path.join(__dirname, 'node_modules')],   
    }
});

mix.js('maps/static/maps/js/app.js', `${distDir}/js/`);
mix.js('maps/static/maps/js/impact.js', `${distDir}/js/`).svelte();

mix.copyDirectory('node_modules/@platform-coop-toolkit/pinecone/src/assets/images', `${distDir}/images`)
    .copyDirectory('maps/static/maps/images', `${distDir}/images`)
    .copyDirectory('node_modules/@platform-coop-toolkit/pinecone/src/assets/fonts', `${distDir}/fonts`)
    .copyDirectory('maps/static/maps/styles/glyphs', `${distDir}/styles/glyphs`);

/*
 We need to individually copy all files in the styles/pcc directory, excluding style.json,
 so that we don't overwrite the file copied with string replacements below.
*/
(async () => {
  const paths = await globby([
    `maps/static/maps/styles/${process.env.MAP_STYLE}/*`,
    `!maps/static/maps/styles/${process.env.MAP_STYLE}/style.json`
  ]);
  paths.forEach(path => {
    mix.copy(path, `${distDir}/styles/pcc/`);
  });
})();

/*
 The laravel-mix-string-replace package only works on processed files.
 Since we are copying the JSON file, we need to use a custom Webpack configuration.
*/
mix.webpackConfig({
  plugins: [
    new CopyPlugin({
      patterns: [
        {
          from: `maps/static/maps/styles/${process.env.MAP_STYLE}/style.json`,
          to: path.join(__dirname, `${distDir}/styles/pcc/`),
          transform(content) {
            let str = content.toString();
            str = str.replace(
              /"sprite": ".*\/static\/maps\/dist\/styles\/.*\/sprites",/,
              `"sprite": "${process.env.MAP_ASSETS_BASE_URL}/static/maps/dist/styles/${process.env.MAP_STYLE}/sprites",`
            );
            str = str.replace(
              /"glyphs": ".*\/glyphs\/{fontstack}\/{range}.pbf",/,
              `"glyphs": "${process.env.MAP_ASSETS_BASE_URL}/static/maps/dist/styles/glyphs/{fontstack}/{range}.pbf",`
            );
            return str;
          },
        },
      ],
    })
  ]
});

mix.options({
    processCssUrls: false,
});

if (mix.inProduction()) {
  mix.version();
} else {
  mix.sourceMaps(false, 'source-map');
}
