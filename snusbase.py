
import os
import platform
import requests
import json

RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def save_to_file(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file)

class Snusbase:
    BASE_URL = "https://beta.snusbase.com/v2/combo/"

    def __init__(self):
        self.session = requests.Session()

    def search(self, term):
        url = f"{self.BASE_URL}{term}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return self.extract_data(data)
        except requests.RequestException as e:
            print(self.format_error_message(e))
            return None

    @staticmethod
    def extract_data(data):
        result = []
        for key in data.get("result", {}):
            result.extend(data["result"][key])
        return result

    def display_results(self, results):
        if not results:
            print("No results found.")
            return
        for item in results:
            print(f"Username: {item.get('username', 'N/A')}, Password: {item.get('password', 'N/A')}")

    def format_error_message(self, e):
        return f"[{RED}{e.response.status_code}{RESET}] {YELLOW}Client Error{RESET}: {e.response.reason} | URL: {BLUE}{e.request.url}{RESET}"

def main():
    clear_screen()
    snus = Snusbase()
    search_term = input("Enter the search term: ")
    results = snus.search(search_term)

    if results is not None:
        snus.display_results(results)
        save_file = input("Do you want to save the results to a file? (yes/no): ").strip().lower()
        if save_file == 'yes':
            save_to_file(results, f"output_{search_term}.json")
            print(f"Results saved to output_{search_term}.json")
    elif results is None:
        pass

if __name__ == '__main__':
    main()
