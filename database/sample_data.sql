USE movie_recommendation;

INSERT IGNORE INTO movies (title, release_year, genre) VALUES
('Inception', 2010, 'Sci-Fi'),
('Interstellar', 2014, 'Sci-Fi'),
('The Dark Knight', 2008, 'Action'),
('Toy Story', 1995, 'Animation'),
('Finding Nemo', 2003, 'Animation'),
('The Grand Budapest Hotel', 2014, 'Comedy'),
('The Shawshank Redemption', 1994, 'Drama'),
('Get Out', 2017, 'Horror'),
('The Notebook', 2004, 'Romance'),
('Knives Out', 2019, 'Crime');

INSERT INTO users (display_name) VALUES
('Demo User 1'), ('Demo User 2'), ('Demo User 3')
ON DUPLICATE KEY UPDATE display_name = VALUES(display_name);

INSERT INTO ratings (user_id, movie_id, rating)
SELECT u.user_id, m.movie_id, x.rating
FROM (
    SELECT 'Demo User 1' AS username, 'Inception' AS title, 5 AS rating UNION ALL
    SELECT 'Demo User 2', 'Inception', 4 UNION ALL
    SELECT 'Demo User 3', 'Inception', 5 UNION ALL
    SELECT 'Demo User 1', 'Interstellar', 5 UNION ALL
    SELECT 'Demo User 2', 'Interstellar', 5 UNION ALL
    SELECT 'Demo User 3', 'Interstellar', 4 UNION ALL
    SELECT 'Demo User 1', 'The Dark Knight', 5 UNION ALL
    SELECT 'Demo User 2', 'The Dark Knight', 4 UNION ALL
    SELECT 'Demo User 3', 'The Dark Knight', 5 UNION ALL
    SELECT 'Demo User 1', 'Toy Story', 4 UNION ALL
    SELECT 'Demo User 2', 'Toy Story', 5 UNION ALL
    SELECT 'Demo User 3', 'Toy Story', 4 UNION ALL
    SELECT 'Demo User 1', 'Finding Nemo', 4 UNION ALL
    SELECT 'Demo User 2', 'Finding Nemo', 4 UNION ALL
    SELECT 'Demo User 3', 'Finding Nemo', 5 UNION ALL
    SELECT 'Demo User 1', 'The Grand Budapest Hotel', 4 UNION ALL
    SELECT 'Demo User 2', 'The Grand Budapest Hotel', 3 UNION ALL
    SELECT 'Demo User 3', 'The Grand Budapest Hotel', 4 UNION ALL
    SELECT 'Demo User 1', 'The Shawshank Redemption', 5 UNION ALL
    SELECT 'Demo User 2', 'The Shawshank Redemption', 5 UNION ALL
    SELECT 'Demo User 3', 'The Shawshank Redemption', 5 UNION ALL
    SELECT 'Demo User 1', 'Get Out', 4 UNION ALL
    SELECT 'Demo User 2', 'Get Out', 4 UNION ALL
    SELECT 'Demo User 3', 'Get Out', 3 UNION ALL
    SELECT 'Demo User 1', 'The Notebook', 3 UNION ALL
    SELECT 'Demo User 2', 'The Notebook', 4 UNION ALL
    SELECT 'Demo User 3', 'The Notebook', 4 UNION ALL
    SELECT 'Demo User 1', 'Knives Out', 4 UNION ALL
    SELECT 'Demo User 2', 'Knives Out', 5 UNION ALL
    SELECT 'Demo User 3', 'Knives Out', 4
) AS x
JOIN users u ON u.display_name = x.username
JOIN movies m ON m.title = x.title
ON DUPLICATE KEY UPDATE rating = VALUES(rating);
