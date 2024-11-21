import streamlit as st
import requests
import json
import base64

# API Endpoint
API_URL = "http://127.0.0.1:8000/bfhl"

# App Title
st.title("JSON Processor")

# Input Section
st.header("Input JSON")
json_input = st.text_area(
    "Enter JSON data (e.g., {\"data\": [\"A\", \"B\", \"1\"]})", height=150
)

# File Upload Section
st.header("Optional: Upload File")
uploaded_file = st.file_uploader("Upload a file to include in the request", type=["png", "jpg", "txt", "pdf"])

# Submit Button
if st.button("Submit"):
    try:
        # Parse JSON input
        payload = json.loads(json_input)

        # Handle file upload
        if uploaded_file is not None:
            file_content = uploaded_file.read()
            file_b64 = base64.b64encode(file_content).decode('utf-8')
            payload["file_b64"] = file_b64

        # Make API Call
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()
            st.success("Response received successfully!")

            # Filter Options
            st.header("Filter Results")
            filters = st.multiselect(
                "Choose what to display:",
                ["Numbers", "Alphabets", "Highest Lowercase Alphabet"],
            )

            # Display Results Based on Filter
            if "Numbers" in filters:
                st.subheader("Numbers")
                st.write(result.get("numbers", []))
            if "Alphabets" in filters:
                st.subheader("Alphabets")
                st.write(result.get("alphabets", []))
            if "Highest Lowercase Alphabet" in filters:
                st.subheader("Highest Lowercase Alphabet")
                st.write(result.get("highest_lowercase_alphabet", []))

            # File Results
            if "file_valid" in result:
                st.header("File Information")
                st.write(f"File Valid: {result.get('file_valid')}")
                st.write(f"MIME Type: {result.get('file_mime_type')}")
                st.write(f"File Size (KB): {result.get('file_size_kb')} KB")
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
    except json.JSONDecodeError:
        st.error("Invalid JSON format! Please check your input.")
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")

# Operation Code Endpoint
if st.button("Get Operation Code"):
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            st.write("Operation Code:", response.json().get("operation_code"))
        else:
            st.error(f"API Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
