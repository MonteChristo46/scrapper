CREATE TABLE IF NOT EXISTS listings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  price FLOAT NOT NULL,
  subtitle VARCHAR(255),
  rating FLOAT,
  num_ratings INT,
  url VARCHAR(255),
  review VARCHAR(255),
  owner VARCHAR(255)
);