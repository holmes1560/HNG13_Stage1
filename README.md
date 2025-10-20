# Backend Wizards - Stage 1: String Analyzer Service

This is a RESTful API service built with Python and Flask that analyzes strings, computes their properties, and stores them. It allows users to create, retrieve, and delete analyzed strings, as well as filter them based on various properties.

## Features

-   Analyzes strings for properties like length, palindrome status, word count, and more.
-   Stores and retrieves string data.
-   Provides endpoints for creating, fetching, deleting, and filtering strings.
-   Includes a simple natural language query endpoint for basic filtering.
-   Uses an in-memory dictionary for data storage.

## Technology Stack

-   **Language:** Python
-   **Framework:** Flask
-   **Production Server:** Gunicorn
-   **Hosting:** Railway

## API Endpoints

### 1. Analyze a new string

-   **Endpoint:** `POST /strings`
-   **Request Body:**
    ```json
    {
      "value": "your string here"
    }
    ```
-   **Success Response (`201 Created`):** Returns the full object of the analyzed string.
-   **Error Responses:** `400 Bad Request`, `409 Conflict`, `422 Unprocessable Entity`.

### 2. Get a specific string

-   **Endpoint:** `GET /strings/{string_value}`
-   **Success Response (`200 OK`):** Returns the object for the requested string.
-   **Error Response:** `404 Not Found`.

### 3. Get all strings with filtering

-   **Endpoint:** `GET /strings`
-   **Query Parameters (optional):**
    -   `is_palindrome` (boolean)
    -   `min_length` (integer)
    -   `max_length` (integer)
    -   `word_count` (integer)
    -   `contains_character` (string)
-   **Success Response (`200 OK`):** Returns a list of strings that match the filters.

### 4. Filter strings using natural language

-   **Endpoint:** `GET /strings/filter-by-natural-language`
-   **Query Parameter:** `query` (e.g., "all single word palindromic strings")
-   **Success Response (`200 OK`):** Returns a list of matching strings.

### 5. Delete a string

-   **Endpoint:** `DELETE /strings/{string_value}`
-   **Success Response (`204 No Content`):** Returns an empty body.
-   **Error Response:** `404 Not Found`.

## Local Setup

To run this project locally, follow these steps:

1.  **Clone the repository.**
2.  **Create and activate a virtual environment:** `python -m venv venv` then `.\venv\Scripts\activate`.
3.  **Install dependencies:** `pip install -r requirements.txt`.
4.  **Run the application:** `python app.py`.

The API will be accessible at `http://127.0.0.1:5000`.