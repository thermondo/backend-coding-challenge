# Documentation

<!-- Temporary home for system design and API documentation -->

## What is this?
Backend for a movie rating application.

### What kind of features does it support?
- User login, user profiles
- Movie info search, movie info creation
- Movie ratings created by users-- users create movie ratings, view ratings from themselves and others

## Service Design

<!-- TODO: Diagram -->

User actions and how they flow through the app
- User search for movie to review (simple text) -> Movie service -> TMDB (cache data) -> DB
- No movie match? User submits a new title (title, release year, description) -> Movie service (flag as user-created) -> DB
- User submits review (user ID, movie ID, rating, details) -> Movie ratings service -> DB
    - User can search for a movie without login but must be logged in to review
- User views profile (with movie ratings) -> User service -> Movie ratings service -> DB


### Core data entities
- Users (authentication)
- Movies (UUID, title, release date, description, maybe )
- Movie ratings (users x movies)

Other data entities
- User Profiles (maybe real name, bio, photo, etc.)

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

So my file structure will end up looking something like this.
Source: https://blog.ashutoshkrris.in/how-to-use-blueprints-to-organize-your-flask-apps

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
|       ├── /templates
|       ├── /static
|       └── routes.py
├── app.py
├── /static
└── /templates
```

## App Setup

<!-- These are just random notes right now -->

I used pyenv to create a virtual env, it is called "tbcc-app".




