import aiohttp

class FlightDataManager:
    """
    Async interactions with Sheety API.
    """
    def __init__(self, prices_endpoint, users_endpoint, username, password):
        self.prices_endpoint = prices_endpoint
        self.users_endpoint = users_endpoint
        self.auth = aiohttp.BasicAuth(login=username, password=password)

    async def get_destination_data(self, session: aiohttp.ClientSession):
        try:
            async with session.get(self.prices_endpoint, auth=self.auth) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get('prices', [])
        except Exception as e:
            print(f"Error fetching prices data: {e}")
            return []

    async def get_customer_emails(self, session: aiohttp.ClientSession):
        try:
            async with session.get(self.users_endpoint, auth=self.auth) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get('users', [])
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []

    async def update_iata_code(self, session: aiohttp.ClientSession, row_id: int, iata_code: str):
        url = f"{self.prices_endpoint}/{row_id}"
        body = {'price': {'iataCode': iata_code}}
        try:
            async with session.put(url, json=body, auth=self.auth) as response:
                response.raise_for_status()
        except Exception as e:
            print(f"Error updating IATA code: {e}")