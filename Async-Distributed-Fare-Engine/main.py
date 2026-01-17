# Standard Library Imports
import os
from datetime import date, timedelta

from data_manager import FlightDataManager
from dotenv import load_dotenv
from flight_data import FlightData
from flight_search import FlightSearch

# Import modules (classes) from local files
from notification_manager import NotificationManager

# ==============================================================================
# 1. CONFIGURATION CONSTANTS (Hardcoded to match procedural code)
# ==============================================================================
# Load environment variables from .env file (We rely on these to be the same)
load_dotenv()

# Amadeus Config (Using hardcoded keys from procedural code for consistency)
AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("API_SECRET")
TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT")
CITY_SEARCH_ENDPOINT = os.getenv("CITY_SEARCH_ENDPOINT")
FLIGHT_ENDPOINT = os.getenv("FLIGHT_ENDPOINT")

ORIGIN_CITY_IATA = "HYD"

DEPARTURE_DATE = date.today() + timedelta(1)
ARRIVAL_DATE = DEPARTURE_DATE + timedelta(30)

# Sheety Config (Using hardcoded URLs from procedural code)
SHEETY_PRICES_ENDPOINT = os.getenv("SHEETY_PRICES_ENDPOINT")
SHEETY_USERS_ENDPOINT = os.getenv("SHEETY_USERS_ENDPOINT")
SHEETY_USERNAME = os.getenv("SHEETY_USERNAME")
SHEETY_PASSWORD = os.getenv("SHEETY_PASSWORD")

# Twilio Config
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_VIRTUAL_NUMBER = os.getenv("TWILIO_VIRTUAL_NUMBER")
TWILIO_VERIFIED_NUMBER = os.getenv("TWILIO_VERIFIED_NUMBER")

# Email Config
MY_MAIL = os.getenv("MY_MAIL")
MY_PASS = os.getenv("MY_PASS")
SMTP_SERVER = "smtp.gmail.com"  # Required for smtplib


