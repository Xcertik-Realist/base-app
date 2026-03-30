from flask import Flask, render_template, request, redirect
import datetime
import os

app = Flask(__name__)

# In-memory notes (will reset on cold start - normal for serverless)
notes = []

@app.route("/")
def home():
    try:
        return render_template("index.html", notes=notes)
    except Exception as e:
        # This will help show the real error in Vercel logs
        return f"Error rendering template: {str(e)}<br><br>Current path: {os.getcwd()}<br>Templates path: {app.template_folder}", 500

@app.route("/add", methods=["POST"])
def add_note():
    title = request.form.get("title", "Untitled").strip()
    content = request.form.get("content", "").strip()
    
    if content:
        notes.append({
            "id": len(notes) + 1,
            "title": title or "Untitled",
            "content": content,
            "time": datetime.datetime.now().strftime("%b %d, %H:%M")
        })
    
    return redirect("/")

@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    global notes
    notes = [n for n in notes if n["id"] != note_id]
    return redirect("/")

# Required for Vercel
app = app
