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
		redirectTo:'/feed'
	});
});
