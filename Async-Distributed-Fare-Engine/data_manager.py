# data_manager.py
import requests

class FlightDataManager:
    """
    Manages interaction with the Google Sheet (via Sheety API) for 
    reading destination data, updating IATA codes, and fetching user data.
    """
    def __init__(self, prices_endpoint, users_endpoint, username, password):
        """
        Initializes the manager with Sheety credentials and endpoints.
        """
        self.prices_endpoint = prices_endpoint 
        self.users_endpoint = users_endpoint 
        self.auth = (username, password)

    def get_destination_data(self):
        """
        Fetches all destination rows and target prices from the sheet.
        """
        try:
            response = requests.get(url=self.prices_endpoint, auth=self.auth)
            response.raise_for_status()
            return response.json().get('prices', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching prices data from Sheety: {e}")
            return []

    def get_customer_emails(self):
        """
        Fetches all customer rows from the 'users' sheet.
        """
        try:
            response = requests.get(url=self.users_endpoint, auth=self.auth)
            response.raise_for_status()
            return response.json().get('users', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching customer data from Sheety: {e}")
            return []
    
    def update_iata_code(self, row_id: int, iata_code: str):
        """
        Updates a specific row in the sheet with the 3-letter IATA code.
        """
        sheety_updated_url = f"{self.prices_endpoint}/{row_id}"
        body = {
            'price': {
                'iataCode': iata_code
            }
        }
        try:
            response = requests.put(
                url=sheety_updated_url,
                json=body,
                auth=self.auth
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error updating IATA code in Sheety: {e}")