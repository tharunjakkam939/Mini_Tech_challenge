import os
import csv
import json
from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv

# Step 1: Load environment variables from the .env file
load_dotenv()

# Step 2: Initialize the Flask app and the Groq client
app = Flask(__name__)
try:
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    client = Groq(api_key=groq_api_key)
except ValueError as e:
    print(f"Error: {e}")
    client = None

# Define the output CSV file name
CSV_FILE = 'call_analysis.csv'

def analyze_transcript(transcript: str) -> dict:
    """
    Analyzes the transcript using the Groq API to get a summary and sentiment.
    """
    if not client:
        return {"error": "Groq client is not initialized. Check API key."}
        
    system_prompt = (
        "You are an expert in conversation analysis. "
        "Analyze the following customer call transcript. "
        "Provide a concise summary in 2-3 sentences. "
        "Also, determine the customer's sentiment as one of these three options: 'Positive', 'Neutral', or 'Negative'. "
        "Please respond with ONLY a valid JSON object with two keys: 'summary' and 'sentiment'."
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript},
            ],
            model="gemma2-9b-it", # <-- This is the updated, active model
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        response_content = chat_completion.choices[0].message.content
        return json.loads(response_content)
    except Exception as e:
        print(f"An error occurred with the Groq API: {e}")
        return {"summary": "Error in analysis.", "sentiment": "Unknown"}

def save_to_csv(data: dict):
    """
    Saves the analysis output into a .csv file.
    """
    file_exists = os.path.isfile(CSV_FILE)
    
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Transcript', 'Summary', 'Sentiment'])
        
        writer.writerow([
            data['transcript'],
            data['summary'],
            data['sentiment']
        ])

@app.route('/analyze', methods=['POST'])
def handle_analysis():
    """
    The main endpoint to accept a transcript and process it.
    """
    data = request.get_json()
    if not data or 'transcript' not in data:
        return jsonify({"error": "Missing 'transcript' in request body"}), 400

    transcript = data['transcript']
    
    analysis_result = analyze_transcript(transcript)

    if "error" in analysis_result:
        return jsonify(analysis_result), 500

    output_data = {
        "transcript": transcript,
        "summary": analysis_result.get("summary", "N/A"),
        "sentiment": analysis_result.get("sentiment", "N/A")
    }
    
    save_to_csv(output_data)

    print("--- Call Analysis Complete ---")
    print(f"Original Transcript: {output_data['transcript']}")
    print(f"Summary: {output_data['summary']}")
    print(f"Sentiment: {output_data['sentiment']}")
    print("----------------------------")
    
    return jsonify(output_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
