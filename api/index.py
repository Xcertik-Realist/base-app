from flask import Flask, render_template, request, redirect, url_for
import datetime
import os

app = Flask(__name__)

# In-memory storage (note: lost when the serverless function sleeps)
# For a real app, consider Vercel KV, Postgres, or SQLite with persistence later
notes = []

@app.route("/")
def home():
    return render_template("index.html", notes=notes)

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
    notes = [note for note in notes if note["id"] != note_id]
    return redirect("/")

# This is required for Vercel to find the WSGI app
app = app  # Vercel looks for a variable named 'app'