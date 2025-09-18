Call Transcript Analyzer using Groq API
This project is a simple Python server built with Flask that analyzes customer call transcripts. It uses the Groq API to perform fast AI-powered analysis, generating a concise summary and determining the customer's sentiment. The results are then saved to a CSV file for record-keeping. 



Features

API Endpoint: Accepts a call transcript via a POST request to the /analyze endpoint. 


AI-Powered Summary: Leverages the Groq API to generate a 2-3 sentence summary of the conversation. 


Sentiment Analysis: Extracts the customer's sentiment, classifying it as Positive, Neutral, or Negative. 



Data Storage: Saves the original transcript, summary, and sentiment into a call_analysis.csv file. 

Requirements
Python 3.7+

An active Groq API Key

The following Python libraries:

Flask

groq

python-dotenv

⚙️ Setup and Installation
Follow these steps to get the project running on your local machine.

1. Clone the Repository
Download or clone the project files to your local machine.

2. Create and Activate a Virtual Environment
Navigate to the project directory in your terminal and run the following commands:


# Create a virtual environment
python -m venv venv

# Activate the environment (Windows)
venv\Scripts\activate

# On macOS/Linux, use:
# source venv/bin/activate
3. Install Dependencies
Install the required Python libraries using pip:


pip install flask groq python-dotenv
4. Set Up Your API Key
Create a new file in the project folder named .env and add your Groq API key in the following format:

GROQ_API_KEY="YOUR_API_KEY_HERE"
▶️ How to Run
Start the Server:
With your virtual environment active, run the main application file from your terminal:


python app.py
The server will start and be available at http://127.0.0.1:5000.

Send a Request:
Open a new terminal window and use a tool like curl to send a transcript to the /analyze endpoint.

Example curl Command:


curl -X POST http://127.0.0.1:5000/analyze -H "Content-Type: application/json" -d "{\"transcript\": \"Hi, I was trying to book a slot yesterday but the payment failed. I tried it a couple of times and my card was charged, but I did not get a confirmation email. Can you please check what went wrong? This is quite frustrating.\"}"
📄 Example Flow

Input Transcript: "Hi, I was trying to book a slot yesterday but the payment failed..." 

Output in Server Terminal:

--- Call Analysis Complete ---
Original Transcript: Hi, I was trying to book a slot yesterday but the payment failed...
Summary: The customer reports a failed payment attempt for a booking, despite their card being charged, and a missing confirmation email. They express frustration with the situation. [cite: 12]
Sentiment: Negative 
----------------------------

Result in call_analysis.csv: 

A new row is added to the CSV file with the transcript, summary, and sentiment. 
