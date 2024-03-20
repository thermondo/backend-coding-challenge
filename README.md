# Welcome to my Movie Rating System!


![App Demo](app_demo.gif)


## Setup
This is a Flask app written in Python-- please enseure you have Python 3.12 installed!
```
$ python --version
# Python 3.12.1
$ pip --version
# pip 24.0 from /Users/margaretmoreno/.pyenv/versions/tbcc-app/lib/python3.12/site-packages/pip (python 3.12)
```

To install the dependencies
```
$ pip install -r requirements.txt
```

To run the server-- the server will automatically spin up on port 5001, see http://127.0.0.1:5001/search
```
$ make migrate-db
$ make run-app
```

To run the unit tests
```
$ make run-tests
```

## How to use

1. Search for movies at `/search`
2. Click on a movie profile to see movie details, url `movies/<movie_id>`
3. Click on "Create a new rating" to add a rating for that movie, url `/ratings/new?movie_id=<movie_id>`
    - **You'll have to log in before you create a review!** Create a new user by clicking "Sign up" or navigate to `/register`
4. Once you're logged in, you can create a new rating.
5. View your ratings by clicking "View my profile", navigating to `/current_user`, or `/users/<your_username>`.
6. Didn't find the movie you want to review? Add it to the DB at `/movies/new`. There was also a button in the top right corner of the search results page.

## Documentation

See [DOCS.md](DOCS.md) for detailed architecture documentation.


## Things I meant to get to but didn't have time

- [ ] More thorough unit testing-- for a lot of stuff, I wrote pretty basic tests and called it Good Enough for this challenge
- [ ] Add an actual Python logger-- I just used a print statement for things I wanted to debug
- [ ] Better code organization and style. For example:
  - [ ] Replace "query" and "filter_by" with session and select
  - [ ] Reorganize original user tests so that login tests are in route
  - [ ] Reorganize original user tests so that login tests are in route
  - [ ] Add system diagrams to DOCS.md
- [ ] Better UI-- not just a better frontend but API UI improvements. For example:
  - [ ] Users can create ratings for _anyone_, not just themselves-- I'd rather they were only able to create ratings for themselves
- [ ] Add swagger-- I haven't used it before, but it looks really neat, and I wanted to try it out.
- [ ] Clean up file structure to better match my intentions written in DOCS.md
- [ ] Deploy the app with a simple service-- If I had more time, I thought it would be cool

---

# Backend Senior Coding Challenge 🍿

Welcome to our Movie Rating System Coding Challenge! We appreciate you taking
the time to participate and submit a coding challenge! 🥳

In this challenge, you'll be tasked with designing and implementing a robust
backend system that handles user interactions and provides movie ratings. We
don't want to check coding conventions only; **we want to see your approach
to systems design!**

**⚠️ As a tech-agnostic engineering team, we ask you to pick the technologies
you are most comfortable with and those that will showcase your strongest
performance. 💪**

## ✅ Requirements

- [X] The backend should expose RESTful endpoints to handle user input and
  return movie ratings.
- [X] The system should store data in a database. You can use any existing
  dataset or API to populate the initial database.
- [X] Implement user endpoints to create and view user information.
- [X] Implement movie endpoints to create and view movie information.
- [X] Implement a rating system to rate the entertainment value of a movie.
- [X] Implement a basic profile where users can view their rated movies.
- [X] Include unit tests to ensure the reliability of your code.
- [X] Ensure proper error handling and validation of user inputs.

## ✨ Bonus Points

- [X] Implement authentication and authorization mechanisms for users.
- [ ] Provide documentation for your API endpoints using tools like Swagger.
- [ ] Implement logging to record errors and debug information.
- [ ] Implement caching mechanisms to improve the rating system's performance.
- [X] Implement CI/CD quality gates. -- I added a linter, but normally I would set up GH actions (or something equivalent) to also run the tests before any PRs are merged.

## 📋 Evaluation Criteria

- **Systems Design:** We want to see your ability to design a flexible and
  extendable system. Apply design patterns and software engineering concepts.
- **Code quality:** Readability, maintainability, and adherence to best
  practices.
- **Functionality:** Does the system meet the requirements? Does it provide
  movie
  ratings?
- **Testing:** Adequate test coverage and thoroughness of testing.
- **Documentation:** Clear documentation for setup, usage, and API endpoints.

## 📐 Submission Guidelines

- Fork this GitHub repository.
- Commit your code regularly with meaningful commit messages.
- Include/Update the README.md file explaining how to set up and run your
  backend, including any dependencies.
- Submit the link to your repository.

## 🗒️ Notes

- You are encouraged to use third-party libraries or frameworks to expedite
  development but be prepared to justify your choices.
- Feel free to reach out if you have any questions or need clarification on the
  requirements.
- Remember to approach the challenge as you would a real-world project, focusing
  on scalability, performance, and reliability.

## 🤔 What if I don't finish?

Part of the exercise is to see what you prioritize first when you have a limited
amount of time. For any unfinished tasks, please do add `TODO` comments to
your code with a short explanation. You will be given an opportunity later to go
into more detail and explain how you would go about finishing those tasks.
