import os
import bcrypt
import pymysql
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session
load_dotenv() 
from decimal import Decimal, InvalidOperation
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.route("/")
def home():
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS n FROM users")
        row = cur.fetchone()
    db.close()
    return f"Connected! Users in DB: {row['n']}"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    errors = []
    if not name:
        errors.append("Name is required")
    if not email:
        errors.append("Email is required")
    if not password:
        errors.append("Password is required")
    if not confirm:
        errors.append("Confirm password is required")
    if password and confirm and password != confirm:
        errors.append("Passwords do not match")

    if errors:
        return render_template("register.html", errors=errors, name=name, email=email)

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute(
                "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",
                (email, name, hashed),
            )
            user_id = cur.lastrowid
        db.commit()
    except pymysql.err.IntegrityError:
        return render_template("register.html", errors=["Email Already Exists"],
                               name=name, email=email)
    finally:
        db.close()

    session["user_id"] = user_id
    session["name"] = name
    return redirect("/todos")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    errors = []
    if not email:
        errors.append("Email is required")
    if not password:
        errors.append("Password is required")
    if errors:
        return render_template("login.html", errors=errors, email=email)

    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute(
                "SELECT user_id, name, password_hash FROM users WHERE email = %s",
                (email,),
            )
            user = cur.fetchone()
    finally:
        db.close()

    if user is None or not bcrypt.checkpw(
        password.encode("utf-8"), user["password_hash"].encode("utf-8")
    ):
        return render_template("login.html", errors=["Invalid email or password"],
                               email=email)

    session["user_id"] = user["user_id"]
    session["name"] = user["name"]
    return redirect("/todos")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


def validate_title(title):
    if not title.strip():
        return "Title is required"
    if len(title) > 200:
        return "Title is too long (200 characters at most)"
    return None


def show_list(errors=None, new_title=None):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute(
                "SELECT todo_id, title, is_done, created_at FROM todos "
                "WHERE user_id = %s ORDER BY todo_id DESC",
                (session["user_id"],),
            )
            items = cur.fetchall()
    finally:
        db.close()
    return render_template("todos.html", name=session["name"], todos=items,
                           errors=errors, new_title=new_title)


@app.route("/todos")
def todos():
    if "user_id" not in session:
        return redirect("/login")
    return show_list()


@app.route("/todos/add", methods=["POST"])
def add_todo():
    if "user_id" not in session:
        return redirect("/login")
    title = request.form.get("title", "").strip()
    error = validate_title(title)
    if error:
        return show_list(errors=[error], new_title=title)

    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("INSERT INTO todos (user_id, title) VALUES (%s, %s)",
                        (session["user_id"], title))
        db.commit()
    finally:
        db.close()
    return redirect("/todos")


@app.route("/todos/<int:todo_id>/edit", methods=["POST"])
def edit_todo(todo_id):
    if "user_id" not in session:
        return redirect("/login")
    title = request.form.get("title", "").strip()
    error = validate_title(title)
    if error:
        return show_list(errors=[error])

    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s",
                        (title, todo_id, session["user_id"]))
        db.commit()
    finally:
        db.close()
    return redirect("/todos")


@app.route("/todos/<int:todo_id>/toggle", methods=["POST"])
def toggle_todo(todo_id):
    if "user_id" not in session:
        return redirect("/login")
    is_done = 1 if request.form.get("is_done") == "1" else 0

    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s",
                        (is_done, todo_id, session["user_id"]))
        db.commit()
    finally:
        db.close()
    return redirect("/todos")


@app.route("/todos/<int:todo_id>/delete", methods=["POST"])
def delete_todo(todo_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM todos WHERE todo_id = %s AND user_id = %s",
                        (todo_id, session["user_id"]))
        db.commit()
    finally:
        db.close()
    return redirect("/todos")

# ====================== Lab 3: Library (Books and Authors) + image bonus ======================

# ---------- images (bonus) ----------
# Images are saved as files: static/uploads/books/<book_id>.<ext>
#                            static/uploads/authors/<author_id>.<ext>
# The database tables are not changed.
UPLOAD_ROOT = os.path.join(app.root_path, "static", "uploads")
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB at most per request

for _kind in ("books", "authors"):
    os.makedirs(os.path.join(UPLOAD_ROOT, _kind), exist_ok=True)


