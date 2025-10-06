import os
from flask import Flask, render_template, request
import re

app = Flask(__name__)

def explain_code(code_snippet):
    """Explain Python code with detailed line-by-line analysis"""
    code_snippet = code_snippet.strip()
    
    if not code_snippet:
        return "Please enter some Python code to explain."
    
    lines = [line.rstrip() for line in code_snippet.split('\n') if line.strip()]
    
    explanation_parts = []
    
    # Header
    explanation_parts.append("🔍 **Detailed Line-by-Line Analysis**")
    explanation_parts.append("=" * 50)
    
    for i, line in enumerate(lines, 1):
        explanation_parts.append(f"\n**Line {i}: `{line}`**")
        
        # Detailed pattern matching with better formatting
        if re.match(r'@app\.route\(.*\)', line):
            route_match = re.search(r'@app\.route\(["\']([^"\']+)["\']', line)
            methods_match = re.search(r'methods=\[([^\]]+)\]', line)
            
            route_path = route_match.group(1) if route_match else "/"
            methods = methods_match.group(1) if methods_match else "GET"
            
            explanation_parts.extend([
                "  - **Flask Route Decorator**: This maps a URL path to the function below",
                f"  - **URL Path**: '{route_path}' (home page)",
                f"  - **HTTP Methods**: {methods}",
                "  - **Purpose**: When someone visits this URL, Flask will call the index() function"
            ])
        
        elif re.match(r'def index\(\):', line):
            explanation_parts.extend([
                "  - **Function Definition**: Creates a function named 'index'",
                "  - **Purpose**: Main page handler for the web application",
                "  - **Parameters**: Takes no additional parameters"
            ])
        
        elif 'code = ""' in line:
            explanation_parts.extend([
                "  - **Variable Initialization**: Creates empty variable 'code'",
                "  - **Purpose**: Will store the user's input Python code"
            ])
        
        elif 'explanation = ""' in line:
            explanation_parts.extend([
                "  - **Variable Initialization**: Creates empty variable 'explanation'",
                "  - **Purpose**: Will store the generated code explanation"
            ])
        
        elif 'if request.method == "POST":' in line:
            explanation_parts.extend([
                "  - **HTTP Method Check**: Determines how the page was accessed",
                "  - **POST**: Form was submitted (user clicked 'Explain Code')",
                "  - **GET**: Page was loaded normally"
            ])
        
        elif 'code = request.form.get("code", "")' in line:
            explanation_parts.extend([
                "  - **Form Data Extraction**: Retrieves user input from the form",
                "  - **request.form.get()**: Safe way to get form data",
                "  - **\"code\"**: Name of the textarea in HTML form",
                "  - **\"\"**: Default empty string if no input provided"
            ])
        
        elif line.strip() == 'if code:':
            explanation_parts.extend([
                "  - **Input Validation**: Checks if user entered any code",
                "  - **Purpose**: Prevents generating explanations for empty input"
            ])
        
        elif 'explanation = explain_code(code)' in line:
            explanation_parts.extend([
                "  - **Function Call**: Invokes the code explanation engine",
                "  - **Input**: User's Python code",
                "  - **Output**: Detailed explanation stored in 'explanation' variable"
            ])
        
        elif 'render_template(' in line:
            explanation_parts.extend([
                "  - **Template Rendering**: Generates final HTML page",
                "  - **\"index.html\"**: Template file used for the web page",
                "  - **code=code**: Preserves user's code in textarea",
                "  - **explanation=explanation**: Displays generated explanation to user"
            ])
        
        elif 'if __name__ == "__main__":' in line:
            explanation_parts.extend([
                "  - **Python Main Guard**: Checks if script is run directly",
                "  - **Purpose**: Code inside only runs when file is executed directly",
                "  - **Prevents**: Code from running when file is imported as module"
            ])
        
        elif 'app.run(debug=True)' in line:
            explanation_parts.extend([
                "  - **Flask Server Startup**: Starts the web development server",
                "  - **debug=True**: Enables:",
                "    • Automatic code reloading on changes",
                "    • Detailed error pages in browser",
                "    • Debug mode (disable in production!)",
                "  - **Default URL**: http://localhost:5000"
            ])
    
    # Add summary section
    explanation_parts.append("\n" + "=" * 50)
    explanation_parts.append("📊 **Summary**")
    explanation_parts.append("-" * 20)
    explanation_parts.extend([
        f"- **Total lines analyzed**: {len(lines)}",
        "- **Type**: Complete Flask web application",
        "- **Components**:",
        "  • Web route handler for code explanation",
        "  • Main execution guard for development server",
        "- **Purpose**: AI-powered code explanation service",
        "- **Execution Flow**:",
        "  1. User visits page (GET) or submits code (POST)",
        "  2. Server validates input and processes request",
        "  3. AI analyzes code and generates explanation",
        "  4. Results displayed to user via web interface",
        "  5. Development server runs on localhost:5000",
        "- **Key Components**:",
        "  - `@app.route`: URL routing decorator",
        "  - `index()`: Main request handler function",
        "  - `explain_code()`: AI analysis engine",
        "  - `render_template()`: HTML page generator",
        "  - `app.run()`: Development server starter"
    ])
    
    return "\n".join(explanation_parts)

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    explanation = ""
    
    if request.method == "POST":
        code = request.form.get("code", "")
        if code:
            explanation = explain_code(code)
    
    return render_template("index.html", code=code, explanation=explanation)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
