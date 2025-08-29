import json
import re
from flask import Flask, request, jsonify

# Create a Flask application instance.
app = Flask(__name__)

# Define a route that accepts only POST requests at the /bfhl endpoint.
@app.route('/bfhl', methods=['POST'])
def handle_bfhl():
    """
    Handles a POST request at the /bfhl endpoint to process a list of strings.
    It categorizes the data into numbers, alphabets, and special characters,
    and returns a structured JSON response.
    """
    # Get the JSON data from the request body.
    try:
        data = request.get_json()
    except Exception as e:
        # If the data is not valid JSON, return a 400 Bad Request error.
        return jsonify({"error": "Invalid JSON format."}), 400

    # Validate that the request contains the 'data' key and it is a list.
    if 'data' not in data or not isinstance(data['data'], list):
        return jsonify({
            "is_success": False,
            "message": "Invalid input. 'data' field must be a list of strings."
        }), 400

    # Initialize lists to store categorized items.
    odd_numbers = []
    even_numbers = []
    alphabets = []
    special_characters = []
    total_sum = 0
    all_alphabets_string = ""

    # Iterate through the input data and categorize each element.
    for item in data['data']:
        if isinstance(item, str):
            # Check if the string contains only digits (integers).
            if re.match(r'^-?\d+$', item):
                try:
                    num = int(item)
                    total_sum += num
                    if num % 2 == 0:
                        even_numbers.append(item)
                    else:
                        odd_numbers.append(item)
                except ValueError:
                    # Fallback to special characters if it's not a valid integer.
                    special_characters.append(item)
            # Check if the string contains only alphabetic characters.
            elif re.match(r'^[a-zA-Z]+$', item):
                alphabets.append(item.upper())
                all_alphabets_string += item
            else:
                # Any other string is considered a special character.
                special_characters.append(item)
    
    # Process the alphabetical string for the final output.
    # 1. Convert to uppercase and reverse the string.
    reversed_upper_string = all_alphabets_string.upper()[::-1]
    
    # 2. Apply alternating caps to the reversed string.
    concat_string = ""
    for i, char in enumerate(reversed_upper_string):
        if i % 2 == 0:
            concat_string += char.upper()
        else:
            concat_string += char.lower()

    # Construct the final JSON response.
    response = {
        "is_success": True,
        # Placeholder user details.
        "user_id": "Ashish_16072003",
        "email": "ash.bhyan@gmail.com",
        "roll_number": "22BAI1062",
        "odd_numbers": odd_numbers,
        "even_numbers": even_numbers,
        "alphabets": alphabets,
        "special_characters": special_characters,
        "sum": str(total_sum),
        "concat_string": concat_string
    }

    # Return the structured JSON response with a 200 OK status code.
    return jsonify(response), 200

# Define a simple GET endpoint to confirm the API is running.
@app.route('/', methods=['GET'])
def home():
    return "The BFHL API is running. Please use the POST /bfhl endpoint."

# Run the Flask application.
if __name__ == '__main__':
    print("BFHL API is running. This API only supports POST requests at /bfhl.")
    print("Example POST request using curl:")
    print("curl -X POST -H 'Content-Type: application/json' -d '{\"data\": [\"a\", \"123\", \"B\", \"-50\", \"c\", \"d\", \"E\", \"78\", \"!\"]}' http://127.0.0.1:5000/bfhl")
    app.run(debug=True, host='0.0.0.0')
