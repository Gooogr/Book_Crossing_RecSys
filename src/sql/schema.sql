CREATE TABLE ratings (
  user_id INT,
  isbn VARCHAR(255),
  rating INT
);

LOAD DATA INFILE '/data/ratings.csv'
INTO TABLE ratings
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

ALTER TABLE ratings ADD column `id` INT unsigned primary KEY AUTO_INCREMENT FIRST;
