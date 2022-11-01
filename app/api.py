import os
import json

from flask import request, abort
from dotenv import load_dotenv

from app import app, models, redis_db, db


load_dotenv()


@app.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    if request.method == 'GET':
        try:
            product = redis_db.get(product_id)  # get redis cache ('None' if there is no cache)

            PAGE_ELEMENTS_NUMBER = 2  # the number of elements on the page
            pages_number = int(request.args.get('page', 1))  # get the page from the '?page=' attribute
            start_page_elements = (pages_number - 1) * PAGE_ELEMENTS_NUMBER  # the first element on the page
            finish_page_elements = pages_number * PAGE_ELEMENTS_NUMBER  # the last element on the page

            if not product:  # if there is no cache
                product = models.Product.query.filter_by(id=product_id).first()  # get the product from the db
                if not product:
                    abort(404, 'Product not found')  # if the product not found, then we return 404
                product = product.to_dict()

                product_reviews = models.Review.query.filter_by(asin=product['Asin'])  # get the reviews from the db
                # convert review from class elements to a dictionary
                product['Reviews'] = [product_review.to_dict() for product_review in product_reviews]

                # save cache
                redis_db.set(product['id'], json.dumps(product).encode('utf-8'), ex=int(os.getenv("REDIS_TTL")))
            else:
                product = json.loads(product)

            product['Reviews'] = product['Reviews'][start_page_elements: finish_page_elements]

            return product

        except Exception as e:
            print(e)
            abort(404)


@app.route('/add_review', methods=['PUT'])
def add_review():
    if request.method == 'PUT':
        try:
            # get data from put-request
            request_data = request.get_json()

            product_id = request_data['Product ID']

            title = request_data['Title']
            review = request_data['Review']

            # get product
            product = models.Product.query.filter_by(id=product_id).first()

            if not product:
                abort(404, f'Product {product_id} not found')  # if the product not found, then we return 404

            product = product.to_dict()

            # save review in db
            new_review = models.Review(asin=product['Asin'], title=title, review=review)
            db.session.add(new_review)
            db.session.commit()

            abort(200)

        except Exception as e:
            print(e)
            abort(404)


def start_api():
    app.run()
