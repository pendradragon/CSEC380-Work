import urllib.request

url = "http://192.168.196.171/wp-login.php" #VM IP 

try:
    # Open the URL
    with urllib.request.urlopen(url) as response:
        # Read the response HTML
        html = response.read().decode('utf-8')
        
        # Print first 500 characters to confirm
        print("Successfully fetched WordPress login page:")
        print(html[:500])  # print a preview of the content

except urllib.error.URLError as e:
    print(f"Failed to reach server: {e.reason}")

except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
