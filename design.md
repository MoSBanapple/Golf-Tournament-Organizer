# Design Document

### Overview

This document covers the design of an application which allows users to organize and participate in golf tournaments, as well as keep track of player standings within said tournament. This application consists of two main components: the front end, which is an Android Application handles information input and output to and from the user, and the back end, which is a Google Datastore where data is held.

___

### User Interface

![Login screen](https://i.imgur.com/4M95uPj.png)

Login screen - This is the initial login screen that the user sees when they open the application. From here, they can enter their username and either attempt to log in or create a new account with the entered username. If the user attempts to create a new account with an existing username, they receive an appropriate error message. Once logged in, the user goes to the Available Tournaments page.

![Available tournaments](https://i.imgur.com/nXL5AIA.png)

Available tournaments - this screen contains a list of available tournaments. Each tournament shows basic details, as well as an indicator if the user is playing in, has played in, or is hosting the tournament. The user is able to sort by date ascending, descending, or put the tournaments they are participating in or hosting at the top. From here, the user is able to go to the tournament creation screen via the top right button or select a tournament to view more details.



![Tournament creation](https://i.imgur.com/yjCSBzx.png)

Tournament creation - The user can fill out the details of the tournament and create the tournament for players to enter. Once created, the user is taken to the “available tournaments” page, where the newly-created tournament should appear.

![Tournament details](https://i.imgur.com/Kzz9tfd.png)

Tournament details - Lists the details of the tournament, as well as the current scores standings. Players not yet in the tournament are able to join the tournament, and participating players are able to update their score within the tournament or leave the tournament. Standings are updated automatically whenever any player enters a new score. Users are able to look at standings on individual holes via a drop down hole select field. The tournament host is able to delete the tournament.

___

### Data storage

Data is stored in Google Datastore. There are three tables for three different types of objects: users, tournaments, and courses. User objects have the following attributes:

* Username
* List of tournament IDs the user is hosting
* List of tournament IDs the user is participating in

Tournament objects have the following attributes:

* Tournament name
* Tournament ID
* Hosting user
* Date
* Time
* Entry fee
* Course ID
* List of player names, each of which has an associated list of scores

Course objects have the following attributes:

* ID
* Name
* Location
* List of pars for each hole

The Android application communicates with the datastore via a stateless HTTP server set up with Google App Engine, which acts as an intermediary between the application and the datastore. The application will send HTTP messages to the server to either request data from the datastore or modify data within the datastore, and the server will retrieve or modify data in the datastore accordingly. Datastore does have an API that can be used to access the data directly, which can potentially be used as an alternative to the Google App Engine server. In a scenario with a large amount of traffic, App Engine and Datastore should be able to scale up/out automatically.

Retrieve tournaments:
* GET /tournaments
* Returns a list of all tournament objects stored in the datastore.

```
{
    tournaments:[
    {
        name: "tournament1",
        id: 154,
        host: "alex",
        date: "01/01/2020",
        time: "10:00 AM",
        fee: 12.54,
        courseid: 3686,
        scores:[
        {
            player: "bob",
            score: [-1, 2, 1, 0, 1, -1, 1, 0, 1, 0, 1, 2, -1, 0, 1, 0, 0, 1]
        },
        {
            player: "jacob",
            score: [-1, 3, 1, 2, 1, 0, 1, 0, -1, 0, 1, 2, 0, 0, 0, 0, 0, 1]
        }
        ]
    }
    ]
}
```

Retrieve single tournament:
* GET /tournaments/{tournament ID}
* Returns a tournament object corresponding to the requested ID

```
{
    name: "tournament1",
    id: 154,
    host: "alex",
    date: "01/01/2020",
    time: "10:00 AM",
    fee: 12.54,
    courseid: 3686,
    scores:[
    {
        player: "bob",
        score: [-1, 2, 1, 0, 1, -1, 1, 0, 1, 0, 1, 2, -1, 0, 1, 0, 0, 1]
    },
    {
        player: "jacob",
        score: [-1, 3, 1, 2, 1, 0, 1, 0, -1, 0, 1, 2, 0, 0, 0, 0, 0, 1]
    }
    ]
}
```


Create tournament:
* POST /tournaments
* Attributes of newly-created tournament are attached in request body except tournament ID
* Creates tournament with unique ID and returns the created tournament object


Modify tournament:
* PUT /tournaments/{tournament ID}
* Modified attributes are attached in the request body
* Modifies and returns the corresponding tournament object
* Many users could be modifying the same tournament at the same time, may be an issue

Delete tournament:
* DELETE /tournaments/{tournament ID}
* Returns “200 OK” if delete successful or “404 not found” if no tournament found

Retrieve user:
* GET /users
* Returns a list of users stored in the datastore.

```
{
    users:[
    {
        username: "alex",
        hosting: [154],
        playing: []
    },
    {
        username: "bob",
        hosting: [],
        playing: [154]
    }
    ]
}
```

Retrieve single user:
* GET /users/{username}
* Returns the corresponding user

```
{
    username: "alex",
    hosting: [154],
    playing: []
}
```

Create user:
* POST /users
* Attributes of newly-created user are attached in request body
* Creates and returns new user

Modify user:
* PUT /users/{username}
* Attributes of modified user are attached in request body
* Modifies and returns user

Delete user:
* DELETE /users/{username}
* Returns “200 OK” if delete successful or “404 not found” if no user found

Retrieve courses:
* GET /courses
* Returns a list of courses

```
{
    courses:[
    {
        name: "course1",
        id: 154,
        location: "1234 example way",
        par: [3,4,3,5,4,5,4,3,4,5,4,3,4,3,3,4,5,5]
    },
    {
        name: "course2",
        id: 157,
        location: "4321 example drive",
        par: [5,4,5,4,3,4,5,4,3,3,4,4,4,4,5,3,4,3]
    }
    ]
}
```

Retrieve single course:
* GET /courses/{course ID}
* Returns the corresponding course

```
courses:[
{
    name: "course1",
    id: 154,
    location: "1234 example way",
    par: [3,4,3,5,4,5,4,3,4,5,4,3,4,3,3,4,5,5]
}
```

Create course:
* POST /courses
* Attributes of newly-created course are attached in request body
* Creates and returns new course

Modify course:
* PUT /courses/{course ID}
* Attributes of modified course are attached in request body
* Modifies and returns course

Delete course:
* DELETE /courses/{course ID}
* Returns “200 OK” if delete successful or “404 not found” if no user found

User and tournament data will be made and modified at the application's request via various commands. Course data, while accessed by the application during regular use, should not be modified by the application. One possible method for populating the course information would be through the [golfbert API](https://golfbert.com/api), which holds a large golf course database.