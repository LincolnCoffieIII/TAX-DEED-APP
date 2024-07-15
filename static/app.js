document.addEventListener('DOMContentLoaded', () => {
    loadProperties();
    loadAuctions();
    setupBidForm();
});

function loadProperties() {
    fetch('/properties')
        .then(response => response.json())
        .then(properties => {
            const propertyList = document.getElementById('property-list');
            propertyList.innerHTML = properties.map(property => createPropertyHTML(property)).join('');
        });
}

function createPropertyHTML(property) {
    return `
        <div class="property">
            <p>${property.address}</p>
            <p>Assessed Value: $${property.assessed_value}</p>
            <p>Tax Amount: $${property.tax_amount}</p>
            <p>Days to Auction: ${property.days_to_auction}</p>
            <p>Rank: ${property.rank}</p>
        </div>
    `;
}

function loadAuctions() {
    fetch('/auctions')
        .then(response => response.json())
        .then(auctions => {
            const auctionCalendar = document.getElementById('auction-calendar');
            auctionCalendar.innerHTML = auctions.map(auction => createAuctionHTML(auction)).join('');
        });
}

function createAuctionHTML(auction) {
    return `
        <div class="auction">
            <p>Property ID: ${auction.property_id}</p>
            <p>Date: ${new Date(auction.date).toLocaleDateString()}</p>
            <p>Starting Bid: $${auction.starting_bid}</p>
        </div>
    `;
}

function setupBidForm() {
    const bidForm = document.getElementById('bid-form-inner');
    if (bidForm) {
        bidForm.addEventListener('submit', processBid);
    }
}

function processBid(event) {
    event.preventDefault();
    const property_id = document.getElementById('property_id').value;
    const amount = document.getElementById('amount').value;
    const payment_method_id = 'your_payment_method_id'; // Retrieve this from Stripe Elements

    fetch('/bids', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ property_id, amount, payment_method_id })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Bid submitted successfully!');
        } else {
            alert('Failed to submit bid.');
        }
    });
}
