CREATE TABLE movie (
    id uuid PRIMARY KEY,
    title text NOT NULL,
    description text,
    genre text NOT NULL,
    release_year integer NOT NULL,
    director text,
    duration_minutes integer,
    poster_url text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);

CREATE TABLE rating (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    movie_id uuid NOT NULL REFERENCES movie(id) ON DELETE CASCADE,
    rating_value decimal(3,2) NOT NULL CHECK (rating_value >= 1.0 AND rating_value <= 10.0),
    review text,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    UNIQUE(user_id, movie_id)
);

CREATE INDEX idx_movie_genre ON movie(genre);
CREATE INDEX idx_movie_release_year ON movie(release_year);
CREATE INDEX idx_rating_user_id ON rating(user_id);
CREATE INDEX idx_rating_movie_id ON rating(movie_id);
CREATE INDEX idx_rating_value ON rating(rating_value);

INSERT INTO movie (id, title, description, genre, release_year, director, duration_minutes, poster_url, created_at, updated_at) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', 'Drama', 1994, 'Frank Darabont', 142, 'https://some.domain/shawshank.jpg', NOW(), NOW()),
('550e8400-e29b-41d4-a716-446655440002', 'The Godfather', 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.', 'Crime', 1972, 'Francis Ford Coppola', 175, 'https://some.domain/godfather.jpg', NOW(), NOW()),
('550e8400-e29b-41d4-a716-446655440003', 'The Dark Knight', 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.', 'Action', 2008, 'Christopher Nolan', 152, 'https://some.domain/darkknight.jpg', NOW(), NOW()),
('550e8400-e29b-41d4-a716-446655440004', 'Pulp Fiction', 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.', 'Crime', 1994, 'Quentin Tarantino', 154, 'https://some.domain/pulpfiction.jpg', NOW(), NOW()),
('550e8400-e29b-41d4-a716-446655440005', 'Inception', 'A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', 'Sci-Fi', 2010, 'Christopher Nolan', 148, 'https://some.domain/inception.jpg', NOW(), NOW());
