
import streamlit as st
import requests
import uuid
import json

# Set up page
st.title("LinkedIn Sales Navigator Scraper Interface")

# Input fields
cookie_json = st.text_area("Paste LinkedIn Sales Navigator Cookie (JSON)", height=200)
search_url = st.text_input("LinkedIn Sales Navigator Search URL")
lead_count = st.number_input("Number of Leads to Generate", min_value=1, step=1)
user_email = st.text_input("Your Email Address")

# Submit button
if st.button("Submit and Run Scraper"):
    if not all([cookie_json, search_url, lead_count, user_email]):
        st.error("All fields are required.")
    else:
        try:
            # Parse cookie to ensure it's valid JSON
            parsed_cookie = json.loads(cookie_json)

            # Generate random session ID
            session_id = str(uuid.uuid4())

            # Prepare payload
            payload = {
                "session_id": session_id,
                "cookie": parsed_cookie,
                "search_url": search_url,
                "lead_count": lead_count,
                "user_email": user_email
            }

            # Send POST request
            webhook_url = "https://your-n8n-instance.com/webhook/linkedin-scraper"  # Replace with your real URL
            headers = {
                "Authorization": "Bearer YOUR_BEARER_TOKEN_HERE",  # Replace with actual token
                "Content-Type": "application/json"
            }

            with st.spinner("Sending request to scraper..."):
                response = requests.post(webhook_url, headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()

                # Display Apify Scraper run logs
                logs = result.get("logs") or result.get("run_logs") or result
                st.success("Scraper launched successfully!")
                st.subheader("Apify Scraper Logs:")
                st.code(json.dumps(logs, indent=2), language='json')

        except json.JSONDecodeError:
            st.error("Invalid JSON in cookie input.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error contacting webhook: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")