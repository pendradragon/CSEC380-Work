import requests
L
url = "http://192.168.196.171/wp-login.php"

# Optional: set a User-Agent to look like a real browser
headers = {
    "User-Agent": "python-requests/2.x (+https://docs.python-requests.org/)"
}

try:
    resp = requests.get(url, headers=headers, timeout=10)  # timeout in seconds
    resp.raise_for_status()  # raise an exception for 4xx/5xx responses

    html = resp.text
    print("Successfully fetched WordPress login page (preview):\n")
    print(html[:500])  # print the first 500 characters as a preview

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e} (status code: {getattr(e.response, 'status_code', 'unknown')})")
except requests.exceptions.ConnectionError:
    print("Failed to connect to the server.")
except requests.exceptions.Timeout:
    print("Request timed out.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
