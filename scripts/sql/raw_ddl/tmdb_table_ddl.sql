-- Table for movies
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    movie_id INT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    origin_country TEXT,
    tagline TEXT,
    overview TEXT,
    release_date DATE,
    vote_average DECIMAL,
    budget INTEGER,
    revenue INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for genres
CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    genre_id INT UNIQUE NOT NULL,
    name TEXT NOT NULL
);

-- Junction table for movie-genre relationships
CREATE TABLE movie_genres (
    id SERIAL PRIMARY KEY,
    movie_id INT REFERENCES movies(movie_id),
    genre_id INT REFERENCES genres(genre_id)
);

-- Table for cast
CREATE TABLE cast (
    id SERIAL PRIMARY KEY,
    movie_id INT REFERENCES movies(movie_id),
    actor_name TEXT NOT NULL,
    character_name TEXT
);

-- Table for similar movies
CREATE TABLE similar (
    id SERIAL PRIMARY KEY,
    similar_movie_id INT UNIQUE NOT NULL,
    similar_name TEXT NOT NULL
);

-- Junction table for movie-similar relationships
CREATE TABLE movies_similar (
    id SERIAL PRIMARY KEY,
    movie_id INT REFERENCES movies(movie_id),
    similar_movie_id INT REFERENCES similar_movies(similar_movie_id)
);