# ==============================================================================
# 2. MAIN ORCHESTRATION FUNCTION
# ==============================================================================
def run_flight_tracker():
    """Initializes managers and executes the core price checking loop."""

    # Initialize all services
    data_manager = FlightDataManager(
        SHEETY_PRICES_ENDPOINT, SHEETY_USERS_ENDPOINT, SHEETY_USERNAME, SHEETY_PASSWORD
    )
    flight_search = FlightSearch(
        AMADEUS_API_KEY,
        API_SECRET,
        TOKEN_ENDPOINT,
        CITY_SEARCH_ENDPOINT,
        FLIGHT_ENDPOINT,
    )
    notification_manager = NotificationManager(
        TWILIO_SID,
        TWILIO_AUTH_TOKEN,
        TWILIO_VIRTUAL_NUMBER,
        TWILIO_VERIFIED_NUMBER,
        MY_MAIL,
        MY_PASS,
        SMTP_SERVER,
    )

    # 1. Get destination and user data
    print("🔄 Fetching Destination Sheet from Sheety....")
    sheet_data = data_manager.get_destination_data()
    user_data = data_manager.get_customer_emails()

    if not sheet_data or not flight_search.access_token:
        print("Initialization failed (No data or no Amadeus token). Exiting.")
        return

    # Convert sheet data rows to FlightData objects
    flight_deals = [
        FlightData(
            city_name=row["city"],
            iata_code=row.get("iataCode", ""),
            target_price=float(row["lowestPrice"]),
            row_id=row["id"],
            stops=0,
        )
        for row in sheet_data
    ]

    # 2. Update IATA codes if missing
    for deal in flight_deals:
        if not deal.iata_code:
            print(f"🔄 Looking up IATA code for {deal.city_name}...")
            iata_code = flight_search.get_iata_code(deal.city_name)

            if iata_code:
                data_manager.update_iata_code(deal.row_id, iata_code)
                deal.iata_code = iata_code
                print(f"✅ IATA code updated to {iata_code}.")

    # 3. Search for flights and compare prices
    print("\n--- Starting Flight Search Loop ---\n")
    for deal in flight_deals:
        if not deal.iata_code:
            print(f"Skipping {deal.city_name}: Missing IATA code.")
            continue

        print(f"\n🔄 Getting Flight deals :✈️  {ORIGIN_CITY_IATA}  ➡️  {deal.city_name} ")

        # 3a. Attempt to find a DIRECT flight
        search_result = flight_search.check_flights(
            origin_code=ORIGIN_CITY_IATA,
            destination_code=deal.iata_code,
            departure_date=DEPARTURE_DATE,
            arrival_date=ARRIVAL_DATE,
            is_direct=True,
        )

        # 3b. If NO direct flight, search for INDIRECT flights
        if search_result is None:
            print(
                f"No direct flight found for {deal.city_name}. Searching for indirect..."
            )
            search_result = flight_search.check_flights(
                origin_code=ORIGIN_CITY_IATA,
                destination_code=deal.iata_code,
                departure_date=DEPARTURE_DATE,
                arrival_date=ARRIVAL_DATE,
                is_direct=False,
            )

        # 4. Process the Result
        if search_result:
            cheapest_price_str, stops_count = search_result
            deal.cheapest_price = float(cheapest_price_str)
            deal.stops = stops_count

            currency = "INR"

            if deal.stops == 0:
                flight_type = "Direct"
                print(f"✅ ✈️ {flight_type} flight found: ₹{deal.cheapest_price:.2f}")
            else:
                flight_type = "Indirect"
                print(
                    f"✅ ✈️ {flight_type} flight with {deal.stops} stops found: ₹{deal.cheapest_price:.2f}"
                )

            # 5. Compare prices and send alert
            if deal.cheapest_price < deal.target_price:
                # --- Twilio SMS Alert ---
                sms_message = f"Low Price alert! \nOnly ₹{deal.cheapest_price:.2f} to fly from {ORIGIN_CITY_IATA} to {deal.iata_code}, \nRound Trip: {DEPARTURE_DATE} -> {ARRIVAL_DATE}"
                notification_manager.send_sms(sms_message)

                # --- Email Alert (Sent to each user individually) ---
                if user_data:
                    for user_row in user_data:
                        first_name = user_row["firstName"]
                        last_name = user_row["lastName"]
                        email = user_row["email"]

                        email_subject = f"LOW PRICE ALERT: {deal.city_name} for {deal.cheapest_price:.2f} {currency}"

                        if deal.stops == 0:
                            email_body = (
                                f"Hi {first_name} {last_name},\n"
                                f"Only {deal.cheapest_price:.2f} {currency} to fly from {ORIGIN_CITY_IATA} to {deal.iata_code} (Direct Flight), "
                                f"with Departure on {DEPARTURE_DATE} and Arrival on {ARRIVAL_DATE}.\n\n"
                                f"Yours Sincerely,\nFlight Club."
                            )
                        else:
                            email_body = (
                                f"Hi {first_name} {last_name},\n"
                                f"Only {deal.cheapest_price:.2f} {currency} to fly from {ORIGIN_CITY_IATA} to {deal.iata_code} with {deal.stops} stop(s), "
                                f"with Departure on {DEPARTURE_DATE} and Arrival on {ARRIVAL_DATE}.\n\n"
                                f"Yours Sincerely,\nFlight Club."
                            )

                        notification_manager.send_individual_email(
                            email, email_subject, email_body
                        )

                else:
                    print("Skipping email notification: No customer emails found.")

            else:
                print(
                    f"Price {deal.cheapest_price:.2f} is higher than target {deal.target_price:.2f}. No alert sent.\n"
                )
        else:
            print(f"❌ No flights found for {deal.iata_code} (Direct or Indirect).\n")


if __name__ == "__main__":
    run_flight_tracker()
