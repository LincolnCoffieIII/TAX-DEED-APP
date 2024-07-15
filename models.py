from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128), nullable=False)
    assessed_value = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, nullable=False)
    days_to_auction = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'address': self.address,
            'assessed_value': self.assessed_value,
            'tax_amount': self.tax_amount,
            'days_to_auction': self.days_to_auction,
            'rank': self.rank
        }

class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    date = db.Column(db.String(128), nullable=False)
    starting_bid = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'date': self.date,
            'starting_bid': self.starting_bid
        }

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    stripe_payment_id = db.Column(db.String(128), nullable=False)
