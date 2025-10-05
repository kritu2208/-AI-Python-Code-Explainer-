from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load a small T5 model for explanation
explainer = pipeline("text2text-generation", model="t5-small")

def explain_code(code_snippet):
    prompt = f"Explain this Python code in simple English:\n{code_snippet}"
    try:
        result = explainer(prompt, max_length=150, min_length=30, do_sample=False)
        explanation = result[0]['generated_text']
        return explanation
    except:
        return "Sorry, could not generate explanation."

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    explanation = ""
    
    if request.method == "POST":
        code = request.form.get("code")
        if code:
            explanation = explain_code(code)
    
    return render_template("index.html", code=code, explanation=explanation)

if __name__ == "__main__":
    app.run(debug=True)
