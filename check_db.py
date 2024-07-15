from flask import Flask
from models import db, Property, Auction
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    properties = Property.query.all()
    auctions = Auction.query.all()

    print("Properties:")
    for prop in properties:
        print(prop.serialize())

    print("\nAuctions:")
    for auction in auctions:
        print(auction.serialize())
