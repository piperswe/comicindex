/* eslint-disable indent */
module.exports = {
  pwa: {
    name: 'comicindex browser',
  },

  publicPath: '/comicindex/browser',

  chainWebpack(config) {
    const sqlRule = config.module.rule('sql');
    sqlRule.test(/\.sql$/).use('url-loader').loader('url-loader');
  },
};
