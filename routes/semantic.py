from flask import Blueprint, request, jsonify
from views import SemanticView

SEMANTIC_BLUEPRINT = Blueprint("semantic", __name__, url_prefix="/document")

@SEMANTIC_BLUEPRINT.route("/search", methods=["POST"])
def run_agent():
    """
    endpoint to handle document search requests.
    """
    try:
        # Extract user input from the request
        user_input = request.json.get("query")
        max_messages=request.json.get("max_messages")
        user_id=request.json.get("user_id")
        if not user_input:
            return jsonify({"error": "Query is required"}), 400

        # Call the LangChain agent function
        result = SemanticView.run_agent_with_pgvector(user_input,user_id,max_messages)
        return jsonify({"response": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500