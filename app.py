from flask import Flask, render_template
from models import db, Property, Auction
from routes import setup_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
with app.app_context():
    db.create_all()

    # Add sample data
    if not Property.query.all():
        sample_property = Property(
            address="123 Main St",
            assessed_value=250000,
            tax_amount=5000,
            days_to_auction=30,
            rank=1
        )
        db.session.add(sample_property)
        db.session.commit()

    if not Auction.query.all():
        sample_auction = Auction(
            property_id=1,
            date="2024-08-01",
            starting_bid=300000
        )
        db.session.add(sample_auction)
        db.session.commit()

setup_routes(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
