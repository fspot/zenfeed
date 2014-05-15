var app = angular.module('zenfeed', ['ngRoute', 'pascalprecht.translate']);

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
        'EDITFEED.HIGHLIGHT': 'Surligner quand mis à jour'
    });


    var browserLanguage = window.navigator.userLanguage || window.navigator.language || 'en';
    browserLanguage = browserLanguage.split('-')[0]; // ignore variations like fr-FR, fr-CA..
    $translateProvider.preferredLanguage(browserLanguage);
    $translateProvider.fallbackLanguage('en');
}]);

app.service('Feed', function($http) {
    var feedApiUrl = "/api/feed/";

    this.refetch = function() {
        return $http.get(feedApiUrl);
    };

    this.findFeed = function(feedId) {
        for (var i = 0; i < this._cached.length; i++) {
            if (this._cached[i].id === +feedId) return this._cached[i];
        }
        return null;
    };

    this.postFeed = function(url) {
        var urlObj = {"url": url};
        return $http.post(feedApiUrl + 'add/', urlObj);
    };

    this.deleteFeed = function(feedId) {
        var idObj = {"id": +feedId};
        return $http.post(feedApiUrl + 'delete/', idObj);
    };

    this.addFeed = function(feed) {
        this._cached.push(feed);
    };

    this.removeFeed = function(feedId) {
        this._cached = this._cached.filter(function(feed) {
            return (+feed.id !== +feedId);
        });
    };

    this._cached = null;
    this.cache = function(obj) { this._cached = obj; };
    this.cached = function() { return this._cached; };
});

app.service('Config', function($http) {
	var configApiUrl = "/api/config/";

    this.refetch = function() {
    	return $http.get(configApiUrl);
    };

    this.save = function(config) {
    	return $http.post(configApiUrl, config);
    };
});

app.config(function($routeProvider) {
	$routeProvider
	.when('/config', {
		controller:'ConfigCtrl',
		templateUrl:'config.html'
	})
	.when('/feed/edit/:feedId', {
		controller:'EditFeedCtrl',
		templateUrl:'edit_feed.html'
	})
    .when('/feed/add', {
        controller:'AddFeedCtrl',
        templateUrl:'add_feed.html'
    })
	.when('/feed', {
		controller:'FeedCtrl',
		templateUrl:'feed.html'
	})
	.otherwise({
		redirectTo:'/config'
	});
});

app.controller('FeedCtrl', function($scope, $translate, Feed) {
    $scope.refetch = function() {
        Feed.refetch()
        .success(function(data, status, headers, cfg) {
            $scope.feeds = data.feeds;
            Feed.cache(data.feeds);
        }).error(function(data, status, headers, cfg) {
            alert('error during refetch() : ' + status);
        });
    };

    $scope.deleteFeed = function(feedId) {
        $translate('FEEDS.CONFIRMDELETE').then(function (confirmMsg) {
            if (confirm(confirmMsg)) {
                Feed.deleteFeed(feedId)
                .success(function(data, status, headers, cfg) {
                    Feed.removeFeed(feedId);
                    $scope.feeds = Feed.cached();
                }).error(function(data, status, headers, cfg) {
                    alert('error during deleteFeed() : ' + status);
                });
            }
        });
    };

    $scope.init = function() {
        $scope.sortOrder = '-updated';
        if (Feed.cached() === null) $scope.refetch();
        else $scope.feeds = Feed.cached();
    };
});

app.controller('EditFeedCtrl', function($scope, $routeParams, Feed) {
    $scope.refetch = function() {
        Feed.refetch()
        .success(function(data, status, headers, cfg) {
            Feed.cache(data.feeds);
            $scope.feed = Feed.findFeed($scope.feedId);
        }).error(function(data, status, headers, cfg) {
            alert('error during refetch() : ' + status);
        });
    };

    $scope.init = function() {
        $scope.feedId = $routeParams.feedId;
        if (Feed.cached() === null) $scope.refetch();
        else $scope.feed = Feed.findFeed($scope.feedId);
    };
});

app.controller('AddFeedCtrl', function($scope, $location, Feed) {

    $scope.addFeed = function() {
        $scope.isFetching = true;

        Feed.postFeed($scope.url)
        .success(function(data, status, headers, cfg) {
            Feed.addFeed(data.feed);
            $location.path('/feed/edit/' + data.feed.id);
        }).error(function(data, status, headers, cfg) {
            alert('error during addFeed() : ' + status);
        })['finally'](function() {
            $scope.isFetching = false;
        });
    };

    $scope.init = function() {
        $scope.isFetching = Feed.cached() === null;
    };
});

app.controller('ConfigCtrl', function($scope, Config) {
    $scope.refetch = function() {
    	Config.refetch()
    	.success(function(data, status, headers, cfg) {
    	    $scope.config = data;
    	}).error(function(data, status, headers, cfg) {
    	    alert('error during refetch() : ' + status);
    	});
    };

    $scope.saveConfig = function() {
    	Config.save($scope.config)
    	.success(function(data, status, headers, cfg) {
    	    alert('Status : ' + data.msg);
    	    if ($scope.config.pw) window.location.reload();
    	}).error(function(data, status, headers, cfg) {
    	    alert('error during saveConfig() : ' + status);
    	});
    };

    $scope.refetch();
});