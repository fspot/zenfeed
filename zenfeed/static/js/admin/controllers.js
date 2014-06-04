app.controller('FeedCtrl', function($scope, $translate, Feed, pathPrefix) {
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
        $scope.pathPrefix = pathPrefix;
        $scope.sortOrder = '-updated';
        if (Feed.cached() === null) $scope.refetch();
        else $scope.feeds = Feed.cached();
    };
});

app.controller('EditFeedCtrl', function($scope, $routeParams, Feed, pathPrefix) {
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
        $scope.pathPrefix = pathPrefix;
        $scope.feedId = $routeParams.feedId;
        if (Feed.cached() === null) $scope.refetch();
        else $scope.feed = Feed.findFeed($scope.feedId);
    };

    $scope.saveFeed = function() {
        Feed.save($scope.feed)
        .success(function(data, status, headers, cfg) {
            alert('Status : ' + data.msg);
        }).error(function(data, status, headers, cfg) {
            alert('error during saveFeed() : ' + status);
        });
    };
});

app.controller('AddFeedCtrl', function($scope, $location, Feed, pathPrefix) {

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
        $scope.pathPrefix = pathPrefix;
        $scope.isFetching = Feed.cached() === null;
    };
});

app.controller('ConfigCtrl', function($scope, Config, pathPrefix) {
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

    $scope.pathPrefix = pathPrefix;
    $scope.refetch();
});
