# streamlit gui
import streamlit as st
import requests
from datetime import date

st.title('Sportsbook Data Scraper')

# User input for the date
selected_date = st.date_input("Choose a date for scraping:", min_value=date.today())

# User selection for sorting order
sort_order = st.selectbox("Select sort order for Sum of Odds:", ["Ascending", "Descending"])


# Define the function to fetch data from the Flask API
def fetch_data(date):
    # Update the URL to point to your Flask API endpoint
    url = f"http://127.0.0.1:5000/scrape?date={date.strftime('%Y-%m-%d')}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


if st.button('Scrape Data'):
    scraped_data = fetch_data(selected_date)

    if scraped_data:
        # Sort the scraped data by 'Sum of Odds' based on the selected sort order
        sorted_data = sorted(scraped_data, key=lambda x: x['Sum of Odds'], reverse=(sort_order == "Descending"))

        # Display each match's data from the sorted list
        for match in sorted_data:
            st.subheader(f"Teams: {match['Teams']}")
            st.write(f"Date and Time: {match['Date and Time']}")
            st.write(f"Odds: {match['Odds']}")
            st.write(f"Sum of Odds: {match['Sum of Odds']}")
            st.write("---")  # Separator
    else:
        st.error("Failed to fetch data or no data found for the selected date.")
