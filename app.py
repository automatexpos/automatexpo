from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client   # <-- added Client
from dotenv import load_dotenv
import os

load_dotenv()                # loads .env variables

app = Flask(__name__)

# initialise Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/consultation", methods=["POST"])
def consultation():
    try:
        data = request.json
        insert_data = {
            "name":  data.get("name"),
            "email": data.get("email"),
            "topic": data.get("topic")
        }

        resp = supabase.table("consultations").insert(insert_data).execute()

        if resp.data:          # success
            return jsonify({"status": "success",
                            "message": "Request received – we’ll be in touch within 24 hours."})
        else:                  # database error
            return jsonify({"status": "error", "message": "Database error"}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)