@app.errorhandler(413)
def too_large(e):
    return "The image is too large (5 MB at most). Go back and choose a smaller image.", 413


def image_url(kind, item_id):
    """Returns the url of the image of this book/author, or None if it has no image."""
    for ext in ALLOWED_EXT:
        path = os.path.join(UPLOAD_ROOT, kind, f"{item_id}.{ext}")
        if os.path.exists(path):
            return url_for("static", filename=f"uploads/{kind}/{item_id}.{ext}",
                           v=int(os.path.getmtime(path)))
    return None


app.jinja_env.globals["image_url"] = image_url


def image_error(file):
    """Checks the uploaded file (before touching the database). None = ok or no file chosen."""
    if file is None or file.filename == "":
        return None
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXT:
        return "Image must be png, jpg, jpeg, gif or webp"
    return None


def remove_image(kind, item_id):
    for ext in ALLOWED_EXT:
        path = os.path.join(UPLOAD_ROOT, kind, f"{item_id}.{ext}")
        if os.path.exists(path):
            os.remove(path)


def save_image(kind, item_id, file):
    """Saves the uploaded image (already checked by image_error). Replaces the old image."""
    if file is None or file.filename == "":
        return
    ext = file.filename.rsplit(".", 1)[-1].lower()
    remove_image(kind, item_id)
    file.save(os.path.join(UPLOAD_ROOT, kind, f"{item_id}.{ext}"))


# ---------- database ----------
def get_library_db():
    # same MySQL server and user as Lab 2, but a different database: `library`
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("LIBRARY_DB_NAME", "library"),
        cursorclass=pymysql.cursors.DictCursor,
    )


def validate_author(name, country):
    errors = []
    if not name:
        errors.append("Author name is required")
    elif len(name) > 100:
        errors.append("Author name is too long (100 characters at most)")
    if len(country) > 50:
        errors.append("Country is too long (50 characters at most)")
    return errors


def validate_book(title, price_text, author_id_text):
    """Returns (errors, price, author_id)."""
    errors = []
    price = None
    author_id = None

    if not title:
        errors.append("Book title is required")
    elif len(title) > 150:
        errors.append("Book title is too long (150 characters at most)")

    try:
        price = Decimal(price_text)
        if price < 0 or price > Decimal("99999999.99"):
            errors.append("Price must be between 0 and 99999999.99")
    except (InvalidOperation, ValueError):
        errors.append("Price must be a number")

    try:
        author_id = int(author_id_text)
    except ValueError:
        errors.append("Please choose an author")

    return errors, price, author_id


def get_all_authors():
    db = get_library_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT author_id, name, country FROM AUTHOR ORDER BY author_id")
            return cur.fetchall()
    finally:
        db.close()


def show_library(errors=None, form=None):
    db = get_library_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT book_id, title, price, author_id FROM BOOK ORDER BY book_id")
            books = cur.fetchall()
            cur.execute("SELECT author_id, name, country FROM AUTHOR ORDER BY author_id")
            authors = cur.fetchall()
    finally:
        db.close()
    return render_template("library.html", books=books, authors=authors,
                           errors=errors, form=form or {})


# ---------- F2.1  show both tables ----------
@app.route("/library")
def library():
    return show_library()


# ---------- F2.2  add an author / add a book ----------
@app.route("/authors/add", methods=["POST"])
def add_author():
    name = request.form.get("name", "").strip()
    country = request.form.get("country", "").strip()
    image = request.files.get("image")

    errors = validate_author(name, country)
    img_err = image_error(image)
    if img_err:
        errors.append(img_err)
    if errors:
        return show_library(errors=errors, form={"author_name": name, "author_country": country})

    db = get_library_db()
    try:
        with db.cursor() as cur:
            cur.execute("INSERT INTO AUTHOR (name, country) VALUES (%s, %s)", (name, country or None))
            new_id = cur.lastrowid
        db.commit()
    finally:
        db.close()

    save_image("authors", new_id, image)
    return redirect("/library")


