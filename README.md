# Lab 3: Foreign Keys and Simple SQL
**Students (Lab 3 team):**
- Sohila Wael, ID 2304073
- Omar Mohamed, ID 2304093

This repository contains two problems:

- **Problem 1:** the COMPANY database (SQL scripts + answers to Q1.1 to Q1.3).
- **Problem 2:** the Library database (AUTHOR and BOOK) + a website to show, add, edit and delete books and authors. The website continues the Lab 2 website (Flask + MySQL). The Lab 2 README is kept at the end of this file.

## Folder structure

```
ass3/
  problem1_DDL.sql        # COMPANY database: tables, primary keys, foreign keys
  problem1_DML.sql        # COMPANY database: INSERT data (3+ rows per table)
  problem1_Answers.txt    # SQL + output/error for Q1.1 to Q1.3
  problem2_DDL.sql        # library database: AUTHOR and BOOK
  problem2_DML.sql        # seed data: 4 authors and 7 books
  website/                # Lab 2 website + the new library pages
    app.py
    requirements.txt
    .env.example
    templates/            # login, register, todos (Lab 2) + library, edit_book, edit_author (Lab 3)
    static/               # style.css and static/uploads (book covers and author photos)
    database/schema.sql   # Lab 2 database (`registration`), needed for the login / to-do pages
  README.md
```

## Requirements

- MySQL Server 8 (and the `mysql` command-line client)
- Python 3.10 or newer

## Step 1: Problem 1 (COMPANY database)

Open the **MySQL Command Line Client** (or run `mysql -u root -p` in a terminal), then run the scripts in this order. Use the full path of the folder, with `/` slashes:

```
source C:/path/to/lab3-2304073/problem1_DDL.sql
source C:/path/to/lab3-2304073/problem1_DML.sql
```

`problem1_DDL.sql` starts with `DROP DATABASE IF EXISTS company; CREATE DATABASE company; USE company;`, so it can be re-run at any time. Run the DDL before the DML.

The answers to Q1.1, Q1.2 and Q1.3 (the SQL and the output/error message) are in `problem1_Answers.txt`.

> On Linux/macOS or Windows CMD you can also run `mysql -u root -p < problem1_DDL.sql`.
> This does not work in PowerShell, use `source` as above.

## Step 2: Problem 2 (library database)

In the same MySQL client:

```
source C:/path/to/lab3-2304073/problem2_DDL.sql
source C:/path/to/lab3-2304073/problem2_DML.sql
```

This creates the database `library` with the tables `AUTHOR(author_id, name, country)` and `BOOK(book_id, title, price, author_id)`. `BOOK.author_id` is a foreign key to `AUTHOR.author_id` with `ON DELETE CASCADE`, so deleting an author also deletes all the books of that author. The DML inserts 4 authors and 7 books.

## Step 3: Lab 2 database (login and to-do pages)

The website still contains the Lab 2 pages (register, login, to-do list), which use the database `registration`. Run:

```
source C:/path/to/lab3-2304073/website/database/schema.sql
```

The library pages do not need a login, so this step is only needed for the Lab 2 pages.

## Step 4: Run the website

Open a terminal in the `website` folder and create the virtual environment:

```
cd website
python -m venv venv
venv\Scripts\activate          # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` (`copy .env.example .env` on Windows, `cp .env.example .env` on Linux/macOS) and fill in your values: your MySQL password and a long random `SECRET_KEY`. The file looks like this:

```
SECRET_KEY=any-long-random-text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=registration
```

`DB_NAME` is the Lab 2 database. The library pages connect to the database `library` automatically, with the same host, user and password.

Start the server:

```
python app.py
```

Open **http://127.0.0.1:5000/library** in the browser (the Lab 2 pages start at http://127.0.0.1:5000/register).

## Website pages (Problem 2)

| Requirement | Where |
|---|---|
| F2.1 Show a table of the books (with the `author_id` of each book) and a table of the authors | `/library` |
| F2.2 Add a book and add an author | forms "Add a book" and "Add an author" on `/library` |
| F2.3 Edit a book and edit an author | the **Edit** link next to each row (`/books/<id>/edit`, `/authors/<id>/edit`) |
| F2.4 Remove a book | the **Delete** button next to each book |
| F2.5 Remove an author | the **Delete** button next to each author (its books are deleted too) |

The pages validate the input (required fields, the price must be a number, the author must exist) and show a red error message when something is wrong.

