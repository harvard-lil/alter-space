var path = require('path');

module.exports = {
  assetsDir: 'static',
  outputDir: path.resolve(__dirname, '../dist'),
  runtimeCompiler: true,
  configureWebpack: {
    devtool: 'source-map'
    //
  }
};
