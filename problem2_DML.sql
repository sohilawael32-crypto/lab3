USE library;

-- Authors first (books reference them)
INSERT INTO AUTHOR (author_id, name, country) VALUES
(1, 'Naguib Mahfouz',  'Egypt'),
(2, 'Agatha Christie', 'United Kingdom'),
(3, 'Paulo Coelho',    'Brazil'),
(4, 'Taha Hussein',    'Egypt');

-- Books (author_id must exist in AUTHOR)
INSERT INTO BOOK (book_id, title, price, author_id) VALUES
(1, 'Palace Walk',                  150.00, 1),
(2, 'Midaq Alley',                  120.50, 1),
(3, 'Murder on the Orient Express', 180.00, 2),
(4, 'And Then There Were None',     165.75, 2),
(5, 'The Alchemist',                140.00, 3),
(6, 'Eleven Minutes',               130.00, 3),
(7, 'The Days',                     110.00, 4);
