import streamlit as st
import openai
import PyPDF2
from io import BytesIO
from jinja2 import Template
import json
import os
import re

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

def extract_text(file):
    """Extracts text from a PDF file."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def extract_information(text):
    """Uses OpenAI's API to extract information from the text."""
    prompt = f"""
You are an assistant that extracts specific information from car sales documents and formats it as JSON.

Please carefully extract the following information from the car sales document:

- **Seller's Full Name**: The person whose name appears after "(SELLER’S FULL NAME)" or who is transferring ownership.
- **Seller's Address**: The address appearing after the seller's name.
- **Buyer's Full Name**: The person whose name appears after "(BUYER’S FULL NAME)" or who is receiving ownership.
- **Buyer's Address**: The address appearing after the buyer's name.
- **Vehicle Make**
- **Vehicle Model**
- **Vehicle Year**
- **Vehicle Style**
- **Vehicle Color**
- **Vehicle Identification Number (VIN)**
- **Odometer Reading**
- **Seller Registration Number**
- **Sale Price**

If any information is missing or not found, indicate that it's missing.

**Important:** For the **Sale Date**, always output "MM/DD/YYYY" as a placeholder.

Format the output as a JSON object with the following keys:

- seller_name
- seller_address
- buyer_name
- buyer_address
- vehicle_make
- vehicle_model
- vehicle_year
- vehicle_style
- vehicle_color
- vin
- odometer_reading
- seller_registration_number
- sale_date
- sale_price

Ensure that your output is only the JSON object and nothing else.

Text:
{text}
"""

    # Using ChatCompletion API with gpt-3.5-turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500,
        temperature=0
    )

    # Extract the assistant's reply
    reply = response['choices'][0]['message']['content'].strip()

    # Clean up the reply to get the JSON object
    reply_clean = re.sub(r'^```(json)?', '', reply, flags=re.MULTILINE).strip('`').strip()
    # Try to extract JSON object from the reply
    json_match = re.search(r'\{.*\}', reply_clean, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
    else:
        json_str = reply_clean  # fallback to the whole reply

    return json_str

def generate_form(data):
    """Generates an HTML form with the extracted data."""
    # Set sale_date to "MM/DD/YYYY" as a placeholder
    data['sale_date'] = "01/06/2028"

    template = """
    <h1>State Authority Form</h1>
    <p><strong>Seller's Name:</strong> {{ seller_name }}</p>
    <p><strong>Seller's Address:</strong> {{ seller_address }}</p>
    <p><strong>Buyer's Name:</strong> {{ buyer_name }}</p>
    <p><strong>Buyer's Address:</strong> {{ buyer_address }}</p>
    <p><strong>Vehicle Make and Model:</strong> {{ vehicle_make }} {{ vehicle_model }} {{ vehicle_year }}</p>
    <p><strong>Vehicle Style:</strong> {{ vehicle_style }}</p>
    <p><strong>Vehicle Color:</strong> {{ vehicle_color }}</p>
    <p><strong>VIN:</strong> {{ vin }}</p>
    <p><strong>Odometer Reading:</strong> {{ odometer_reading }}</p>
    <p><strong>Seller Registration Number:</strong> {{ seller_registration_number }}</p>
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

                if not text.strip():
                    st.error("The uploaded PDF appears to be empty.")
                    return

                # Use LLM to extract information
                extracted_info = extract_information(text)

                # Try to parse the JSON output
                try:
                    data = json.loads(extracted_info)
                except json.JSONDecodeError as e:
                    st.error("Failed to extract information from the document. Please ensure the document contains the required information.")
                    st.error(f"JSON decoding error: {e}")
                    st.write("Assistant's response:")
                    st.code(extracted_info)
                    return

                # Check if all extracted values are missing
                if all(not value or 'missing' in str(value).lower() for value in data.values()):
                    st.error("No usable information was extracted from the document. Please upload a document with the required information filled in.")
                    return

                # Generate the form
                form_html = generate_form(data)

                st.success("Form generated successfully!")
                st.markdown(form_html, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
