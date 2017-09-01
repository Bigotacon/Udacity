var map;

function init() {
    // Constructor creates a new map - only center and zoom are required.
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 40.7413549, lng: -73.9980244},
        zoom: 13
    });
};

//contains the data to be used
var initialMarkers = [
   {title: 'Spring Condominiuniums', location: {lat:30.268819, lng:-97.753838}},
    {title: 'Vista Hill Luxury Condiniums', location: {lat:30.252844, lng:-97.875664}},
    {title: '360 Condominiums', location: {lat:30.267056, lng:-97.749750}},
    {title: 'W Austin', location: {lat:30.265723, lng:-97.746747}},
    {title: 'Four Seasons', location: {lat:30.261675, lng:-97.742270}},
    {title: 'Omni Austin', location: {lat:30.270772, lng:-97.740369}}
];

//the object to be called from the view mode
//this will have the properties for the view to access
//data method contain properties of initialMarkers
var Marker = function(data){
    this.title = ko.observable(data.title);
};

//contains information for the focus
var ViewModel = function(){
    var self = this;
    //contain the list
    this.markerList = ko.observableArray([]);
    //takes data and push it to the list
    initialMarkers.forEach(function(markerItem){
        self.markerList.push( new Marker(markerItem));
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
