from flask import Flask, request, jsonify
from flask_cors import CORS

# Import your custom agents
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize agents
ingestion_agent = IngestionAgent()
retrieval_agent = RetrievalAgent()
llm_agent = LLMResponseAgent()

# Root route to check server status
@app.route('/')
def home():
    return jsonify({"status": "Agentic RAG Chatbot Backend is Running!"})

# Upload route
@app.route('/api/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({"error": "No files part in the request"}), 400

    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    try:
        for file in files:
            file_texts = ingestion_agent.process_file(file)
            retrieval_agent.embed_and_store(file_texts)
        return jsonify({"message": "Files uploaded and processed successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Query route
@app.route('/api/query', methods=['POST'])
def query():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing query in request"}), 400

    try:
        user_query = data['query']
        relevant_chunks = retrieval_agent.retrieve(user_query)
        answer = llm_agent.generate_answer(user_query, relevant_chunks)
        return jsonify({
            "answer": answer,
            "sources": relevant_chunks
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run app
if __name__ == '__main__':
    app.run(debug=True)