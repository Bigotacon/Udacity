var initialCats = [
    {
        clickCount: 0,
        name: 'Tabby',
        imgSrc:'img/434164568_fea0ad4013_z.jpg',
        imgAttribution: 'https:www.flickr.com/photos/bigtallguy/434164568',
        nicknames: ["Nina", "Pinta", "Santa Maria"]
    },
    {
        clickCount: 0,
        name: 'Tiger',
        imgSrc:'img/4154543904_6e2428c421_z.jpg',
        imgAttribution: 'https:www.flickr.com/photos/bigtallguy/434164568',
        nicknames: ["Tigger"]
    },
    {
        clickCount: 0,
        name: 'Scaredy',
        imgSrc: 'img/22252709_010df3379e_z.jpg',
        imgAttribution: 'https:www.flickr.com/ph otos/bigtallguy/434164568',
        nicknames: ["Lion"]
    },
    {
        clickCount: 0,
        name: 'Shadow',
        imgSrc:'img/1413379559_412a540d29_z.jpg',
        imgAttribution: 'https:www.flickr.com/photos/bigtallguy/434164568',
        nicknames: ["Ninja"]
    },
    {
        clickCount: 0,
        name: 'Sleepy',
        imgSrc:'img/9648464288_2516b35537_z.jpg',
        imgAttribution: 'https:www.flickr.com/photos/bigtallguy/434164568',
        nicknames: ["Zzzzzz"]
    }
];

var Cat = function(data){
    this.clickCount = ko.observable(data.clickCount);
    this.name = ko.observable(data.name);
    this.imgSrc = ko.observable(data.imgSrc);
    this.imgAttribution = ko.observable(data.imgAttribution);
    this.nicknames = ko.observableArray(data.nicknames);
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
    var self = this;
    this.catList = ko.observableArray([]);
    initialCats.forEach(function(catItem){
        self.catList.push( new Cat(catItem));
    });
    this.currentCat = ko.observable(this.catList()[0]);
    this.incrementCounter = function() {
        self.currentCat().clickCount(self.currentCat().clickCount()+1);
        };
    this.setCat = function(clickedCat){
        self.currentCat(clickedCat);
    };
}
ko.applyBindings(new ViewModel());
