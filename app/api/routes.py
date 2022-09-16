from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/books', methods= ['POST'])
@token_required
def create_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    publisher = request.json['publisher']
    year = request.json['year']
    hardcover = request.json['hardcover']
    isbn = request.json['isbn']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(title, author, publisher, year, hardcover, isbn, user_token=user_token)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    single_book = Book.query.get(id)
    response = book_schema.dump(single_book)
    return jsonify(response)

@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_car(current_user_token,id):
    book = Book.query.get(id) 
    book.title = request.json['title']
    book.author = request.json['author']
    book.publisher = request.json['publisher']
    book.year = request.json['year']
    book.hardcover = request.json['hardcover']
    book.isbn = request.json['isbn']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)