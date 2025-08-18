# Import necessary classes and functions from the Flask module: Flask for the app, request for handling incoming requests, jsonify for creating JSON responses.
# Documentation: https://flask.palletsprojects.com/en/latest/api/#flask.Flask (for Flask), https://flask.palletsprojects.com/en/latest/api/#flask.request (for request), https://flask.palletsprojects.com/en/latest/api/#flask.jsonify (for jsonify)
from flask import Flask, request, jsonify

# Import CORS from flask_cors to handle Cross-Origin Resource Sharing.
# Documentation: https://flask-cors.readthedocs.io/en/latest/api.html#flask_cors.CORS
from flask_cors import CORS

# Create an instance of the Flask application, passing the current module name.
# Documentation: https://flask.palletsprojects.com/en/latest/api/#flask.Flask
app = Flask(__name__)

# Define the allowed frontend origin for CORS.
# This is a constant string; no specific Flask documentation needed.
FRONTEND_ORIGIN = "https://84fl4c.csb.app"

# Initialize CORS on the app with specific configurations: resources for /api/* paths, origins limited to the frontend, no credentials support, allowed methods, and headers.
# Documentation: https://flask-cors.readthedocs.io/en/latest/api.html#flask_cors.CORS
CORS(
    app,
    resources={r"/api/*": {"origins": [FRONTEND_ORIGIN]}},
    supports_credentials=False,
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

# Initialize a list to store messages, starting with a default message.
# This is standard Python; no Flask documentation needed.
MESSAGES = [{"id": 1, "text": "Hello from the server 👋"}]

# Define a route for GET requests to /api/health using the app.get decorator.
# Documentation: https://flask.palletsprojects.com/en/latest/api/#flask.Flask.get (shortcut for route with GET method)
@app.get("/api/health")
def health():
    # Return a JSON response with status information and HTTP status code 200.
    # Documentation: https://flask.palletsprojects.com/en/latest/api/#flask.jsonify
    return jsonify({"status": "ok", "service": "flask"}), 200

# Define a route for GET requests to /api/messages.
# Documentation: https://flask.palletsprojects.com/en/latest/api/#flask.Flask.get
@app.get("/api/messages")
def list_messages():
    # Return the list of messages as JSON with status 200.
    # Documentation: https://flask.palletsprojects.com/en/latest/api/#flask.jsonify
    return jsonify(MESSAGES), 200

# Define a route for POST requests to /api/messages.
# Documentation: https://flask.palletsprojects.com/en/latest/api/#flask.Flask.post (shortcut for route with POST method)
@app.post("/api/messages")
def add_message():
    # Parse the JSON data from the request, silently ignoring errors.
    # Documentation: https://flask.palletsprojects.com/en/latest/api/#flask.Request.get_json
    data = request.get_json(silent=True) or {}
    # Extract and strip the 'text' field from the data.
    # Standard Python dictionary access; no Flask documentation needed.
    text = (data.get("text") or "").strip()
    # Check if text is provided; if not, return error.
    # Standard Python conditional; no Flask documentation needed.
    if not text:
        # Return error JSON with status 400.
        # Documentation: https://flask.palletsprojects.com/en/latest/api/#flask.jsonify
        return jsonify({"error": "text is required"}), 400
    # Calculate the new message ID based on existing messages.
    # Standard Python list comprehension and max function; no Flask documentation needed.
    new_id = (max([m["id"] for m in MESSAGES]) + 1) if MESSAGES else 1
    # Create a new message dictionary.
    # Standard Python; no Flask documentation needed.
    msg = {"id": new_id, "text": text}
    # Append the new message to the list.
    # Standard Python list append; no Flask documentation needed.
    MESSAGES.append(msg)
    # Return the new message as JSON with status 201.
    # Documentation: https://flask.palletsprojects.com/en/latest/api/#flask.jsonify
    return jsonify(msg), 201

# Explicit route for OPTIONS requests to /api/messages (for CORS preflight).
# Documentation: https://flask.palletsprojects.com/en/latest/api/#flask.Flask.route
@app.route("/api/messages", methods=["OPTIONS"])
def options_messages():
    # Return empty response with status 204 for preflight.
    # Standard Flask return; documentation on responses: https://flask.palletsprojects.com/en/latest/api/#flask.make_response
    return ("", 204)

# Decorator to add a function that runs after each request.
# Documentation: https://flask.palletsprojects.com/en/latest/api/#flask.Flask.after_request
@app.after_request
def add_cors_headers(resp):
    # Set Access-Control-Allow-Origin header to the frontend origin.
    # Accessing response headers; documentation: https://flask.palletsprojects.com/en/latest/api/#flask.Response
    resp.headers["Access-Control-Allow-Origin"] = FRONTEND_ORIGIN
    # Set Vary header to Origin.
    resp.headers["Vary"] = "Origin"
    # Set allowed headers.
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    # Set allowed methods.
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    # Return the modified response.
    return resp

# Standard Python idiom to run the app only if the script is executed directly.
# Documentation for app.run: https://flask.palletsprojects.com/en/latest/api/#flask.Flask.run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
