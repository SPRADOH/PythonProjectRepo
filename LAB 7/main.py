import requests # type: ignore
import json
from datetime import datetime

# Your API key
API_KEY = '919784ee-64ca-46a0-b18c-728645cf096e'
URL = 'https://holidayapi.com/v1/holidays'

class SimpleHolidayAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.params = {'key': self.api_key}
        self.country = ''
        self.year = ''
    
    def set_query(self, country, year):
        self.country = country
        self.year = year
        print(f"Searching: {country}, {year}")
    
    def fetch_data(self):
        self.params['country'] = self.country
        self.params['year'] = self.year
        
        response = requests.get(URL, params=self.params)
        return response.json()
    
    def display(self, data):
        holidays = data.get('holidays', [])
        
        print("\n")
        print(f"HOLIDAYS IN {self.country} FOR {self.year}")
        print("\n")
        print(f"Total found: {len(holidays)}")
        print("\n")
        
        for i, h in enumerate(holidays[:5], 1):
            print(f"\n{i}. {h.get('name', 'N/A')}")
            print(f"   Date: {h.get('date', 'N/A')}")
            
            date_str = h.get('date', '')
            if date_str:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                weekday = date_obj.strftime('%A')
                print(f"   Weekday: {weekday}")
            
            print(f"   Public: {'Yes' if h.get('public') else 'No'}")
            print(f"   Observed: {h.get('observed', 'N/A')}")
            print(f"   Country: {self.country}")
        
        if len(holidays) == 0:
            print("\n  No holidays found for this country in 2025")
        
        print("\n")

# Available countries dictionary
COUNTRIES = {
    '1': {'code': 'US', 'name': 'United States'},
    '2': {'code': 'GB', 'name': 'United Kingdom'},
    '3': {'code': 'CA', 'name': 'Canada'},
    '4': {'code': 'FR', 'name': 'France'},
    '5': {'code': 'DE', 'name': 'Germany'},
    '6': {'code': 'JP', 'name': 'Japan'},
    '7': {'code': 'AU', 'name': 'Australia'},
    '8': {'code': 'BR', 'name': 'Brazil'},
    '9': {'code': 'IN', 'name': 'India'},
    '10': {'code': 'RU', 'name': 'Russia'},
    '11': {'code': 'CN', 'name': 'China'},
    '12': {'code': 'IT', 'name': 'Italy'},
    '13': {'code': 'ES', 'name': 'Spain'},
    '14': {'code': 'MX', 'name': 'Mexico'},
    '15': {'code': 'NG', 'name': 'Nigeria'},
    '16': {'code': 'ZA', 'name': 'South Africa'},
    '17': {'code': 'EG', 'name': 'Egypt'},
    '18': {'code': 'SA', 'name': 'Saudi Arabia'},
    '19': {'code': 'TR', 'name': 'Turkey'},
    '20': {'code': 'KR', 'name': 'South Korea'},
}

def show_menu():
    print("\n")
    print("HOLIDAY API PROGRAM - VARIANT 7")
    print("\n")
    print("YEAR: 2025 (Your plan supports 2025 only)")
    print("\n")
    print("OPTIONS:")
    print("1. Show holidays for ALL countries")
    print("2. Show holidays for a SPECIFIC country")
    print("3. Exit")
    print("\n")

def show_country_list():
    print("\nAVAILABLE COUNTRIES:")
    print("\n")
    for key, country in COUNTRIES.items():
        print(f"{key}. {country['name']} ({country['code']})")
    print("\n")

def get_country_choice():
    while True:
        choice = input("\nEnter country number (1-20): ").strip()
        if choice in COUNTRIES:
            return COUNTRIES[choice]['code'], COUNTRIES[choice]['name']
        else:
            print("Invalid choice. Please enter a number between 1 and 20.")

if __name__ == '__main__':
    api = SimpleHolidayAPI(API_KEY)
    year = 2025  # My plan only supports 2025
    
    while True:
        show_menu()
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            # Show for ALL countries
            print(f"\n")
            print(f"FETCHING HOLIDAYS FOR ALL COUNTRIES ({year})")
            print(f"\n")
            
            for key, country in COUNTRIES.items():
                print(f"\n{key}. {country['name']} ({country['code']})")
                print("\n")
                
                # Set option for each country
                api.set_query(country['code'], year)
                
                # Get data
                print("Fetching data...")
                result = api.fetch_data()
                
                # Display
                api.display(result)
                
                # Save raw JSON files
                filename = f'holidays_{country["code"]}_2025.json'
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2)
                print(f"Saved to {filename}")
                print()
            
            print("\n")
            print("ALL COUNTRIES COMPLETED!")
            print("\n")
            
        elif choice == '2':
            # Show for SPECIFIC country
            show_country_list()
            country_code, country_name = get_country_choice()
            
            print(f"\n")
            print(f"FETCHING HOLIDAYS FOR {country_name} ({country_code}) - {year}")
            print(f"\n")
            
            # Set option for selected country
            api.set_query(country_code, year)
            
            # get data
            print("Fetching data...")
            result = api.fetch_data()
            
            # Display
            api.display(result)
            
            # Save raw JSON
            filename = f'holidays_{country_code}_2025.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            print(f"Saved to {filename}")
            
        elif choice == '3':
            print("\nGoodbye! Thanks for using the Holiday API program!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
        
        input("\nPress Enter to continue...")