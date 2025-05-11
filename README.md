# The Annoying Grammar Teacher Bot

**The Annoying Grammar Teacher Bot** is a highly interactive, language-focused web platform designed to not only identify grammar issues but to deliver critique with an unapologetically opinionated personality. More than just a grammar checker, it’s an engaging application that offers users a unique experience through dynamic feedback, context-aware sarcasm, and AI-powered linguistic suggestions.

---

## Overview

This application goes beyond basic grammar correction. It simulates a fully-fledged virtual grammar teacher with an attitude—designed to mimic the persona of an overly critical educator. It processes user-submitted text, analyzes it through LanguageTool's advanced natural language processing engine, and delivers layered, context-sensitive feedback wrapped in commentary that is both informative and entertaining.

The system is built to be extensible and structured for real-world application—serving as a blueprint for building engaging educational NLP tools.

---

## Features

* Deep grammar and syntax analysis via LanguageTool
* Rich, multi-level feedback delivered through a narrative interface
* Dynamic HTML formatting for highlighting issues and suggestions
* Stateless request-response processing for ease of scaling
* Structured separation of frontend, backend, and processing logic
* Easily customizable sarcasm/commentary profiles for tone modulation

---

## Technologies Used

* **Python 3** for application logic
* **Flask** for serving the web application
* **HTML/CSS** for responsive and styled UI
* **language\_tool\_python** for robust grammar and language analysis
* **Jinja2** templates for dynamic HTML rendering
* **LanguageTool Java backend** (via the Python bridge)

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/annoying-grammar-teacher.git
cd annoying-grammar-teacher
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If a `requirements.txt` file is not available, install manually:

```bash
pip install flask language_tool_python markupsafe
```

### 4. Run the Application

```bash
python app.py
```

Then, open your browser and navigate to:

```
http://localhost:5000
```

> To deploy this app online, consider services like Render, Railway, or Heroku and configure a WSGI server such as Gunicorn.

---

## File Structure

```
├── app.py                   # Web server and routing logic
├── annoying_bot.py         # Core logic for grammar evaluation and bot personality
├── index.html              # Frontend template rendered via Jinja2
├── README.md               # Project documentation
```

---

## Extensibility

This project is designed to be extensible:

* Modify `annoying_bot.py` to customize tone, error reporting structure, or even introduce multilingual support.
* Replace the markup rendering logic to suit mobile or API-based frontends.
* Integrate session management for user tracking and logging if building a full SaaS grammar tool.

---

## License

Licensed under the MIT License. See `LICENSE` file for details.

---

## Author

Built by [TirupMehta](https://github.com/TirupMehta), inspired by the idea that education and humor can coexist in code.
