from flask import Flask, redirect, url_for, jsonify, request 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)   # Flask constructor 
  
# Sample data
books = [
    {"id": 1, "title": "Concept of Physics", "author": "H.C Verma"},
    {"id": 2, "title": "Gunahon ka Devta", "author": "Dharamvir Bharti"},
    {"id": 3, "title": "Problems in General Physics", "author": "I.E Irodov"}
]

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/my_books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning

# Create SQLAlchemy instance
db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=False, nullable=False)
    author = db.Column(db.String(20), unique=False, nullable=False)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Name : {self.title}, Author: {self.author}"

# A decorator used to tell the application 
# which URL is associated function 
@app.route('/')       
def hello(): 
    return 'HELLO'

# A decorator used to tell the application
# which URL is associated with the function
@app.route('/hello/<name>')
def hello_name(name):
    return f'Hello {name} !'  

@app.route('/blog/<int:postID>')
def show_blog(postID): 
    return 'Blog Number %d' % postID

@app.route('/admin')  # decorator for route(argument) function
def hello_admin():  # binding to hello_admin call
    return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):  # binding to hello_guest call
    return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':  # dynamic binding of URL to function
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest=name))


# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# Get a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    return jsonify(book) if book else (jsonify({"error": "Book not found"}), 404)

# Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    '''
    curl http://192.168.1.190:5000/books -H "Content-Type: application/json" -d '{"id": 4, "title": "Mythology", "author": "Edith Hamilton"}'
    '''
    new_book = request.json
    books.append(new_book)
    return jsonify(new_book), 201

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    '''
    curl http://192.168.1.190:5000/books/1 -H "Content-Type: application/json" -X "DELETE" 
    '''
    global books
    books = [book for book in books if book["id"] != book_id]
    return jsonify({"message": "Book deleted"})

if __name__=='__main__': 
   with app.app_context():  # Needed for DB operations
        db.create_all()      # Creates the database and tables
   app.run(debug=True, host="0.0.0.0")