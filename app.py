from flask import Flask, render_template, request, jsonify
from vectors import *
app = Flask(__name__)

ind = create_index_llama(dir)
query_engine(ind)
store_context = save_index1(ind)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    query = request.get_json().get("message")
    #response = get_response(text)
    sto_con = store_context
    response = load_reply_index1(sto_con, query)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)