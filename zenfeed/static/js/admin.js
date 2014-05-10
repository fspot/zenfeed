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
        'FEED.TITLE': 'Feeds'
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
        'FEED.TITLE': 'Flux'
    });


    var browserLanguage = window.navigator.userLanguage || window.navigator.language || 'en';
    browserLanguage = browserLanguage.split('-')[0]; // ignore variations like fr-FR, fr-CA..
    $translateProvider.preferredLanguage(browserLanguage);
    $translateProvider.fallbackLanguage('en');
}]);

app.service('Feed', function() {
    this.name = "Anonymous";
    this.id = null;
    this.all = function() {
    	return ["1", "2", "3", "4"];
    };
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
	.when('/', {
		controller:'ConfigCtrl',
		templateUrl:'config.html'
	})
	// .when('/edit/:projectId', {
	// 	controller:'EditCtrl',
	// 	templateUrl:'detail.html'
	// })
	.when('/feed', {
		controller:'FeedCtrl',
		templateUrl:'feed.html'
	})
	.otherwise({
		redirectTo:'/'
	});
});

app.controller('FeedCtrl', function($scope, Feed) {
    $scope.feeds = [
    	{text: "1"}, {text: "2"}, {text: "3"}
    ];

    $scope.addFeed = function() {
        $scope.feeds.push({text: $scope.feedText});
        $scope.feedText = '';
    };
});

app.controller('ConfigCtrl', function($scope, Config) {
    $scope.refetch = function() {
    	console.log("refreshing");
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
    	    console.log($scope.config);
    	    if ($scope.config.pw) window.location.reload();
    	}).error(function(data, status, headers, cfg) {
    	    alert('error during saveConfig() : ' + status);
    	});
    };

    $scope.refetch();
});
