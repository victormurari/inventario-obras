import streamlit as st
import pandas as pd
import re

# App title
st.title("Artwork Inventory Generator")

st.markdown("Fill in the form below to register a new artwork.")

# Validation functions
def validate_year(value):
    return bool(re.match(r"^\d{4}(-\d{4})?$", value))

def validate_dimensions(value):
    return bool(re.match(r"^\d+(\.\d+)?x\d+(\.\d+)?\s?cm$", value.strip().lower()))

def validate_location(value):
    return value.replace(" ", "").isalpha() and value.istitle()

# Form fields
with st.form(key="artwork_form"):
    registry = st.text_input("Inventory/Registry Number")
    title = st.text_input("Title of the Artwork")
    artist = st.text_input("Artist/Author")
    year = st.text_input("Year or Period of Creation (e.g. 1990 or 1980-1990)")
    technique = st.text_input("Technique/Materials")
    dimensions = st.text_input("Dimensions (e.g. 30x40 cm)")
    location = st.text_input("Place of Production")
    provenance = st.text_input("Provenance/History")

    submit = st.form_submit_button("Submit")

# Initialize session data storage
if "entries" not in st.session_state:
    st.session_state["entries"] = []

# On submit
if submit:
    errors = []

    if not validate_year(year):
        errors.append("⚠️ 'Year or Period of Creation' must be in the format '1990' or '1980-1990'.")
    if not validate_dimensions(dimensions):
        errors.append("⚠️ 'Dimensions' must be in the format '30x40 cm'.")
    if not validate_location(location):
        errors.append("⚠️ 'Place of Production' must contain only letters and start with a capital letter.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        artwork = {
            "Inventory Number": registry,
            "Title": title,
            "Artist": artist,
            "Year/Period": year,
            "Technique": technique,
            "Dimensions": dimensions,
            "Place of Production": location,
            "Provenance/History": provenance
        }
        st.session_state["entries"].append(artwork)
        st.success("✅ Artwork successfully registered!")

# Display the table
if st.session_state["entries"]:
    st.markdown("### Registered Artworks:")
    df = pd.DataFrame(st.session_state["entries"])
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", data=csv, file_name="artwork_inventory.csv", mime="text/csv")
