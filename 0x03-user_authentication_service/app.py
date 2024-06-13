#!/usr/bin/env python3
"""
    Main flask app module file
"""

from flask import Flask


app = flask(__name__)


@app.route("/", methods=["GET"])
def root():
    """view function:
        response for the domain root
    """

    return jsonify({
            "message": "Bienvenue"
           })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
