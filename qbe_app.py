"""Main script to run API server"""
import pandas as pd
from flask import Flask, jsonify, request


def create_app(config=None):
    """Wrapper to create flask app"""
    app = Flask(__name__)

    test = test+1

    if config is not None:
        app.config.from_mapping(config)

    data_df = pd.read_csv("data.csv")

    # Check that data_df is unique
    assert len(data_df) == len(
        data_df[["var_name", "category"]].drop_duplicates()
    ), "Duplicated records present"
    acceptable_var_names = list(
        data_df["var_name"].unique()
    )  # or manually ["country", "age_group"]

    @app.route("/", methods=["GET"])
    def index():
        """Checks the server running state"""
        return "Server is running"

    @app.route("/validate", methods=["POST"])
    def validate():
        """Validates JSON request data. It checks that the var_name is either
        "country" or "age". Then it checks that the combination of var_name and
        category exists in the reference data.csv.

        The function expects a JSON payload with structure:
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

        if not req_data or "data" not in req_data:
            return (
                jsonify({"error": "Invalid request. Must contain json with data key."}),
                400,
            )

        for obj in req_data["data"]:
            # Checking var_name is valid
            if "var_name" not in obj or "category" not in obj:
                return (
                    jsonify(
                        {
                            "error": "Invalid json. Must contain var_name and category fields."
                        }
                    ),
                    400,
                )

            var_name = obj.get("var_name")
            category = obj.get("category")

            # Checking var_name is valid
            if var_name not in acceptable_var_names:
                return jsonify({"error": f"Invalid var_name: {var_name}."}), 400

            # Checking category, var_name matches
            filtered_df = data_df[
                (data_df["var_name"] == var_name) & (data_df["category"] == category)
            ]
            if len(filtered_df) == 0:
                return (
                    jsonify(
                        {
                            "error": (
                                f"Invalid pair of var_name: {var_name} "
                                f"and category: {category}."
                            )
                        }
                    ),
                    400,
                )
        return jsonify({"message": "Successfully validated"}), 200

    @app.route("/get_factors", methods=["POST"])
    def get_factors():
        """Retrieves factors based var_name and category from reference
        csv. It first validates the request, before retrieving relevant
        factors.

        The function expects a JSON payload with structure:
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
            - 400 Bad Request if it fails validation checks.
            - 200 OK with the JSON of factors in "results".
        """
        req_data = request.get_json()

        validation_response = validate()
        if validation_response[1] != 200:
            return validation_response

        results_list = []
        for obj in req_data["data"]:
            var_name = obj.get("var_name")
            category = obj.get("category")

            # filtered_df is guaranteed len = 1
            filtered_df = data_df[
                (data_df["var_name"] == var_name) & (data_df["category"] == category)
            ]
            results_list.append(filtered_df.iloc[0].to_dict())
        return jsonify({"results": results_list}), 200

    return app


if __name__ == "__main__":
    qbe_app = create_app()
    qbe_app.run(port=3000, debug=True)
