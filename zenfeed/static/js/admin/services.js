app.service('Config', function($http, pathPrefix) {
    var configApiUrl = pathPrefix + "/api/config/";

    this.refetch = function() {
        return $http.get(configApiUrl);
    };

    this.save = function(config) {
        return $http.post(configApiUrl, config);
    };
});

app.service('Feed', function($http, pathPrefix) {
    var feedApiUrl = pathPrefix + "/api/feed/";

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

    this.save = function(feed) {
        return $http.post(feedApiUrl, feed);
    };

    this._cached = null;
    this.cache = function(obj) { this._cached = obj; };
    this.cached = function() { return this._cached; };
});
