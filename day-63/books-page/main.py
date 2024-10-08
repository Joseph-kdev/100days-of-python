from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

with app.app_context():
    # db.create_all()
    # all_books = Book.query.all()
    pass

@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        new_book = Book(title=request.form["title"], author=request.form["author"], rating= request.form["rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    
    return render_template("add.html")

@app.route("/edit/<id>", methods=["POST", "GET"])
def edit(id):
    book = Book.query.get(id)
    if request.method == "POST":
        book.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template("edit.html",book=book)

@app.route("/delete")
def delete():
    book_id = request.args.get("id")
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))
    

if __name__ == "__main__":
    app.run(debug=True)

