# Handles API fetching

import requests
import pandas as pd

# API Endpoint
API_URL = "https://www.ratemyprofessors.com/graphql"

# Headers for the request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Authorization": "Basic dGVzdDp0ZXN0", 
    "Origin": "https://www.ratemyprofessors.com",
    "Referer": "https://www.ratemyprofessors.com/"
}

# GraphQL Query Payload
payload = {
    "query": """
    query NewSearchTeachersQuery($query: TeacherSearchQuery!) {
        newSearch {
            teachers(query: $query) {
                edges {
                    node {
                        firstName
                        lastName
                        legacyId
                        department
                    }
                }
            }
        }
    }
    """,
    "variables": {
        "query": {
            "text": "UC Merced"
        }
    }
}


# Fetch professors from Rate My Professors
def fetch_professors():
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    # Print response status and content for debugging
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)  # Print raw response text

    if response.status_code == 200:
        try:
            data = response.json()  # Attempt to parse JSON
            edges = data["data"]["newSearch"]["teachers"]["edges"]

            professors = []
            for edge in edges:
                node = edge["node"]
                professors.append({
                    "First Name": node["firstName"],
                    "Last Name": node["lastName"],
                    "Legacy ID": node["legacyId"],
                    "Department": node["department"]
                })

            return professors
        except requests.exceptions.JSONDecodeError:
            print("❌ Failed to parse JSON. Check the raw response above.")
            return []
    else:
        print(f"❌ Request failed with status code: {response.status_code}")
        return []


# Save data to a CSV file
def save_professors_to_csv(professors):
    df = pd.DataFrame(professors)
    df.to_csv("uc_merced_professors.csv", index=False)
    print("✅ Data saved to uc_merced_professors.csv")

if __name__ == "__main__":
    professors = fetch_professors()
    if professors:
        save_professors_to_csv(professors)
        print("✅ Professors fetched and saved successfully!")
    else:
        print("No professors found.")
