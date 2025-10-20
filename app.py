# app.py

import hashlib
import datetime
from flask import Flask, request, jsonify

# --- App Initialization and In-Memory Database ---
app = Flask(__name__)
# Using a simple dictionary as our in-memory database
# The key will be the string itself for quick lookups
strings_db = {}

# --- Helper Function for String Analysis ---
def analyze_string(input_str):
    """Computes all required properties for a given string."""
    # is_palindrome: case-insensitive check
    s_lower = input_str.lower()
    is_palindrome = s_lower == s_lower[::-1]

    # character_frequency_map
    freq_map = {}
    for char in input_str:
        freq_map[char] = freq_map.get(char, 0) + 1

    properties = {
        "length": len(input_str),
        "is_palindrome": is_palindrome,
        "unique_characters": len(set(input_str)),
        "word_count": len(input_str.split()),
        "sha256_hash": hashlib.sha256(input_str.encode()).hexdigest(),
        "character_frequency_map": freq_map
    }
    return properties

# --- API Endpoints ---

# 1. Create/Analyze a String
@app.route('/strings', methods=['POST'])
def create_string():
    # Check for valid JSON and 'value' field
    if not request.json or 'value' not in request.json:
        return jsonify({"error": "Invalid request body or missing 'value' field"}), 400
    
    value = request.json['value']

    # Check data type
    if not isinstance(value, str):
        return jsonify({"error": "Invalid data type for 'value', must be a string"}), 422

    # Check if string already exists
    if value in strings_db:
        return jsonify({"error": "String already exists in the system"}), 409

    # Analyze and store the string
    properties = analyze_string(value)
    new_entry = {
        "id": properties["sha256_hash"],
        "value": value,
        "properties": properties,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    strings_db[value] = new_entry

    return jsonify(new_entry), 201

# 2. Get a Specific String
@app.route('/strings/<string_value>', methods=['GET'])
def get_string(string_value):
    if string_value not in strings_db:
        return jsonify({"error": "String does not exist in the system"}), 404
    
    return jsonify(strings_db[string_value]), 200

# 5. Delete a String (Doing this before GET all for simplicity)
@app.route('/strings/<string_value>', methods=['DELETE'])
def delete_string(string_value):
    if string_value not in strings_db:
        return jsonify({"error": "String does not exist in the system"}), 404
    
    del strings_db[string_value]
    return '', 204 # Standard for successful DELETE is 204 No Content

# 3. Get All Strings with Filtering
@app.route('/strings', methods=['GET'])
def get_all_strings():
    args = request.args
    filters_applied = {}
    filtered_data = list(strings_db.values())

    try:
        # is_palindrome filter
        if 'is_palindrome' in args:
            is_palindrome_filter = args['is_palindrome'].lower() == 'true'
            filters_applied['is_palindrome'] = is_palindrome_filter
            filtered_data = [s for s in filtered_data if s['properties']['is_palindrome'] == is_palindrome_filter]

        # min_length filter
        if 'min_length' in args:
            min_len = int(args['min_length'])
            filters_applied['min_length'] = min_len
            filtered_data = [s for s in filtered_data if s['properties']['length'] >= min_len]

        # max_length filter
        if 'max_length' in args:
            max_len = int(args['max_length'])
            filters_applied['max_length'] = max_len
            filtered_data = [s for s in filtered_data if s['properties']['length'] <= max_len]

        # word_count filter
        if 'word_count' in args:
            wc = int(args['word_count'])
            filters_applied['word_count'] = wc
            filtered_data = [s for s in filtered_data if s['properties']['word_count'] == wc]
        
        # contains_character filter
        if 'contains_character' in args:
            char = args['contains_character']
            if len(char) != 1:
                raise ValueError("contains_character must be a single character")
            filters_applied['contains_character'] = char
            filtered_data = [s for s in filtered_data if char in s['value']]

    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid query parameter value: {e}"}), 400

    response = {
        "data": filtered_data,
        "count": len(filtered_data),
        "filters_applied": filters_applied
    }
    return jsonify(response), 200

# 4. Natural Language Filtering
@app.route('/strings/filter-by-natural-language', methods=['GET'])
def filter_natural_language():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    parsed_filters = {}
    
    if 'palindrome' in query or 'palindromic' in query:
        parsed_filters['is_palindrome'] = True
    
    if 'single word' in query:
        parsed_filters['word_count'] = 1
    
    if 'longer than' in query:
        try:
            length = int(query.split('longer than')[1].strip().split()[0])
            parsed_filters['min_length'] = length + 1
        except (ValueError, IndexError):
            return jsonify({"error": "Unable to parse length from query"}), 400
            
    if 'contain' in query or 'containing' in query:
        try:
            # Simple heuristic: find the letter in quotes or the first letter after 'letter'
            if 'the letter' in query:
                char = query.split('the letter')[1].strip()[0]
                parsed_filters['contains_character'] = char
            elif '"' in query:
                char = query.split('"')[1]
                if len(char) == 1:
                    parsed_filters['contains_character'] = char
        except IndexError:
            pass # Ignore if parsing fails

    # This part is tricky. Let's just apply the filters we found.
    # We can reuse the logic from the get_all_strings endpoint by applying our parsed filters.
    
    filtered_data = list(strings_db.values())
    
    if parsed_filters.get('is_palindrome'):
        filtered_data = [s for s in filtered_data if s['properties']['is_palindrome']]
    if 'word_count' in parsed_filters:
        filtered_data = [s for s in filtered_data if s['properties']['word_count'] == 1]
    if 'min_length' in parsed_filters:
        filtered_data = [s for s in filtered_data if s['properties']['length'] >= parsed_filters['min_length']]
    if 'contains_character' in parsed_filters:
        filtered_data = [s for s in filtered_data if parsed_filters['contains_character'] in s['value']]
    
    if not parsed_filters:
        return jsonify({"error": "Unable to parse natural language query"}), 400

    response = {
        "data": filtered_data,
        "count": len(filtered_data),
        "interpreted_query": {
            "original": request.args.get('query', ''),
            "parsed_filters": parsed_filters
        }
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)