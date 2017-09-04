var map;
var markers = [];

//contains the data to be used
var myLocations = [

    {title: 'Rock & Roll Sushi Station',  location:{lat:35.5371903, lng:-97.6016389, streetAddress:'4501 NW 63rd St', cityAddress:'Oklahoma City, OK 73132'}} ,
    {title: 'El Fogon de Edgar',  location:{lat:35.493049, lng:-97.555724, streetAddress:'2416 NW 23rd St', cityAddress:'Oklahoma City, OK 73107'}},
    {title: 'Hanks Coffee',  location:{lat:35.4811162, lng:-97.5212462, streetAddress:'1227 N Walker Ave', cityAddress:'Oklahoma City, OK 73103'}},
    {title: 'Cafe Kao Cao',  location:{lat:35.5039125, lng:-97.5346584 , streetAddress:'3325 N Classen Blvd', cityAddress:'Oklahoma City, OK 73118'}},
    {title: 'Couscous Cafe',  location:{lat:35.5347062, lng:-97.5662244, streetAddress:'6165 N May Ave', cityAddress:'Oklahoma City, OK 73112'}},
    {title: 'Ingrids',  location:{lat:35.507901, lng:-97.5523263, streetAddress:'3701 N Youngs Blvd', cityAddress:'Oklahoma City, OK 73112'}}
];

function init() {
    // Constructor creates a new map - only center and zoom are required.
    map = new google.maps.Map(document.getElementById('map'), {
        center: myLocations[5].location,
        zoom: 13
    });
    //passes the map object to set markers from myLocations
    setMarkers(map);
};


function setMarkersOld(myLocations){
    // Style the markers a bit. This will be our listing marker icon.
    //var defaultIcon = makeMarkerIcon('0091ff');

    // Create a "highlighted location" marker color for when the user
    // mouses over the marker.
    //var highlightedIcon = makeMarkerIcon('FFFF24');

    // The following group uses the location array to create an array of markers on initialize.
    for (var i = 0; i < myLocations.length; i++) {
        // Get the position from the location array.
        var position = myLocations[i].location;
        var title = myLocations[i].title;
        // Create a marker per location, and put into markers array.
        var marker = new google.maps.Marker({
            position: position,
            title: title,
            animation: google.maps.Animation.DROP,
            //icon: defaultIcon,
            id: i
        });
        // Push the marker to our array of markers.
        markers.push(marker);
    }
}

//helper function for init method
function setMarkers(map){
    //Adds marker to the map
    for(var i = 0; i < myLocations.length; i++){
        var myLocation = myLocations[i];
        var position = myLocation.location;
        var title = myLocation.title;
        var marker = new google.maps.Marker({
            position:position,
            map:map,
            title: title 
        });
        var infowindow = new google.maps.InfoWindow({
            content: "words" + i
        });
        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });
    }
}

//the object to be called from the view mode
//this will have the properties for the view to access
//data method contain properties of myLocations
var Marker = function(data){
    this.title = ko.observable(data.title);
};

//contains information for the focus
var ViewModel = function(){
    var self = this;
    //contain the list
    self.markerList = ko.observableArray([]);
    //takes data and push it to the list
    myLocations.forEach(function(markerItem){
        self.markerList.push( new Marker(markerItem));
    });

    self.query = ko.observable("");
    self.filteredMarkerList = ko.computed(function(){
        var filter = self.query().toLowerCase();
        if(!filter){
            return self.markerList();
        }
        else{
            return ko.utils.arrayFilter(self.markerList(), function(item){
                return item.title().toLowerCase().indexOf(filter) !== -1;
            });
        }
    });

    //property that contains an active marker
    //the defa being the first item in the list
    this.currentMarker = ko.observable(this.markerList()[0]);
    //clicking a list item will change the property currentMarker
    this.setMarker = function(clickedMarker){
        self.currentMarker(clickedMarker);
    };
};


ko.applyBindings(new ViewModel());
