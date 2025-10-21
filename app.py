# # app.py

# import hashlib
# import datetime
# from flask import Flask, request, jsonify

# # --- App Initialization and In-Memory Database ---
# app = Flask(__name__)
# strings_db = {}

# # --- Helper Function for String Analysis (No changes here) ---
# def analyze_string(input_str):
#     """Computes all required properties for a given string."""
#     s_lower = input_str.lower()
#     is_palindrome = s_lower == s_lower[::-1]
#     freq_map = {}
#     for char in input_str:
#         freq_map[char] = freq_map.get(char, 0) + 1
#     properties = {
#         "length": len(input_str),
#         "is_palindrome": is_palindrome,
#         "unique_characters": len(set(input_str)),
#         "word_count": len(input_str.split()),
#         "sha256_hash": hashlib.sha256(input_str.encode()).hexdigest(),
#         "character_frequency_map": freq_map
#     }
#     return properties

# # --- API Endpoints ---

# # FIX: Separate function for POST /strings
# @app.route('/strings', methods=['POST'])
# def create_string():
#     """Creates a new string entry."""
#     if not request.json or 'value' not in request.json:
#         return jsonify({"error": "Invalid request body or missing 'value' field"}), 400
    
#     value = request.json['value']
#     if not isinstance(value, str):
#         return jsonify({"error": "Invalid data type for 'value', must be a string"}), 422
#     if value in strings_db:
#         return jsonify({"error": "String already exists in the system"}), 409

#     properties = analyze_string(value)
#     new_entry = {
#         "id": properties["sha256_hash"],
#         "value": value,
#         "properties": properties,
#         "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
#     }
#     strings_db[value] = new_entry
#     return jsonify(new_entry), 201

# # FIX: Separate function for GET /strings
# @app.route('/strings', methods=['GET'])
# def get_strings_with_filters():
#     """Gets all strings, with optional filters."""
#     args = request.args
#     filters_applied = {}
#     filtered_data = list(strings_db.values())

#     try:
#         if 'is_palindrome' in args:
#             is_palindrome_filter = args['is_palindrome'].lower() == 'true'
#             filters_applied['is_palindrome'] = is_palindrome_filter
#             filtered_data = [s for s in filtered_data if s['properties']['is_palindrome'] == is_palindrome_filter]
#         if 'min_length' in args:
#             min_len = int(args['min_length'])
#             filters_applied['min_length'] = min_len
#             filtered_data = [s for s in filtered_data if s['properties']['length'] >= min_len]
#         if 'max_length' in args:
#             max_len = int(args['max_length'])
#             filters_applied['max_length'] = max_len
#             filtered_data = [s for s in filtered_data if s['properties']['length'] <= max_len]
#         if 'word_count' in args:
#             wc = int(args['word_count'])
#             filters_applied['word_count'] = wc
#             filtered_data = [s for s in filtered_data if s['properties']['word_count'] == wc]
#         if 'contains_character' in args:
#             char = args['contains_character']
#             if len(char) != 1: raise ValueError("contains_character must be a single character")
#             filters_applied['contains_character'] = char
#             filtered_data = [s for s in filtered_data if char in s['value']]
#     except (ValueError, TypeError) as e:
#         return jsonify({"error": f"Invalid query parameter value: {e}"}), 400

#     response = { "data": filtered_data, "count": len(filtered_data), "filters_applied": filters_applied }
#     return jsonify(response), 200

# # FIX: Separate function for GET /strings/<string_value>
# @app.route('/strings/<string_value>', methods=['GET'])
# def get_specific_string(string_value):
#     """Gets a specific string by its value."""
#     if string_value not in strings_db:
#         return jsonify({"error": "String does not exist in the system"}), 404
#     return jsonify(strings_db[string_value]), 200

# # FIX: Separate function for DELETE /strings/<string_value>
# @app.route('/strings/<string_value>', methods=['DELETE'])
# def delete_specific_string(string_value):
#     """Deletes a specific string by its value."""
#     if string_value not in strings_db:
#         return jsonify({"error": "String does not exist in the system"}), 404
#     del strings_db[string_value]
#     return '', 204

# # Natural Language Filtering (No changes needed here)
# @app.route('/strings/filter-by-natural-language', methods=['GET'])
# def filter_natural_language():
#     query = request.args.get('query', '').lower()
#     if not query: return jsonify({"error": "Missing 'query' parameter"}), 400
    
#     parsed_filters = {}
#     if 'palindrome' in query or 'palindromic' in query: parsed_filters['is_palindrome'] = True
#     if 'single word' in query: parsed_filters['word_count'] = 1
#     if 'longer than' in query:
#         try:
#             length = int(query.split('longer than')[1].strip().split()[0])
#             parsed_filters['min_length'] = length + 1
#         except (ValueError, IndexError): return jsonify({"error": "Unable to parse length from query"}), 400
#     if 'contain' in query or 'containing' in query:
#         try:
#             if 'the letter' in query: char = query.split('the letter')[1].strip()[0]
#             elif '"' in query: char = query.split('"')[1]
#             else: char = ''
#             if len(char) == 1: parsed_filters['contains_character'] = char
#         except IndexError: pass
    
#     if not parsed_filters: return jsonify({"error": "Unable to parse natural language query"}), 400
    
