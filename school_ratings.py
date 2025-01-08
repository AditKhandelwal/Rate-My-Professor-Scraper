import requests
import base64

# API Endpoint
API_URL = "https://www.ratemyprofessors.com/graphql"

# Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://www.ratemyprofessors.com",
    "Referer": "https://www.ratemyprofessors.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": "Basic dGVzdDp0ZXN0"
}

# Decoded School ID
school_id = "U2Nob29sLTQ3Njc="  # Base64 ID for UC Merced

# GraphQL Payload
payload = {
    "query": """
    query SchoolRatingsPageQuery($id: ID!) {
        school: node(id: $id) {
            __typename
            ... on School {
                id
                legacyId
                name
                city
                state
                country
                numRatings
                avgRatingRounded
                avgRating
                summary {
                    schoolReputation
                    schoolSatisfaction
                    campusCondition
                    schoolSafety
                    socialActivities
                    foodQuality
                }
            }
        }
    }
    """,
    "variables": {
        "id": school_id
    }
}

# Make the Request
response = requests.post(API_URL, headers=HEADERS, json=payload)

# Debugging: Print Raw Response
print("Status Code:", response.status_code)
print("Response Text:", response.text)

# Check if the response is JSON
try:
    data = response.json()
    school_data = data.get("data", {}).get("school", {})
    print("✅ School Data Fetched Successfully!")
    print(f"Name: {school_data.get('name')}")
    print(f"City: {school_data.get('city')}")
    print(f"State: {school_data.get('state')}")
    print(f"Country: {school_data.get('country')}")
    print(f"Number of Ratings: {school_data.get('numRatings')}")
    print(f"Average Rating: {school_data.get('avgRating')}")
    print(f"Campus Safety: {school_data.get('summary', {}).get('schoolSafety')}")
except requests.exceptions.JSONDecodeError:
    print("❌ Failed to decode JSON. Check the raw response above.")
