App Engine application for the Udacity training course.

## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [Google Cloud Endpoints][3]

## Setup Instructions
1. Update the value of `application` in `app.yaml` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
1. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console][4].
1. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
1. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
1. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting
   your local server's address (by default [localhost:8080][5].)
1. Generate your client library(ies) with [the endpoints tool][6].
1. Deploy your application.

## Endpoint Additional Queries
   The following additional queries could be used to determine the sessions within a conference in a given day, along with finding sessions of a particular type:
1. getConferenceSessionsByDate --Get all the session for a Conference in a given date, order by startTime
2. getConferenceSessionsByType --Given a ConferenceKey and a sessionType, returns all the sessions of that type


## Task 1: Design Choices (Response)
I did not use inheritance for Session. I prefer to explicitly define a property ('conference') to define the relation. Iy seems more logical and the code is more readable.
I used Memcache for featured speakers as a Task inside _createSessionObject(). When a session is put in the datastore the task checks if the speaker has more than one session in that conference. mem_key is the key for Memcache I used string {websafeConferenceKey}:featured, to specify that is referred to featured speakers of a given Conference.
## Session Endpoints
sessions/create/{ConferenceKey} -> conference.createSession
sessions/{ConferenceKey} -> conference.getConferenceSessions
sessions/by/speaker/{speakerName} -> conference.getSessionsBySpeaker
sessions/{ConferenceKey}/type/{sessionType} -> conference.getConferenceSessionsByType
## featuredSpeaker Endpoint
conference/{websafeConferenceKey}/featuredSpeaker -> conference.getFeaturedSpeaker

## Task 2: Add Sessions to User Wishlist
I added the wishlist as a property ('sessionKeysWishlist') in the Profile model. This is the most efficient way to do it.
The SessionKey can be retrieved via conference.getConferenceSessions.
## wishlist Endpoints
wishlist/add/{websafeSessionKey} -> conference.addSessionToWishlist
wishlist/get -> conference.getSessionsInWishlist

## Task 3 and Query Problem
I added the index needed by the queries for Session objects in the index.yaml.
The problem with the query is that datastore will reject queries using inequality filtering on more than one property. To solve the issue, instead of specifying an entire query filter in a single expression, build it up in steps, by iterating the results of the 1st filter until objects of the 2nd filter are found. See SpecialQuery implementation.
## SpecialQuery Endpoint
SpecialQuery/{websafeConferenceKey}


