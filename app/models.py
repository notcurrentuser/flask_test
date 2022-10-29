from sqlalchemy_utils import database_exists, create_database, drop_database

from app import db, app, DB_URL, POSTGRES_DB


class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    asin = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, title, asin):
        self.title = title
        self.asin = asin

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'Title': self.title,
            'Asin': self.asin
        }


class Review(db.Model):
    __tablename__ = 'reviews'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(120), db.ForeignKey('products.asin'), nullable=False)
    title = db.Column(db.String())
    review = db.Column(db.String())

    def __init__(self, asin, title, review):
        self.asin = asin
        self.title = title
        self.review = review

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'Asin': self.asin,
            'Title': self.title,
            'Review': self.review
        }


def reset_db():
    with app.app_context():
        if database_exists(DB_URL) and \
                input(f"Database {POSTGRES_DB} already exists, reset? Type 'y' to confirm\n").lower() == 'y':
            drop_database(DB_URL)
        create_database(DB_URL)
        db.create_all()
        print('Successfully created')
