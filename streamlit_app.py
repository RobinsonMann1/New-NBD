import streamlit as st
import requests
import uuid
import json

# --- USER CREDENTIALS ---
VALID_USERS = {
    "admin": "strongpassword123",  # username: password
    "rob": "boardclic2024"
}

# --- LOGIN MECHANISM ---
def login():
    st.title("🔒 Secure Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username in VALID_USERS and VALID_USERS[username] == password:
            st.session_state["authenticated"] = True
            st.success(f"Welcome, {username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# --- MAIN APP ---
def scraper_app():
    st.title("🔍 LinkedIn Sales Navigator Scraper")

    cookie_json = st.text_area("Paste LinkedIn Sales Navigator Cookie (JSON)", height=200)
    search_url = st.text_input("LinkedIn Sales Navigator Search URL")
    lead_count = st.number_input("Number of Leads to Generate", min_value=1, step=1)
    user_email = st.text_input("Your Email Address")

    if st.button("Submit and Run Scraper"):
        if not all([cookie_json, search_url, lead_count, user_email]):
            st.error("All fields are required.")
        else:
            try:
                parsed_cookie = json.loads(cookie_json)
                session_id = str(uuid.uuid4())

                payload = {
                    "session_id": session_id,
                    "cookie": parsed_cookie,
                    "search_url": search_url,
                    "lead_count": lead_count,
                    "user_email": user_email
                }

                webhook_url = "https://your-n8n-instance.com/webhook/linkedin-scraper"  # Replace with your real URL
                headers = {
                    "Authorization": "Bearer YOUR_BEARER_TOKEN_HERE",  # Replace with actual token
                    "Content-Type": "application/json"
                }

                with st.spinner("Sending request to scraper..."):
                    response = requests.post(webhook_url, headers=headers, json=payload)
                    response.raise_for_status()
                    result = response.json()

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

# --- APP ENTRY POINT ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    scraper_app()
else:
    login()
