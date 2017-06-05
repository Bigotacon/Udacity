var skills =
[".NET", "C#","C++", "Python", "SQL", "HTML", "JavaScript", "CSS", "GIT"]

var bio = {
  "name" : "Joshua",
  "role" : "Application Developer",
  "contacts" : {
    "mobile" : "405-664-2575",
    "github" : "Bigotacon",
    "location" : "Oklahoma City"
  }
  "welcomeMessage" : "We hope you enjoy the show."
  "skills" : skills,
  "bioPic" : "images/fry.jpg"
}

var work = {};
work["position"] = "Application Developer";
work["years"] = 1;
work["city"] = "Oklahoma City";

var education = {};
education.name = "Rhode Island College";
education.years = "2009 - 2013";

$("#main").append(work.position);
$("#main").append(education["name"]);
console.log(work.position);

var education = {
  "schools" : [
    {
      "name" : "Rhode Island College",
      "city" : "Providence",
      "degree" : "BS",
      "major" : ["Economics", "Finance"],
      "year" : 2013
    },
    {
      "name" : "Community College of Rhode Island",
      "city" : "Newport",
      "degree" : "Associates",
      "major" : ["Finance"],
      "year" : 2010
    }
  ],
  "online courses": [
    "title" : ["Into to Computer Science", "Fullstack Web Development"],
    "school" : "Udacity",
    "dates" : 2017,
    "url" : "https://classroom.udacity.com/""https://classroom.udacity.com/"
  ]
}

var work = {
  "jobs" : [
    {
      "employer" : "AT&T",
      "title" : "Application Developer",
      "dates" : "July 2017 - Future",
      "desription" : "Full stack developer for AT&T systems. Also implements automation opportunities."
    },
    {
      "employer" : "AT&T",
      "title" : "Project Manager",
      "dates" : "September 2013 - July 2017",
      "desription" : "Interfaces with clients and oversees the implementation of telecommunicatoion services."
    }
  ]
}

var projects = {
  "projects" : [
    {
      "title" : "ECS Polling App",
      "dates" : "2017",
      "description" : "Fullstack developer for an Execuitve polling app. The project was made with MVC and uses C# .Net Framework The database is  SQL Server was used on the back end.",
      "images" : ""
    }
  ]
}
