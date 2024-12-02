Note: brainrot this... using nosu

# Dealership Paperwork Automation MVP

This is a minimal viable product (MVP) that automates the process of filing paperwork with state authorities after a car dealership sells a car. The application uses OpenAI's GPT model to extract necessary information from uploaded sales documents and generates an auto-filled state form.

## Features

- **Upload Sales Documents**: Accepts PDF files of sales documents.
- **Automatic Information Extraction**: Uses an LLM to extract key information.
- **Auto-Filled Forms**: Generates a state authority form with the extracted data.
- **User-Friendly Interface**: Built with Streamlit for ease of use.

## Tech Stack

- **Python 3.x**
- **Streamlit** for the web interface.
- **OpenAI API** for language processing.
- **PyPDF2** for PDF text extraction.
- **Jinja2** for HTML templating.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher.
- An OpenAI API key. Sign up at [OpenAI](https://openai.com/) to obtain one.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/dealership-paperwork-automation.git
   cd dealership-paperwork-automation
