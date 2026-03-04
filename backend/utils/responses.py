
from flask import Flask, request, jsonify, send_from_directory, Response

# -----------------------------
# API Response Helpers
# -----------------------------

def success_response(data, status_code=200):
    return jsonify({
        "status": "success",
        "data": data
    }), status_code


def error_response(message, status_code=400):

    return jsonify({
        "status": "error",
        "message": message,
        "code": status_code
    }), status_code
