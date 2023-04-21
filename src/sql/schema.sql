CREATE TABLE Rating (
  user_id INT,
  isbn VARCHAR(255),
  rating INT
);

LOAD DATA INFILE '/data/ratings.csv'
INTO TABLE Rating
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

ALTER TABLE Rating ADD column `id` INT unsigned primary KEY AUTO_INCREMENT FIRST;
