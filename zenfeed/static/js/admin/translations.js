app.config(['$translateProvider', function ($translateProvider) {
    $translateProvider.translations('en', {
        'MENU.SETTINGS': 'Settings',
        'MENU.FEEDS': 'Feeds',
        'MENU.LOG_OUT': 'Log out',
        'CONFIG.TITLE': 'General and default settings',
        'CONFIG.LOGIN': 'Login',
        'CONFIG.PASSWORD': 'Password',
        'CONFIG.PASSWORD.PLACEHOLDER': 'Leave blank for no change',
        'CONFIG.PASSWORD.DETAILS': 'You will need to log in again after this operation.',
        'CONFIG.TIME_INTERVAL': 'Default refresh time interval',
        'CONFIG.MAXENTRIES': 'Default maximum entries number',
        'CONFIG.ENTRIES_PER_PAGE': 'Default entries number per page',
        'CONFIG.HIGHLIGHT': 'Highlight updated feeds by default',
        'CONFIG.SAVE': 'Save',
        'CONFIG.REFETCH': 'Refetch',
        'FEEDS.TITLE': 'Feed list',
        'FEEDS.NEW': '+ New',
        'FEEDS.IMPORT': 'Import',
        'FEEDS.EXPORT': 'Export',
        'FEEDS.CONFIRMDELETE': 'All data associated with this feed will be deleted. Continue ?',
        'ADDFEED.ADD': 'Add',
        'ADDFEED.NOTE': 'For some heavy feeds, downloading and processing may need several minutes !',
        'ADDFEED.TITLE': 'Add a feed',
        'EDITFEED.URL': 'Feed URL',
        'EDITFEED.TITLE': 'Title',
        'EDITFEED.LINK': 'Link',
        'EDITFEED.REFRESHINTERVAL': 'Refresh time interval',
        'EDITFEED.MAXENTRIES': 'Max entries number',
        'EDITFEED.ENTRIES_PER_PAGE' : 'Entries per page',
        'EDITFEED.HIGHLIGHT': 'Highlight news'
    });

    $translateProvider.translations('fr', {
        'MENU.SETTINGS': 'Paramètres',
        'MENU.FEEDS': 'Flux',
        'MENU.LOG_OUT': 'Se déconnecter',
        'CONFIG.TITLE': 'Paramètres généraux et par défaut',
        'CONFIG.LOGIN': 'Identifiant',
        'CONFIG.PASSWORD': 'Mot de passe',
        'CONFIG.PASSWORD.PLACEHOLDER': "Laisser vide pour conserver l'ancien",
        'CONFIG.PASSWORD.DETAILS': 'Une reconnexion sera nécessaire suite à cette opération.',
        'CONFIG.TIME_INTERVAL': 'Intervalle de rafraîchissement des flux',
        'CONFIG.MAXENTRIES': "Nombre maximal d'entrées par flux",
        'CONFIG.ENTRIES_PER_PAGE': "Nombre d'entrées par page",
        'CONFIG.HIGHLIGHT': 'Surligner les flux mis à jour',
        'CONFIG.SAVE': 'Enregistrer',
        'CONFIG.REFETCH': 'Rafraîchir',
        'FEEDS.TITLE': 'Liste des flux',
        'FEEDS.NEW': '+ Ajouter',
        'FEEDS.IMPORT': 'Importer',
        'FEEDS.EXPORT': 'Exporter',
        'FEEDS.CONFIRMDELETE': 'Toutes les données de ce flux seront supprimées. Continuer ?',
        'ADDFEED.ADD': 'Ajouter',
        'ADDFEED.NOTE': 'Certains flux très lourds peuvent mettre plusieurs minutes à être récupérés !',
        'ADDFEED.TITLE': 'Ajouter un flux',
        'EDITFEED.URL': 'URL du flux',
        'EDITFEED.TITLE': 'Titre',
        'EDITFEED.LINK': 'Lien',
        'EDITFEED.REFRESHINTERVAL': 'Intervalle de mise à jour',
        'EDITFEED.MAXENTRIES': "Nombre maximal d'entrées",
        'EDITFEED.ENTRIES_PER_PAGE' : "Nombre d'entrées par page",
        'EDITFEED.HIGHLIGHT': 'Surligner quand mis à jour'
    });


    var browserLanguage = window.navigator.userLanguage || window.navigator.language || 'en';
    browserLanguage = browserLanguage.split('-')[0]; // ignore variations like fr-FR, fr-CA..
    $translateProvider.preferredLanguage(browserLanguage);
    $translateProvider.fallbackLanguage('en');
}]);
