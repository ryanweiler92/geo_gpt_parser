from flask import Flask, jsonify, request
from response_parse import parse_response
from detect_coordinate_system import detect_coordinate_system
from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env file
load_dotenv()

# app instance
app = Flask(__name__)

app.config["NOVA_API_KEY"] = os.environ.get("NOVA_API_KEY")
app.config["NOVA_API_BASE"] = os.environ.get("NOVA_API_BASE")

starting_prompt = """The very last sentence of this message is going to contain search criteria. 
I want you to use this last sentence to create a list (array) of objects that contain x and y coordinates.
Please use the webmercator coordinate system.
The objects should be in the following format: { name: 'name of location', lon: 'x', lat: 'y' }. 
The maximum length of this list should be 40."""


@app.route("/ask", methods=["POST"])
def get_completion():
    NOVA_API_KEY = app.config["NOVA_API_KEY"]
    NOVA_API_BASE = app.config["NOVA_API_BASE"]

    data = request.get_json()  # get the input data

    # check if 'content' is in data
    if "content" not in data:
        return jsonify({"error": "Content is required"}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOVA_API_KEY}",
    }

    payload_content = starting_prompt + " " + data["content"]
    print(payload_content)

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": payload_content}],
    }

    response = requests.post(
        f"{NOVA_API_BASE}/chat/completions", headers=headers, json=payload
    )

    if response.status_code == 200:
        content_value = response.json()["choices"][0]["message"]["content"]
        # Parse the response into a list of objects
        parsed_response = parse_response(content_value)

        # PRINT STATEMENTS FOR DEBUGGING

        print(content_value)
        print(parsed_response)

        # If the response is empty or we can't parse, return an empty list
        if len(parsed_response) == 0:
            return jsonify(parsed_response)

        # Detect if the coordinate system is EPSG:4326 or EPSG:3857
        coordinate_system = detect_coordinate_system(parsed_response)

        print(coordinate_system)

        return jsonify(parsed_response)
    else:
        return jsonify({"error": "Failed to get completion"}), 500


if __name__ == "__main__":
    app.run(debug=True)
