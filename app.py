"""Main script to run API server"""
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

data_df = pd.read_csv("data.csv")
ACCEPTABLE_VAR_NAMES = ["country", "age_group"] # data_df["var_name"].unique().to_list()

@app.route('/validate', methods=['POST'])
def validate():
    """Validates JSON request data. It checks that the var_name is either 
    "country" or "age". Then it checks that the combination of var_name and 
    category exists in the reference data.csv.

    The funciton expects a JSON payload with structure:
    {
        "data": [
            {
                "var_name": "country",
                "category": "USA"
            },
            ...
        ]
    }

    Returns:
        - 400 Bad Request if:
            - the requested format is invalid
            - the var_name is not in the reference csv
            - the var_name, category combination is not in the reference csv
        - 200 OK if it passes all validation checks
    """
    req_data = request.get_json()

    if not req_data or 'data' not in req_data:
        return jsonify({
            "error": "Invalid request. Must contain data json."
        }), 400
    
    for obj in req_data["data"]:
        var_name = obj.get("var_name")
        category = obj.get("category")

        # Checking var_name is valid
        if var_name not in ACCEPTABLE_VAR_NAMES:
            return jsonify({
                "error": f"Invalid var_name: {var_name}."
            }), 400
        
        # Checking category, var_name matches
        filtered_df = data_df[(data_df["var_name"] == var_name) & (data_df["category"] == category)]
        if len(filtered_df) == 0:
            return jsonify({
                "error": f"Invalid pair of var_name: {var_name} and category: {category}."
            }), 400
    return jsonify({"message": "Successfully validated"}), 200

if __name__ == '__main__':
    app.run(port=3000, debug=True)