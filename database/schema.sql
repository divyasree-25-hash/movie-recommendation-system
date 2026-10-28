CREATE DATABASE IF NOT EXISTS movie_recommendation
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE movie_recommendation;

CREATE TABLE IF NOT EXISTS movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    release_year SMALLINT,
    genre VARCHAR(80) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_movie_title_year (title, release_year)
);

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    rating TINYINT NOT NULL,
    rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_rating_range CHECK (rating BETWEEN 1 AND 5),
    CONSTRAINT fk_rating_user FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_rating_movie FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        ON DELETE CASCADE,
    UNIQUE KEY unique_user_movie_rating (user_id, movie_id)
);
