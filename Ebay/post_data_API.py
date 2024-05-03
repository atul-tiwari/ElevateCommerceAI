import requests
import json

# Define your eBay Sandbox API credentials
sandbox_client_id = 'PiyushAr-EcomAI-SBX-eac2147f3-3a2644b9'
sandbox_client_secret = 'SBX-ac2147f3c427-dee1-4356-a464-1bf1'
sandbox_oauth_url = 'https://api.sandbox.ebay.com/identity/v1/oauth2/token'
sandbox_listing_url = 'https://api.sandbox.ebay.com/sell/inventory/v1/inventory_item'

# Get OAuth token
def get_access_token(client_id, client_secret, oauth_url):
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {client_id}:{client_secret}'}
    data = {'grant_type': 'client_credentials', 'scope': 'https://api.ebay.com/oauth/api_scope'}
    response = requests.post(oauth_url, headers=headers, data=data)
    return response.json()['access_token']

# Add a product listing
def add_product_listing(access_token, listing_url):
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}', 'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US'}
    payload = {
        "availability": {
            "shipToLocationAvailability": {
                "quantity": 10
            }
        },
        "condition": "NEW",
        "product": {
            "title": "Sample Product",
            "description": "This is a sample product description.",
            "imageUrls": [
                "https://www.example.com/image.jpg"
            ],
            "aspects": {
                "Brand": "Sample Brand"
            }
        },
        "productCode": "UPC123456789",
        "published": False
    }
    response = requests.post(listing_url, headers=headers, data=json.dumps(payload))
    return response.json()

# Main function
def main():
    access_token = get_access_token(sandbox_client_id, sandbox_client_secret, sandbox_oauth_url)
    response = add_product_listing(access_token, sandbox_listing_url)
    print(response)

if __name__ == '__main__':
    main()
