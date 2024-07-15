def calculate_rank(property_data):
    return (
        property_data['assessed_value'] * 0.5 +
        property_data['tax_amount'] * 0.3 +
        (365 - property_data['days_to_auction']) * 0.2
    )
