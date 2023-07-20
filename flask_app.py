from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
import psycopg2
import os
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)

def analyze_link(link):
    # Make a request to the website
    r = requests.get(link)

    # Parse the webpage
    soup = BeautifulSoup(r.text, 'html.parser')

    # Extract the title of the webpage
    title = soup.title.text if soup.title else "No title found"

    # Extract the first few paragraphs of text
    paragraphs = soup.find_all('p')
    text = " ".join(p.text for p in paragraphs[:3])

    # Use GPT-3 to summarize the text
    openai.api_key = os.getenv("OPENAI_KEY")
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=f"{text}\n\nSummarize:",
      temperature=0.3,
      max_tokens=100,
    )

    summary = response.choices[0].text.strip()

    # Return a report
    return {
        "title": title,
        "link": link,
        "description": summary
    }

@app.route('/get_resource_data', methods=['GET'])
def get_resource_data():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="resource_links",
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="localhost"
    )

    # Create a cursor object
    cur = conn.cursor()

    # Execute the SELECT statement
    cur.execute("SELECT link FROM resources")

    # Fetch all the rows
    resource_links = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Analyze each link
    data = {f"resource{i+1}": analyze_link(link[0]) for i, link in enumerate(resource_links)}

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # specify the port number to be 5001
