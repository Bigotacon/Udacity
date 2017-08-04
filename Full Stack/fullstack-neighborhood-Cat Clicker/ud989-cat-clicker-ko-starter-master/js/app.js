var Cat = function(){
    this.clickCount = ko.observable(0);
    this.name = ko.observable('Tabby');
    this.imgSrc = ko.observable('img/434164568_fea0ad4013_z.jpg');
    this.imgAttribution = ko.observable('https://www.flickr.com/photos/big');
    this.nicknames = ko.observableArray(["Nina", "Pinta", "Santa Maria"]);
    this.level = ko.computed(function(){
        var level;
        var clicks = this.clickCount();
        switch(clicks)
        {
            case 0:
                return "Kitten";
            case 5:
                return "Lint Pouncer";
            case 10:
                return "Mouse Chaser";
            case 20:
                return "Assasin";
            case 50:
                return "Master";
            default:
                return this.level();
        }
    },this);
}

var ViewModel = function(){
    this.currentCat = ko.observable( new Cat() );
    this.incrementCounter = function() {
        this.clickCount(this.clickCount() +1 );
    };
}
ko.applyBindings(new ViewModel());