**Bonus (images):** when adding or editing a book you can upload a cover, and for an author a photo (png, jpg, jpeg, gif or webp, 5 MB at most). The images are saved as files in `website/static/uploads/books/<book_id>.<ext>` and `website/static/uploads/authors/<author_id>.<ext>` and are shown as thumbnails in the tables. The database tables are not changed.

---

# Lab 2: Login & To-Do Application (previous assignment, kept in this README)

The Lab 2 pages are still part of the website (`/register`, `/login`, `/logout`, `/todos`). To run them, follow Steps 3 and 4 above and open `http://127.0.0.1:5000/register`.

## 1. Team Members

### Student 1
- Name: Sohila Wael
- ID: 2304073
- Wrote `database/schema.sql` (both tables and the foreign key).
- R1: Register with a duplicate e-mail check (`Email Already Exists`).
- R2: Login with the same message for a wrong e-mail or password, and logout.
- R3: Private list; redirect to the login page when not logged in.
- R9: bcrypt password hashing, parameterized queries, `user_id` from the session.
- R8 (part): validation of the register and login forms in the browser and on the server.
- Screenshots and README sections.

### Student 2
- Name: Omar Mohamed
- ID: 2304093
- R4 to R7: add, edit, mark done/not done, delete (with confirmation), using `AND user_id = ?`.
- R8 (part): validation of the to-do title in the browser and on the server.
- R10: consistent styling, 360 px responsive layout, empty-list message, done state.
- Bonus: counter of open to-dos.

## 2. Technology

- Back end: Python 3 with Flask. Passwords are hashed with `bcrypt`. MySQL is accessed with `PyMySQL` using plain SQL with parameters (no ORM).
- Front end: HTML, CSS and JavaScript, with Jinja templates.
- Database: MySQL 8.0, database `registration`.

## 3. Features

- R1 = Register with name, e-mail, password and confirm password. A duplicate e-mail shows `Email Already Exists`. After registering, the user is logged in and sees the list.
- R2 = Login with e-mail and password. A wrong e-mail or a wrong password shows the same message, `Invalid email or password`. Logout ends the session.
- R3 = The list is private. A visitor who is not logged in is redirected to the login page, and each user sees only their own to-dos, newest first.
- R4 = Add a to-do.
- R5 = Edit a to-do title.
- R6 = Mark a to-do as done or not done.
- R7 = Delete a to-do, with an "Are you sure?" confirmation.
- R8 = Validation in the browser (JavaScript) and again on the server, with the exact messages from the lab.
- R9 = Passwords are stored as bcrypt hashes. Only the given queries are used, always with parameters, and `user_id` always comes from the session.
- R10 = A consistent, responsive interface that works on a 360 px screen, with error messages, a visible state for done to-dos, an empty-list message, and the user's name with a logout button.
- Bonus: counter showing how many to-dos are still open.

## 4. Screenshots

The Lab 2 screenshots are in the `screenshots` folder of the Lab 2 repository:
https://github.com/sohilawael32-crypto/-Login-To-Do-Application-lab2

## 5. Answers

**(a) Why do UPDATE and DELETE contain `AND user_id = ?`, and what changes if you remove it?**
The id of a to-do comes from the browser, so anybody can send somebody else's number. Adding `AND user_id = ?` (the id of the logged-in user, taken from the session and never from a form) makes the statement change zero rows when the to-do is not yours. Without it, any logged-in user could edit or delete another user's to-dos just by changing the number in the request.

**(b) What happens if you insert a to-do for a `user_id` that does not exist, and which constraint of the lecture is that?**
MySQL rejects the INSERT with error 1452: "Cannot add or update a child row: a foreign key constraint fails". This is the foreign key constraint (referential integrity): every to-do must belong to exactly one existing user.

**(c) Why do you store a hash and not the password?**
If the database is leaked, anyone who reads it would see all the real passwords. A bcrypt hash cannot be reversed to get the original password. It is also salted, so two users with the same password get different hashes, and it is slow on purpose, which makes guessing attacks expensive. To log in, the library compares the typed password with the stored hash (`bcrypt.checkpw`).

**(d) The `name` column is NOT NULL: why did you still need your own check for an empty name?**
`NOT NULL` only means that the column must have a value. An empty text `''` is a value, not NULL, so MySQL accepts it. Only our own checks (in JavaScript in the browser and again on the server) can refuse an empty name.