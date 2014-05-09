var app = angular.module('zenfeed', ['ngRoute']);

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
