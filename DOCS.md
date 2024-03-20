# Documentation

## What is this?
Simple movie rating application.

### What kind of features does it support?
- User login, user profiles
- Movie info search, movie info creation
- Movie ratings created by users-- users create movie ratings, view ratings from themselves and others

## Service Design

<!-- TODO: Diagram -->

User actions and how they flow through the app
- User search for movie to review (simple text) -> Movie service -> TMDB (cache data) -> DB
- No movie match? User submits a new title (title, release year, description, TMDB ID) -> Movie service pulls data from, else creates the movie manually -> DB
- User submits review (user ID, movie ID, rating (out of 5), review) -> Ratings service -> DB
    - User can search for a movie without login but must be logged in to submit a rating
- User views profile (with movie ratings) -> User service -> DB : Users model has a one-to-many relationship with Ratings


### Core data entities
- Users (authentication), see [src/users/models.py](src/users/models.py)
- Movies (UUID, title, release date, overview, tmdb_id, etc.), see [src/movies/models.py](src/movies/models.py)
- Ratings (users x movies), see [src/ratings/models.py](src/ratings/models.py)

<!-- Diagram here -->


## External Integrations
- External movie database API: TMDB

Choosing an external movie database API (EMD API): thoughts, requirements
- EMD API needs to be free or mostly free
    * I will cache these requests, so it's not like I need an expansive rate limit, but I don't want to get suddenly billed after this coding challenge is submitted.
- EMD API needs to be be pretty complete, updated regularly, reliable
- EMD API should have good documentation
- _Ideally_ EMD API has a community, other develop users, so that I can Google any issues that might arise

*My choice: https://www.themoviedb.org/*
Why?
- This choice meets all the requirements-- it's free, it has a large inventory of movies and ratings, the documentation is great, and there is an existing community of developers who use this. It's an established technology, and I feel lucky that it's free for personal use.

What else did I consider?
- IMDB via AWS: Only free for a month https://aws.amazon.com/marketplace/pp/prodview-3n67c76ppu2yy?sr=0-3&ref_=beagle&applicationId=AWSMPContessa#offers
- IMDB via Rapid API: API wasn't as full-featured as other offerings (only had generic keyword search, and then one details API endpoint per title / name / video / news), which might limit the features that we could build in the future. https://rapidapi.com/Glavier/api/imdb146
- MoviesDatabase via Rapid API: Sufficiently full-featured, but the documentation was just a schema https://rapidapi.com/SAdrian/api/moviesdatabase/tutorials/moviesdatabase-documentation
- Rotten Tomatoes: You have to apply for API access, too much effort https://developer.fandango.com/rotten_tomatoes

Note: I liked the idea of Rapid API-- they host a collection of APIs that devs can access, and they give devs a dashboard to manage their API subscriptions and usage. I would love to use this service for future projects!

### File structure

Having seen multiple monolith-to-microservice migrations in my tech career, I'm going to set up my baby service with separation of concerns already built in.

I'm going to use Flask Blueprint to do this.

So my file structure will (hopefully, if I have time) end up looking something like this.

TODO Note: I ran out of time to really clean up the file structure, but this was my aspiration:

```
/thermondo-backend-coding-challenge
├── /services
│   ├── __init__.py
│   ├── /users
│   │   ├── /templates
│   │   ├── /static
│   │   └── routes.py
│   ├── /user_profiles
│   │   ├── /templates
│   │   ├── /static
│   │   └── routes.py
│   ├── /movies
│   │   ├── /templates
│   │   ├── /static
│   │   └── routes.py
│   └── /movie_reviews
│       ├── /templates
│       ├── /static
│       └── routes.py
├── app.py
├── /static
├── /templates
└── /migrations
```

## Setup and Utilities

_This is also documented in the README_

This project has a `make` file that contains all the commands you should need.

Run the server
```
$ make run-app
```

Run the tests
```
$ make run-tests
```

Run and apply migrations
```
$ make migrate-db
```

Run the python linter
```
$ make lint-py
```


