import os
import json

from flask import request, abort
from dotenv import load_dotenv

from app import app, models, redis_db, db


load_dotenv()


@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    if request.method == 'GET':
        product = redis_db.get(product_id)

        PAGE_ELEMENTS_NUMBER = 2
        pages_number = int(request.args.get('page', 1))
        start_page_elements = (pages_number - 1) * PAGE_ELEMENTS_NUMBER
        finish_page_elements = pages_number * PAGE_ELEMENTS_NUMBER

        if not product:
            product = models.Product.query.filter_by(id=product_id).first()
            if not product:
                abort(404, 'Product not found')
            product = product.to_dict()

            product_reviews = models.Review.query.filter_by(asin=product['Asin'])
            product['Reviews'] = [product_review.to_dict() for product_review in product_reviews]

            redis_db.set(product['id'], json.dumps(product).encode('utf-8'), ex=int(os.getenv("REDIS_TTL")))
        else:
            product = json.loads(product)

        product['Reviews'] = product['Reviews'][start_page_elements: finish_page_elements]

        return product


@app.route('/add_review', methods=['PUT'])
def add_review():
    if request.method == 'PUT':
        request_data = request.get_json()

        product_id = request_data['Product ID']

        title = request_data['Title']
        review = request_data['Review']

        product = models.Product.query.filter_by(id=product_id).first()

        if not product:
            abort(404, f'Product {product_id} not found')

        product = product.to_dict()

        new_review = models.Review(asin=product['Asin'], title=title, review=review)
        db.session.add(new_review)
        db.session.commit()

        abort(200)


def start_api():
    app.run()
