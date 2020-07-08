const mix = require('laravel-mix');
const webpack = require('webpack');


mix.setPublicPath('./maps/static/maps/dist');

mix.browserSync({
    proxy: 'localhost:8000',
    open: false
});

mix.sass('maps/static/maps/css/app.scss', 'maps/static/maps/dist/css/', {
    sassOptions: {
        includePaths: [path.join(__dirname, 'node_modules')],   
    },
});

mix.js('maps/static/maps/js/app.js', 'maps/static/maps/dist/js/');

mix.copy('node_modules/@platform-coop-toolkit/pinecone/src/assets/images', 'maps/static/maps/dist/images')
    .copy('maps/static/maps/images', 'maps/static/maps/dist/images') // Temporary.
    .copy('node_modules/@platform-coop-toolkit/pinecone/src/assets/fonts', 'maps/static/maps/dist/fonts');

mix.copyDirectory('maps/static/maps/styles', 'maps/static/maps/dist/styles');

mix.options({
    processCssUrls: false,
});

mix.sourceMaps(false, 'source-map');

mix.version();

mix.webpackConfig({
    plugins: [
        new webpack.DefinePlugin({
            'process.env.BASE_URL': (process.env.BASE_URL) ? JSON.stringify(process.env.BASE_URL) : JSON.stringify('https://directory.platform.coop')
        })
    ]
});

// Full API
// mix.js(src, output);
// mix.react(src, output); <-- Identical to mix.js(), but registers React Babel compilation.
// mix.preact(src, output); <-- Identical to mix.js(), but registers Preact compilation.
// mix.coffee(src, output); <-- Identical to mix.js(), but registers CoffeeScript compilation.
// mix.ts(src, output); <-- TypeScript support. Requires tsconfig.json to exist in the same folder as webpack.mix.js
// mix.extract(vendorLibs);
// mix.sass(src, output);
// mix.less(src, output);
// mix.stylus(src, output);
// mix.postCss(src, output, [require('postcss-some-plugin')()]);
// mix.browserSync('my-site.test');
// mix.combine(files, destination);
// mix.babel(files, destination); <-- Identical to mix.combine(), but also includes Babel compilation.
// mix.copy(from, to);
// mix.copyDirectory(fromDir, toDir);
// mix.minify(file);
// mix.sourceMaps(); // Enable sourcemaps
// mix.version(); // Enable versioning.
// mix.disableNotifications();
// mix.setPublicPath('path/to/public');
// mix.setResourceRoot('prefix/for/resource/locators');
// mix.autoload({}); <-- Will be passed to Webpack's ProvidePlugin.
// mix.babelConfig({}); <-- Merge extra Babel configuration (plugins, etc.) with Mix's default.
// mix.then(function () {}) <-- Will be triggered each time Webpack finishes building.
// mix.override(function (webpackConfig) {}) <-- Will be triggered once the webpack config object has been fully generated by Mix.
// mix.dump(); <-- Dump the generated webpack config object to the console.
// mix.extend(name, handler) <-- Extend Mix's API with your own components.
// mix.options({
//   extractVueStyles: false, // Extract .vue component styling to file, rather than inline.
//   globalVueStyles: file, // Variables file to be imported in every component.
//   processCssUrls: true, // Process/optimize relative stylesheet url()'s. Set to false, if you don't want them touched.
//   purifyCss: false, // Remove unused CSS selectors.
//   terser: {}, // Terser-specific options. https://github.com/webpack-contrib/terser-webpack-plugin#options
//   postCss: [] // Post-CSS options: https://github.com/postcss/postcss/blob/master/docs/plugins.md
// });
