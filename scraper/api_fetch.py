import requests
import pandas as pd

# API Endpoint
API_URL = "https://www.ratemyprofessors.com/graphql"

# Headers for the request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Authorization": "Basic dGVzdDp0ZXN0"
}

# Function to fetch professors
def fetch_professors():
    professors = []
    has_next_page = True
    after = None  # Start with no cursor

    while has_next_page:
        # GraphQL Payload with Pagination Support
        payload = {
            "query": """
            query NewSearchTeachersQuery($query: TeacherSearchQuery!, $after: String) {
                newSearch {
                    teachers(query: $query, after: $after) {
                        edges {
                            node {
                                firstName
                                lastName
                                legacyId
                                department
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                }
            }
            """,
            "variables": {
                "query": {
                    "schoolID": 4767  # Filter professors by UC Merced's school ID
                },
                "after": after
            }
        }

        print(f"Fetching page with cursor: {after}")
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            try:
                data = response.json()
                print("Response JSON:", data)  # Debug: Print raw response JSON

                # Extract professors from the response
                teachers = data["data"]["newSearch"]["teachers"]
                for edge in teachers["edges"]:
                    node = edge["node"]
                    professors.append({
                        "First Name": node["firstName"],
                        "Last Name": node["lastName"],
                        "Legacy ID": node["legacyId"],
                        "Department": node["department"]
                    })

                # Handle pagination
                page_info = teachers["pageInfo"]
                has_next_page = page_info["hasNextPage"]
                after = page_info["endCursor"]  # Update cursor for next request
            except Exception as e:
                print(f"❌ Error processing response: {e}")
                break
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(response.text)
            break

    return professors

# Save professors to CSV
def save_professors_to_csv(professors):
    df = pd.DataFrame(professors)
    df.to_csv("uc_merced_professors.csv", index=False)
    print("✅ Data saved to uc_merced_professors.csv")

if __name__ == "__main__":
    professors = fetch_professors()
    if professors:
        save_professors_to_csv(professors)
        print(f"✅ Fetched {len(professors)} professors!")
    else:
        print("❌ No professors found.")
