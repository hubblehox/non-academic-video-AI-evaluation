from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Set the FastAPI endpoint URL (adjust the URL/port as needed)
FASTAPI_URL = "http://127.0.0.1:8000/predict"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve input parameters from the HTML form
        video_path = request.form.get("VideoPath")
        subject = request.form.get("subject")
        role = request.form.get("role")
        
        # Build the payload to send to FastAPI
        payload = [{
            "VideoPath": video_path,
            "subject": subject,
            "role": role
        }]
        
        try:
            # Send a POST request to the FastAPI endpoint
            response = requests.post(FASTAPI_URL, json=payload)
            response.raise_for_status()  # Raise error for bad status codes
            result = response.json()
        except Exception as e:
            result = {"error": str(e)}
        
        # Render a results page to show the returned data
        return render_template("result.html", result=result)
    
    # On GET, render the input form
    return render_template("form.html")

if __name__ == "__main__":
    app.run(port=9000, debug=True)
