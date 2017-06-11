
function loadData() {
    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // load streetview  
    var streetStr =  $('#street').val();
    var cityStr = $('#city').val();
    var address = streetStr + ', ' + cityStr;

    $greeting.text("Welcome to fabulous " + address);

    var streetviewUrl = 'http://maps.googleapis.com/maps/api/' +
                        'streetview?size=600x300&location=' +
                        address + '';

    console.log(streetviewUrl);
    console.log(address);
    $body.append('<img class="bgimg" src="' + streetviewUrl + '">');
    $body.append('<img class="bgimg" src=');

    // YOUR CODE GOES HERE!
   
    var nyTimeUrl = "https://api.nytimes.com/svc/search/v2/" +
        "articlesearch.json?q=" + cityStr + "&sort=newest" +
        "&api-key=2414599ebca647e38cdf4ac8bf8cd908";
    console.log(nyTimeUrl);

    $.getJSON(nyTimeUrl, function (data) {
        $nytHeaderElem.text('New York Times Article About ' + cityStr)
        var articles = data.response.docs;
        for (var i = 0; i < articles.length; i++) {
            var article = articles[i];
            $nytElem.append('<li class="article">' +
                '<a href="' + article.web_url + '">' + article.headline.main +
                '</a>' +
                '<p>' + article.snippet + '</p>' +
                '</li>');
        };
    }).error(function (e) {
        $nytHeaderElem.text("Sorry, we could not get any articles!");
    });
    var wikiUrl = "https://en.wikipedia.org/w/api.php?action=opensearch&search=" + cityStr + "&format=json&callback=wikiCallback";
    console.log(wikiUrl);

    var wikiRequestTimeout = setTimeout(function () {
        $wikiElem.text("Failed to get wikipedia resources");
    }, 8000);

    $.ajax({
        url: wikiUrl,
        dataType: "jsonp",
        success: function (response) {
            var articleList = response[1];

            for (var i = 0; i < articleList.length; i++) {
                articleStr = articleList[i];
                var url = 'http://en.wikipedia.org/wiki/' + articleStr;
                $wikiElem.append('<li><a href="' + url + '">' +
                    articleStr + '</a></li>');
            };
            clearTimeout(wikiRequestTimeout);
        }
    });
    return false;
};

$('#form-container').submit(loadData);
//$("#submit-btn").click(function(){
//    alert("The paragraph was clicked.");
//});
