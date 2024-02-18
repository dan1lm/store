from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)

url = "postgresql://lezxadrs:GF_zYsaHAhSJO9V8d_oQcUuYF3NNF_pG@drona.db.elephantsql.com/lezxadrs"
app.config['SQLALCHEMY_DATABASE_URI'] = url
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    category = db.Column(db.String(255))
    image = db.Column(db.String(255))
    rating_rate = db.Column(db.Float)
    rating_count = db.Column(db.Integer)

@app.route('/products')
def get_products():
    url_params = request.args
    sort = url_params.get('sort', 'desc')  # Default to 'desc' if not provided
    limit = url_params.get('limit', 12)  # Default to 12 if not provided
    query = Product.query.order_by(Product.price.desc() if sort == 'desc' else Product.price.asc()).limit(limit)
    products = query.all()
    
    return jsonify([{
        'id': product.id,
        'title': product.title,
        'price': product.price,
        'description': product.description,
        'category': product.category,
        'image': product.image,
        'rating': {
            'rate': product.rating_rate,
            'count': product.rating_count
        }
    } for product in products])


@app.route('/products/category/<categoryName>', methods=['GET'])
def get_filtered_products_by_category(categoryName):
    url_params = request.args
    #category = url_params.get('category', 'jewelery')
    sort = url_params.get('sort', 'desc')  # Default to 'desc' if not provided
    limit = url_params.get('limit', 12)  # Default to 12 if not provided

    # Retrieve from database
    query = Product.query.filter_by(category=categoryName)
    query = query.order_by(Product.price.desc() if sort == 'desc' else Product.price.asc())
    query = query.limit(limit)
    products = query.all()

    # Return the products as JSON
    return jsonify([{
        'id': product.id,
        'title': product.title,
        'price': product.price,
        'description': product.description,
        'category': product.category,
        'image': product.image,
        'rating': {
            'rate': product.rating_rate,
            'count': product.rating_count
        }
    } for product in products])

    
@app.route('/products/categories')
def get_categories():
    return jsonify([
        "electronics",
        "jewelry",
        "men's clothing",
        "women's clothing"
    ])

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(
        title=data['title'],
        price=data['price'],
        description=data['description'],
        category=data['category'],
        image=data['image'],
        rating_rate=data['rating']['rate'],
        rating_count=data['rating']['count']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully'})


        
if __name__ == '__main__':
    app.run(debug=True, port=8000)
