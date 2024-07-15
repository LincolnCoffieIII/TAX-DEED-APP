from flask import request, jsonify
from models import Property, Auction, Purchase, db
import stripe

stripe.api_key = 'your_stripe_api_key'

def setup_routes(app):
    @app.route('/properties', methods=['GET'])
    def get_properties():
        properties = Property.query.all()
        return jsonify([p.serialize() for p in properties])

    @app.route('/auctions', methods=['GET', 'POST'])
    def manage_auctions():
        if request.method == 'GET':
            auctions = Auction.query.all()
            return jsonify([a.serialize() for a in auctions])
        elif request.method == 'POST':
            data = request.get_json()
            auction = Auction(**data)
            db.session.add(auction)
            db.session.commit()
            return jsonify(auction.serialize()), 201

    @app.route('/bids', methods=['POST'])
    def process_bid():
        data = request.get_json()
        property_id = data['property_id']
        amount = data['amount']
        payment_method_id = data['payment_method_id']
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency='usd',
            payment_method=payment_method_id,
            confirmation_method='manual',
            confirm=True,
        )
        purchase = Purchase(
            property_id=property_id,
            amount=amount,
            stripe_payment_id=payment_intent.id
        )
        db.session.add(purchase)
        db.session.commit()
        return jsonify({'status': 'success'}), 200
