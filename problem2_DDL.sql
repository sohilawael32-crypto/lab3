DROP DATABASE IF EXISTS library;
CREATE DATABASE library;
USE library;

-- AUTHOR must be created first because BOOK references it
CREATE TABLE AUTHOR (
  author_id INT          NOT NULL AUTO_INCREMENT,
  name      VARCHAR(100) NOT NULL,
  country   VARCHAR(50),
  PRIMARY KEY (author_id)
);

CREATE TABLE BOOK (
  book_id   INT           NOT NULL AUTO_INCREMENT,
  title     VARCHAR(150)  NOT NULL,
  price     DECIMAL(10,2),
  author_id INT           NOT NULL,
  PRIMARY KEY (book_id),
  FOREIGN KEY (author_id) REFERENCES AUTHOR(author_id)
    ON DELETE CASCADE   -- deleting an author deletes all of his/her books
);