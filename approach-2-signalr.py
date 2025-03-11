import requests
import time
import re
from bs4 import BeautifulSoup


class RajasthanScraper:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://epanjiyan.rajasthan.gov.in/"
        self.signalr_base = f"{self.base_url}signalr/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'X-MicrosoftAjax': 'Delta=true'
        }
        self.message_id = None
        self.connection_token = None

    def signalr_handshake(self):
        """Complete SignalR negotiation sequence"""
        # Negotiate
        negotiate_params = {
            'clientProtocol': '2.0',
            'connectionData': '[{"name":"messagehub"}]',
            '_': str(int(time.time() * 1000))
        }
        negotiate_resp = self.session.get(
            f"{self.signalr_base}negotiate",
            params=negotiate_params
        )
        negotiate_resp.raise_for_status()
        self.connection_token = negotiate_resp.json()['ConnectionToken']

        # Connect
        connect_params = {
            'transport': 'longPolling',
            'clientProtocol': '2.0',
            'connectionToken': self.connection_token
        }
        connect_resp = self.session.post(
            f"{self.signalr_base}connect",
            params=connect_params
        )
        connect_resp.raise_for_status()
        self.message_id = connect_resp.json().get('C')

        # Start
        start_params = {
            'transport': 'longPolling',
            'clientProtocol': '2.0',
            'connectionToken': self.connection_token,
            '_': str(int(time.time() * 1000))
        }
        start_resp = self.session.post(
            f"{self.signalr_base}start",
            params=start_params
        )
        start_resp.raise_for_status()

    def maintain_connection(self):
        """Maintain SignalR connection with polling"""
        poll_params = {
            'transport': 'longPolling',
            'clientProtocol': '2.0',
            'connectionToken': self.connection_token
        }
        poll_resp = self.session.post(
            f"{self.signalr_base}poll",
            params=poll_params,
            data=f"messageId={self.message_id}"
        )
        poll_resp.raise_for_status()
        self.message_id = poll_resp.json().get('C')

    def parse_form_state(self, response_text):
        """Parse both regular and encoded viewstate formats"""
        soup = BeautifulSoup(response_text, 'html.parser')
        fields = {}

        # Regular hidden inputs
        for hidden in soup.select('input[type=hidden]'):
            name = hidden.get('name')
            if name:
                fields[name] = hidden.get('value', '')

        # Encoded viewstate block
        encoded_block = soup.find(string=re.compile(r'\|\d+\|hiddenField\|'))
        if encoded_block:
            parts = encoded_block.split('|')
            i = 0
            while i < len(parts) - 4:
                if parts[i+1] == 'hiddenField':
                    fields[parts[i+2]] = parts[i+3]
                    i += 4
                else:
                    i += 1

        # Validate required fields
        required = ['__VIEWSTATE', '__EVENTVALIDATION', '__VIEWSTATEGENERATOR']
        for field in required:
            if field not in fields:
                raise ValueError(f"Missing required field: {field}")

        return fields, soup

    def execute_action(self, current_fields, event_target, event_value):
        """Execute postback with proper state management"""
        try:
            # Prepare post data
            post_data = {
                **current_fields,
                '__EVENTTARGET': event_target,
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                'ScriptManager1_HiddenField': '',
                'ctl00$ContentPlaceHolder1$a': 'rbtrural' if 'rbtrural' in current_fields else 'rbturban'
            }

            if event_value:
                post_data[event_target] = event_value

            # Execute request
            response = self.session.post(
                f"{self.base_url}e-search-page.aspx",
                data=post_data,
                headers={**self.headers,
                         'Referer': f"{self.base_url}e-search-page.aspx"}
            )
            response.raise_for_status()

            # Parse and validate new state
            new_fields, soup = self.parse_form_state(response.text)

            # Maintaining signalr connection
            self.maintain_connection()

            return new_fields, soup

        except Exception as e:
            print(f"Action failed: {str(e)}")
            raise

    def validate_selection(self, soup, element_id, expected_value):
        """Verify selection persistence in the DOM"""
        element = soup.find(id=element_id)
        if not element:
            raise ValueError(f"Element {element_id} not found")

        if 'checked' in element.attrs:
            actual_value = element.get('value')
        else:
            actual_value = element.find('option', selected=True)[
                'value'] if element.name == 'select' else None

        if str(actual_value) != str(expected_value):
            raise ValueError(
                f"Selection failed: Expected {expected_value}, got {actual_value}")

    def run(self):
        """Main workflow with proper state sequencing"""
        try:
            # Initial setup
            self.signalr_handshake()

            # Get initial state
            response = self.session.get(f"{self.base_url}e-search-page.aspx")
            current_fields, soup = self.parse_form_state(response.text)

            # Step 1: Select Rural
            print("➔ Selecting Rural...")
            current_fields, soup = self.execute_action(
                current_fields, 'ctl00$ContentPlaceHolder1$rbtrural', 'rbtrural')
            self.validate_selection(
                soup, 'ContentPlaceHolder1_rbtrural', 'rbtrural')

            # Step 2: Select District (AJMER=1)
            print("➔ Selecting District...")
            current_fields, soup = self.execute_action(
                current_fields, 'ctl00$ContentPlaceHolder1$ddlDistrict', '1')
            self.validate_selection(
                soup, 'ContentPlaceHolder1_ddlDistrict', '1')

            # Step 3: Get Tehsil options from current response
            print("➔ Fetching Tehsil options...")
            tehsil_select = soup.find(
                'select', id='ContentPlaceHolder1_ddlTehsil')
            if not tehsil_select:
                raise ValueError(
                    "Tehsil dropdown missing after district selection")

            tehsil_options = [opt['value'] for opt in tehsil_select.find_all(
                'option') if opt['value'].strip()]
            print(f"Available Tehsils: {tehsil_options}")

            if len(tehsil_options) < 2:
                raise ValueError("Tehsil options not populated")

            # Step 4: Select Tehsil
            print(f"➔ Selecting Tehsil: {tehsil_options[1]}...")
            current_fields, soup = self.execute_action(
                current_fields, 'ctl00$ContentPlaceHolder1$ddlTehsil', tehsil_options[1])
            self.validate_selection(
                soup, 'ContentPlaceHolder1_ddlTehsil', tehsil_options[1])

            print("All steps completed!")

        except Exception as e:
            print(f"Scraping failed: {str(e)}")
            raise


if __name__ == "__main__":
    scraper = RajasthanScraper()
    scraper.run()