#     filtered_data = list(strings_db.values())
#     if parsed_filters.get('is_palindrome'): filtered_data = [s for s in filtered_data if s['properties']['is_palindrome']]
#     if 'word_count' in parsed_filters: filtered_data = [s for s in filtered_data if s['properties']['word_count'] == 1]
#     if 'min_length' in parsed_filters: filtered_data = [s for s in filtered_data if s['properties']['length'] >= parsed_filters['min_length']]
#     if 'contains_character' in parsed_filters: filtered_data = [s for s in filtered_data if parsed_filters['contains_character'] in s['value']]

#     response = { "data": filtered_data, "count": len(filtered_data), "interpreted_query": { "original": request.args.get('query', ''), "parsed_filters": parsed_filters } }
#     return jsonify(response), 200

# if __name__ == '__main__':
#     import os
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=True)




# app.py

import hashlib
import datetime
from flask import Flask, request, jsonify

# --- App Initialization and In-Memory Database ---
app = Flask(__name__)
strings_db = {}

# --- Helper Function for String Analysis (Verified Correct) ---
def analyze_string(input_str):
    """Computes all required properties for a given string."""
    s_lower = input_str.lower()
    is_palindrome = s_lower == s_lower[::-1]
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

@app.route('/strings', methods=['POST'])
def create_string():
    """Creates a new string entry."""
    if not request.json or 'value' not in request.json:
        return jsonify({"error": "Invalid request body or missing 'value' field"}), 400
    
    value = request.json['value']
    if not isinstance(value, str):
        return jsonify({"error": "Invalid data type for 'value', must be a string"}), 422
    if value in strings_db:
        return jsonify({"error": "String already exists in the system"}), 409

    properties = analyze_string(value)
    new_entry = {
        "id": properties["sha256_hash"],
        "value": value,
        "properties": properties,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    strings_db[value] = new_entry
    return jsonify(new_entry), 201

@app.route('/strings', methods=['GET'])
def get_strings_with_filters():
    """Gets all strings, with optional filters."""
    args = request.args
    filters_applied = {}
    filtered_data = list(strings_db.values())

    try:
        if 'is_palindrome' in args:
            is_palindrome_filter = args['is_palindrome'].lower() == 'true'
            filters_applied['is_palindrome'] = is_palindrome_filter
            filtered_data = [s for s in filtered_data if s['properties']['is_palindrome'] == is_palindrome_filter]
        if 'min_length' in args:
            min_len = int(args['min_length'])
            filters_applied['min_length'] = min_len
            filtered_data = [s for s in filtered_data if s['properties']['length'] >= min_len]
        if 'max_length' in args:
            max_len = int(args['max_length'])
            filters_applied['max_length'] = max_len
            filtered_data = [s for s in filtered_data if s['properties']['length'] <= max_len]
        if 'word_count' in args:
            wc = int(args['word_count'])
            filters_applied['word_count'] = wc
            filtered_data = [s for s in filtered_data if s['properties']['word_count'] == wc]
        if 'contains_character' in args:
            char = args['contains_character']
            if len(char) != 1: raise ValueError("contains_character must be a single character")
            filters_applied['contains_character'] = char
            filtered_data = [s for s in filtered_data if char in s['value']]
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid query parameter value: {e}"}), 400

    response = { "data": filtered_data, "count": len(filtered_data), "filters_applied": filters_applied }
    return jsonify(response), 200

@app.route('/strings/<string_value>', methods=['GET'])
def get_specific_string(string_value):
    """Gets a specific string by its value."""
    if string_value not in strings_db:
        return jsonify({"error": "String does not exist in the system"}), 404
    return jsonify(strings_db[string_value]), 200

@app.route('/strings/<string_value>', methods=['DELETE'])
def delete_specific_string(string_value):
    """Deletes a specific string by its value."""
    if string_value not in strings_db:
        return jsonify({"error": "String does not exist in the system"}), 404
    del strings_db[string_value]
    return '', 204

@app.route('/strings/filter-by-natural-language', methods=['GET'])
def filter_natural_language():
    query = request.args.get('query', '').lower()
    if not query: return jsonify({"error": "Missing 'query' parameter"}), 400
    
    parsed_filters = {}
    if 'palindrome' in query or 'palindromic' in query: parsed_filters['is_palindrome'] = True
    if 'single word' in query: parsed_filters['word_count'] = 1
    if 'longer than' in query:
        try:
            length = int(query.split('longer than')[1].strip().split()[0])
            parsed_filters['min_length'] = length + 1
        except (ValueError, IndexError): return jsonify({"error": "Unable to parse length from query"}), 400
    if 'contain' in query or 'containing' in query:
        try:
            if 'the letter' in query: char = query.split('the letter')[1].strip()[0]
            elif '"' in query: char = query.split('"')[1]
            else: char = ''
            if len(char) == 1: parsed_filters['contains_character'] = char
        except IndexError: pass
    
    if not parsed_filters: return jsonify({"error": "Unable to parse natural language query"}), 400
    
    filtered_data = list(strings_db.values())
    if parsed_filters.get('is_palindrome'): filtered_data = [s for s in filtered_data if s['properties']['is_palindrome']]
    if 'word_count' in parsed_filters: filtered_data = [s for s in filtered_data if s['properties']['word_count'] == 1]
    if 'min_length' in parsed_filters: filtered_data = [s for s in filtered_data if s['properties']['length'] >= parsed_filters['min_length']]
    if 'contains_character' in parsed_filters: filtered_data = [s for s in filtered_data if parsed_filters['contains_character'] in s['value']]

    response = { "data": filtered_data, "count": len(filtered_data), "interpreted_query": { "original": request.args.get('query', ''), "parsed_filters": parsed_filters } }
    return jsonify(response), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)