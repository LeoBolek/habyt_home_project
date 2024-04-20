import requests
import csv

class Property:
    def __init__(self, propertyId, address):
        self.propertyId = propertyId
        self.address = address

class Unit:
    def __init__(self, unitId, occupancyType, propertyId, address, roomNumber):
        self.unitId = unitId
        self.occupancyType = occupancyType
        self.propertyId = propertyId
        self.address = address
        self.roomNumber = roomNumber

# Make HTTP request to fetch data
def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Transform data into object models
def transform_data(data):
    properties = []
    units = []
    applicants = []
    co_applicants = []
    prices = []
    concessions = []
    fees = []

    for item in data:
        propertyId = item['propertyId']
        address = item['address']['fullAddress']
        property_obj = Property(propertyId, address)
        properties.append(property_obj)

        units_data = item.get('units', [])
        for unit_data in units_data:
            unitId = unit_data['id']
            occupancyType = unit_data['occupancyType']
            roomNumber = unit_data['address']['roomNumber']
            
            unit_obj = Unit(unitId, occupancyType, propertyId, address, roomNumber)
            units.append(unit_obj)

            # Applicant data (assuming at least one applicant per unit)
            applicantId = unit_data['applicant']['id']
            applicant_obj = (applicantId, unitId)
            applicants.append(applicant_obj)

            # Co-applicants data (if present)
            co_applicants_data = unit_data.get('coApplicants', [])
            for co_applicant_data in co_applicants_data:
                coApplicantId = co_applicant_data['id']
                co_applicant_obj = (coApplicantId, applicantId)
                co_applicants.append(co_applicant_obj)

            # Price data
            prices_data = unit_data['pricing']['monthlyPricing']
            for price_data in prices_data:
                priceId = price_data['name']  # Using name as unique identifier for simplicity
                amount = price_data['amount']
                duration = price_data['months']
                price_obj = (priceId, unitId, amount, duration)
                prices.append(price_obj)

            # Concession data
            concessions_data = price_data['concessionsApplied']
            for concession_data in concessions_data:
                concessionId = concession_data  # Assuming concession names are unique
                concession_obj = (concessionId, unitId, None)  # No specific amount for concessions in the provided data
                concessions.append(concession_obj)

            # Fee data (assuming only one fee per unit)
            fees_data = unit_data.get('fees', [])
            for fee_data in fees_data:
                feeId = fee_data['name']
                fee_type = fee_data['description']
                amount = fee_data['amount']
                fee_obj = (feeId, unitId, fee_type, amount)
                fees.append(fee_obj)

    return properties, units, applicants, co_applicants, prices, concessions, fees

# Serialize object models and persist them as CSV files
def serialize_data(properties, units, applicants, co_applicants, prices, concessions, fees):
    # Write properties to CSV
    with open('properties.csv', 'w', newline='') as property_file:
        property_writer = csv.writer(property_file)
        property_writer.writerow(['propertyId', 'address'])
        for property_obj in properties:
            property_writer.writerow([property_obj.propertyId, property_obj.address])

    # Write units to CSV
    with open('units.csv', 'w', newline='') as unit_file:
        unit_writer = csv.writer(unit_file)
        unit_writer.writerow(['unitId', 'occupancyType', 'propertyId', 'address', 'roomNumber'])
        for unit_obj in units:
            unit_writer.writerow([unit_obj.unitId, unit_obj.occupancyType, unit_obj.propertyId, unit_obj.address, unit_obj.roomNumber])

    # Write applicants to CSV
    with open('applicants.csv', 'w', newline='') as applicant_file:
        applicant_writer = csv.writer(applicant_file)
        applicant_writer.writerow(['applicantId', 'unitId'])
        for applicant_obj in applicants:
            applicant_writer.writerow(applicant_obj)

    # Write co-applicants to CSV
    with open('co_applicants.csv', 'w', newline='') as co_applicant_file:
        co_applicant_writer = csv.writer(co_applicant_file)
        co_applicant_writer.writerow(['coApplicantId', 'applicantId'])
        for co_applicant_obj in co_applicants:
            co_applicant_writer.writerow(co_applicant_obj)

    # Write prices to CSV
    with open('prices.csv', 'w', newline='') as price_file:
        price_writer = csv.writer(price_file)
        price_writer.writerow(['priceId', 'unitId', 'amount', 'duration'])
        for price_obj in prices:
            price_writer.writerow(price_obj)

    # Write concessions to CSV
    with open('concessions.csv', 'w', newline='') as concession_file:
        concession_writer = csv.writer(concession_file)
        concession_writer.writerow(['concessionId', 'unitId', 'amount'])
        for concession_obj in concessions:
            concession_writer.writerow(concession_obj)

    # Write fees to CSV
    with open('fees.csv', 'w', newline='') as fee_file:
        fee_writer = csv.writer(fee_file)
        fee_writer.writerow(['feeId', 'unitId', 'type', 'amount'])
        for fee_obj in fees:
            fee_writer.writerow(fee_obj)

# Main function to orchestrate the process
def main():
    api_url = 'https://www.common.com/cmn-api/listings/common'
    data = fetch_data(api_url)
    if data:
        properties, units, applicants, co_applicants, prices, concessions, fees = transform_data(data)
        serialize_data(properties, units, applicants, co_applicants, prices, concessions, fees)
        print("Data serialized and saved as CSV files.")
    else:
        print("Failed to fetch data from the API.")

if __name__ == "__main__":
    main()
    