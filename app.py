from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import smtplib, ssl, os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.secret_key = "superstructure"  # needed for flash messages

# ------------------ Contact Form ------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        sender_email = "skillstackofficialinfo@gmail.com"
        receiver_email = "skillstackofficialinfo@gmail.com"
        password = "lxag crik ziam mgtd"  # Gmail App Password

        subject = f"New Contact Form Message from {name}"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        msg = f"Subject: {subject}\n\n{body}"

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg)

            flash("Message sent successfully! ✅")
        except Exception as e:
            flash(f"⚠️ Failed to send message: {str(e)}")

        return redirect(url_for("home"))

    return render_template("index.html")

# ------------------ Chatbot API ------------------
@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4o-mini" if available
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant. Explain coding errors and solve doubts clearly."},
                {"role": "user", "content": user_msg}
            ]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    return jsonify({"reply": reply})

# ------------------ Run App ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
