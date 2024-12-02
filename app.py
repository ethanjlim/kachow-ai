# app.py

import streamlit as st
import openai
import PyPDF2
from io import BytesIO
from jinja2 import Template
import json
import os

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

def extract_text(file):
    """Extracts text from a PDF file."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_information(text):
    """Uses OpenAI's API to extract information from the text."""
    prompt = f"""
    Extract the following information from the car sales document:
    - Buyer's Full Name
    - Buyer's Address
    - Vehicle Make and Model
    - Vehicle Identification Number (VIN)
    - Sale Date
    - Sale Price

    Format the output as JSON with keys:
    buyer_name, buyer_address, vehicle_make_model, vin, sale_date, sale_price.

    Text:
    {text}
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=300,
        temperature=0
    )

    return response.choices[0].text.strip()

def generate_form(data):
    """Generates an HTML form with the extracted data."""
    template = """
    <h1>State Authority Form</h1>
    <p><strong>Buyer's Name:</strong> {{ buyer_name }}</p>
    <p><strong>Buyer's Address:</strong> {{ buyer_address }}</p>
    <p><strong>Vehicle Make and Model:</strong> {{ vehicle_make_model }}</p>
    <p><strong>VIN:</strong> {{ vin }}</p>
    <p><strong>Sale Date:</strong> {{ sale_date }}</p>
    <p><strong>Sale Price:</strong> {{ sale_price }}</p>
    """
    html_template = Template(template)
    output = html_template.render(data)
    return output

def main():
    """Main function to run the Streamlit app."""
    st.title("Dealership Paperwork Automation")

    uploaded_file = st.file_uploader("Upload Sales Document (PDF)", type=["pdf"])

    if uploaded_file is not None:
        with st.spinner('Processing the document...'):
            try:
                # Extract text from the uploaded file
                text = extract_text(BytesIO(uploaded_file.read()))

                # Use LLM to extract information
                extracted_info = extract_information(text)

                # Parse the JSON output
                data = json.loads(extracted_info)

                # Generate the form
                form_html = generate_form(data)

                st.success("Form generated successfully!")
                st.markdown(form_html, unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.error("Failed to extract information from the document. Please ensure the document contains the required information.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