@app.route("/books/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    price_text = request.form.get("price", "").strip()
    author_id_text = request.form.get("author_id", "").strip()
    image = request.files.get("image")

    errors, price, author_id = validate_book(title, price_text, author_id_text)
    img_err = image_error(image)
    if img_err:
        errors.append(img_err)
    form = {"book_title": title, "book_price": price_text, "book_author_id": author_id_text}
    if errors:
        return show_library(errors=errors, form=form)

    db = get_library_db()
    try:
        with db.cursor() as cur:
            cur.execute("INSERT INTO BOOK (title, price, author_id) VALUES (%s, %s, %s)",
                        (title, price, author_id))
            new_id = cur.lastrowid
        db.commit()
    except pymysql.err.IntegrityError:
        # foreign key failed: this author_id does not exist
        return show_library(errors=["This author does not exist"], form=form)
    finally:
        db.close()

    save_image("books", new_id, image)
    return redirect("/library")


# ---------- F2.3  edit an author / edit a book ----------
@app.route("/authors/<int:author_id>/edit", methods=["GET", "POST"])
def edit_author(author_id):
    db = get_library_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT author_id, name, country FROM AUTHOR WHERE author_id = %s",
                        (author_id,))
            author = cur.fetchone()
    finally:
        db.close()
    if author is None:
        return redirect("/library")

    if request.method == "GET":
        return render_template("edit_author.html", author=author)

    name = request.form.get("name", "").strip()
    country = request.form.get("country", "").strip()
    image = request.files.get("image")

    errors = validate_author(name, country)
    img_err = image_error(image)
    if img_err:
        errors.append(img_err)
    if errors:
        author["name"], author["country"] = name, country
        return render_template("edit_author.html", author=author, errors=errors)

    db = get_library_db()
    try:
        with db.cursor() as cur:
            cur.execute("UPDATE AUTHOR SET name = %s, country = %s WHERE author_id = %s",
                        (name, country or None, author_id))
        db.commit()
    finally:
        db.close()

    save_image("authors", author_id, image)
    return redirect("/library")


@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
    db = get_library_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT book_id, title, price, author_id FROM BOOK WHERE book_id = %s",
                        (book_id,))
            book = cur.fetchone()
    finally:
        db.close()
    if book is None:
        return redirect("/library")

    authors = get_all_authors()
    if request.method == "GET":
        return render_template("edit_book.html", book=book, authors=authors)

    title = request.form.get("title", "").strip()
    price_text = request.form.get("price", "").strip()
    author_id_text = request.form.get("author_id", "").strip()
    image = request.files.get("image")

    errors, price, author_id = validate_book(title, price_text, author_id_text)
    img_err = image_error(image)
    if img_err:
        errors.append(img_err)
    if errors:
        book["title"], book["price"] = title, price_text
        if author_id is not None:
            book["author_id"] = author_id
        return render_template("edit_book.html", book=book, authors=authors, errors=errors)

    db = get_library_db()
    try:
        with db.cursor() as cur:
            cur.execute("UPDATE BOOK SET title = %s, price = %s, author_id = %s WHERE book_id = %s",
                        (title, price, author_id, book_id))
        db.commit()
    except pymysql.err.IntegrityError:
        book["title"], book["price"] = title, price_text
        return render_template("edit_book.html", book=book, authors=authors,
                               errors=["This author does not exist"])
    finally:
        db.close()

    save_image("books", book_id, image)
    return redirect("/library")


# ---------- F2.4 remove a book / F2.5 remove an author ----------
@app.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    db = get_library_db()
    try:
        with db.cursor() as cur:
            cur.execute("DELETE FROM BOOK WHERE book_id = %s", (book_id,))
        db.commit()
    finally:
        db.close()

    remove_image("books", book_id)
    return redirect("/library")


@app.route("/authors/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id):
    # ON DELETE CASCADE in the database also deletes all the books of this author,
    # so we remember their ids to delete their cover images too
    db = get_library_db()
    try:
        with db.cursor() as cur:
            cur.execute("SELECT book_id FROM BOOK WHERE author_id = %s", (author_id,))
            book_ids = [row["book_id"] for row in cur.fetchall()]
            cur.execute("DELETE FROM AUTHOR WHERE author_id = %s", (author_id,))
        db.commit()
    finally:
        db.close()

    for bid in book_ids:
        remove_image("books", bid)
    remove_image("authors", author_id)
    return redirect("/library")

# ====================== end of Lab 3 block ======================

if __name__ == "__main__":
    app.run(debug=True)