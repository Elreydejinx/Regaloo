const i18n = require('i18n');

i18n.configure({
    locales: ['en', 'es'],
    directory: __dirname + '/locales',
    defaultLocale: 'en',
    autoReload: true,
    syncFiles: true,
    queryParameter: 'lang',
    objectNotation: true
});

module.exports = i18n;