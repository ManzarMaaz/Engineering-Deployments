# main.py
import os
import asyncio
import aiohttp
from datetime import date, timedelta
from dotenv import load_dotenv

from data_manager import FlightDataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

# --- Load Config ---
load_dotenv()
AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("API_SECRET")
TOKEN_ENDPOINT = os.getenv("TOKEN_ENDPOINT")
CITY_SEARCH_ENDPOINT = os.getenv("CITY_SEARCH_ENDPOINT")
FLIGHT_ENDPOINT = os.getenv("FLIGHT_ENDPOINT")
SHEETY_PRICES_ENDPOINT = os.getenv("SHEETY_PRICES_ENDPOINT")
SHEETY_USERS_ENDPOINT = os.getenv("SHEETY_USERS_ENDPOINT")
SHEETY_USERNAME = os.getenv("SHEETY_USERNAME")
SHEETY_PASSWORD = os.getenv("SHEETY_PASSWORD")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_VIRTUAL_NUMBER = os.getenv("TWILIO_VIRTUAL_NUMBER")
TWILIO_VERIFIED_NUMBER = os.getenv("TWILIO_VERIFIED_NUMBER")
MY_MAIL = os.getenv("MY_MAIL")
MY_PASS = os.getenv("MY_PASS")

ORIGIN_CITY_IATA = "HYD"
DEPARTURE_DATE = date.today() + timedelta(1)
ARRIVAL_DATE = DEPARTURE_DATE + timedelta(30)

# --- Worker Function for a Single City ---
async def process_city_task(semaphore, session, deal: FlightData, flight_search, notification_manager, user_data):
    """
    Handles the lifecycle for one city: 
    Check Direct -> Check Indirect -> Compare Price -> Notify.
    Uses a semaphore to ensure we don't spam the API too hard.
    """
    async with semaphore: # Limits concurrency
        if not deal.iata_code:
            print(f"⚠️  Skipping {deal.city_name}: Missing IATA code.")
            return

        print(f"🔎 Checking: {ORIGIN_CITY_IATA} -> {deal.city_name}...")

        # 1. Search Direct
        result = await flight_search.check_flights(
            session, ORIGIN_CITY_IATA, deal.iata_code, DEPARTURE_DATE, ARRIVAL_DATE, is_direct=True
        )

        # 2. Search Indirect if needed
        if not result:
            print(f"   No direct flight for {deal.city_name}. Trying indirect...")
            result = await flight_search.check_flights(
                session, ORIGIN_CITY_IATA, deal.iata_code, DEPARTURE_DATE, ARRIVAL_DATE, is_direct=False
            )

        # 3. Process Result
        if result:
            price_str, stops = result
            deal.cheapest_price = float(price_str)
            deal.stops = stops
            print(f"   ✅ Found {deal.city_name}: ₹{deal.cheapest_price}")

            if deal.cheapest_price < deal.target_price:
                print(f"   🚨 DEAL ALERT: {deal.city_name} is ₹{deal.cheapest_price} (Target: ₹{deal.target_price})")
                
                # --- Send Notifications (Sync calls inside Async flow) ---
                # Note: Sending SMS/Email is blocking here, but fast enough for this use case.
                
                sms_msg = f"Low Price! ₹{deal.cheapest_price} {ORIGIN_CITY_IATA}->{deal.iata_code} ({DEPARTURE_DATE}-{ARRIVAL_DATE})"
                notification_manager.send_sms(sms_msg)

                if user_data:
                    for user in user_data:
                        msg_body = f"Only ₹{deal.cheapest_price} to {deal.city_name}!"
                        notification_manager.send_individual_email(user['email'], "Flight Deal!", msg_body)
            else:
                print(f"   Pricing high for {deal.city_name}. (Current: {deal.cheapest_price} > Target: {deal.target_price})")
        else:
            print(f"   ❌ No flights found for {deal.city_name}.")

# --- Main Async Orchestrator ---
async def main():
    print("🚀 Starting Async Flight Tracker...")
    
    # 1. Init Managers
    data_manager = FlightDataManager(SHEETY_PRICES_ENDPOINT, SHEETY_USERS_ENDPOINT, SHEETY_USERNAME, SHEETY_PASSWORD)
    flight_search = FlightSearch(AMADEUS_API_KEY, API_SECRET, TOKEN_ENDPOINT, CITY_SEARCH_ENDPOINT, FLIGHT_ENDPOINT)
    notification_manager = NotificationManager(TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_VIRTUAL_NUMBER, TWILIO_VERIFIED_NUMBER, MY_MAIL, MY_PASS, "smtp.gmail.com")

    # 2. Create Session & Authenticate
    async with aiohttp.ClientSession() as session:
        # Authenticate Amadeus (Must be done first)
        await flight_search.authenticate(session)
        if not flight_search.headers:
            print("Authentication failed.")
            return

        # Fetch Sheet Data
        print("📥 Fetching Sheet Data...")
        sheet_data_raw = await data_manager.get_destination_data(session)
        user_data = await data_manager.get_customer_emails(session)

        # Convert to Objects
        flight_deals = [
            FlightData(
                city_name=row["city"],
                iata_code=row.get("iataCode", ""),
                target_price=float(row["lowestPrice"]),
                row_id=row["id"]
            ) for row in sheet_data_raw
        ]

        # 3. Handle Missing IATA Codes (Async Loop)
        print("🔎 Verifying IATA Codes...")
        iata_tasks = []
        for deal in flight_deals:
            if not deal.iata_code:
                # We define a tiny helper to fetch AND update
                async def fix_iata(d):
                    code = await flight_search.get_iata_code(session, d.city_name)
                    if code:
                        await data_manager.update_iata_code(session, d.row_id, code)
                        d.iata_code = code
                        print(f"   Updated IATA for {d.city_name} -> {code}")
                iata_tasks.append(fix_iata(deal))
        
        if iata_tasks:
            await asyncio.gather(*iata_tasks)

        # 4. Search Flights (Fan-Out)
        print("\n✈️  Launching Flight Search Tasks...")
        semaphore = asyncio.Semaphore(10) # Max 10 simultaneous requests
        tasks = []
        for deal in flight_deals:
            task = process_city_task(semaphore, session, deal, flight_search, notification_manager, user_data)
            tasks.append(task)
        
        # Fan-In: Wait for all to finish
        await asyncio.gather(*tasks)

    print("\n🏁 All checks completed.")

if __name__ == "__main__":
    # Ensure asyncio support for Windows if needed
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())