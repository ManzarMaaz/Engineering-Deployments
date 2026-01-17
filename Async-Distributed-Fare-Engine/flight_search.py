import aiohttp
import asyncio

class FlightSearch:
    """
    Async interactions with Amadeus API.
    """
    def __init__(self, api_key, api_secret, token_endpoint, city_endpoint, flight_endpoint):
        self.api_key = api_key
        self.api_secret = api_secret
        self.token_endpoint = token_endpoint
        self.city_endpoint = city_endpoint
        self.flight_endpoint = flight_endpoint
        self.headers = {} 

    async def authenticate(self, session: aiohttp.ClientSession):
        """
        Asynchronously fetches the OAuth token and sets the headers.
        """
        print("Acquiring new Amadeus access token...")
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }
        try:
            async with session.post(self.token_endpoint, headers=headers, data=body) as response:
                response.raise_for_status()
                data = await response.json()
                self.headers = {"Authorization": f"Bearer {data['access_token']}"}
                print("Token acquired successfully.")
        except Exception as e:
            print(f"Error getting Amadeus token: {e}")

    async def get_iata_code(self, session: aiohttp.ClientSession, city_name: str):
        """
        Async IATA code lookup.
        """
        city_params = {'keyword': city_name, 'max': '1'}
        try:
            async with session.get(self.city_endpoint, params=city_params, headers=self.headers) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                results = data.get('data', [])
                if results and 'iataCode' in results[0]:
                    return results[0]['iataCode']
                return None
        except Exception as e:
            print(f"Error searching city {city_name}: {e}")
            return None

    async def check_flights(self, session: aiohttp.ClientSession, origin_code, destination_code, departure_date, arrival_date, is_direct=True):
        """
        Async flight search.
        """
        non_stop_param = "true" if is_direct else "false"
        query = {
            "originLocationCode": origin_code,
            "destinationLocationCode": destination_code,
            "departureDate": departure_date.strftime("%Y-%m-%d"),
            "returnDate": arrival_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "currencyCode": "INR",
            "max": "1",
            "nonStop": non_stop_param
        }

        try:
            async with session.get(self.flight_endpoint, headers=self.headers, params=query) as response:
                if response.status != 200:
                    return None
                
                result = await response.json()
                if result.get('data') and len(result['data']) > 0:
                    flight_data = result['data'][0]
                    total_price = flight_data['price']['grandTotal']
                    stops = len(flight_data['itineraries'][0]['segments']) - 1
                    return total_price, stops
                return None
        except Exception as e:
            print(f"Error searching flight {origin_code}->{destination_code}: {e}")
            return None