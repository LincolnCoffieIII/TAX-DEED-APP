import requests
from bs4 import BeautifulSoup
from models import db, Property, Auction
from app import app

def scrape_properties():
    url = 'URL_OF_BELL_COUNTY_PROPERTY_LISTINGS'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    properties = []
    for item in soup.find_all('div', class_='property'):
        address = item.find('span', class_='address').text
        assessed_value = float(item.find('span', class_='assessed_value').text.replace('$', '').replace(',', ''))
        tax_amount = float(item.find('span', class_='tax_amount').text.replace('$', '').replace(',', ''))
        days_to_auction = int(item.find('span', class_='days_to_auction').text)
        rank = calculate_rank(assessed_value, tax_amount, days_to_auction)
        properties.append(Property(
            address=address,
            assessed_value=assessed_value,
            tax_amount=tax_amount,
            days_to_auction=days_to_auction,
            rank=rank
        ))

    return properties

def scrape_auctions():
    url = 'https://www.bellcountytx.com/county_government/county_clerk/foreclosures.php'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    auctions = []
    for item in soup.find_all('div', class_='auction'):
        property_id = int(item.find('span', class_='property_id').text)
        date = item.find('span', class_='date').text
        starting_bid = float(item.find('span', class_='starting_bid').text.replace('$', '').replace(',', ''))
        auctions.append(Auction(
            property_id=property_id,
            date=date,
            starting_bid=starting_bid
        ))

    return auctions

def calculate_rank(assessed_value, tax_amount, days_to_auction):
    return assessed_value / (tax_amount + days_to_auction)

def save_to_db():
    properties = scrape_properties()
    auctions = scrape_auctions()

    with app.app_context():
        db.session.bulk_save_objects(properties)
        db.session.bulk_save_objects(auctions)
        db.session.commit()

if __name__ == '__main__':
    save_to_db()
