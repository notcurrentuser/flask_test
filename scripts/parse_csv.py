import os

from tools.parser_csv import ParserCSV
from app import app, db, models


path = os.path.join(os.path.dirname(__file__), '../source_csv/')


def parse():
    products = ParserCSV(path, 'Products.csv').get_items()
    with app.app_context():
        for product in products:
            new_product = models.Product(title=product['Title'], asin=product['Asin'])
            db.session.add(new_product)
            db.session.commit()

    reviews = ParserCSV(path, 'Reviews.csv').get_items()
    with app.app_context():
        for review in reviews:
            new_review = models.Review(asin=review['Asin'], title=review['Title'], review=review['Review'])
            db.session.add(new_review)
            db.session.commit()
    print('The database is successfully filled')