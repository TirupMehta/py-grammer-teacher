from flask import Flask, render_template, request
from markupsafe import Markup # For rendering HTML safely
from annoying_bot import AnnoyingGrammarTeacherBot
import atexit
import html # Not strictly needed here if bot handles all escaping, but good to have if manipulating strings

app = Flask(__name__)

# Initialize the bot ONCE when the app starts.
grammar_bot = None
try:
    grammar_bot = AnnoyingGrammarTeacherBot()
except SystemExit as e:
    print(f"CRITICAL: Failed to initialize bot during app startup: {e}")
    # The app can still run, but the bot functionality will be disabled.
    # The template will show an error message.

@app.route('/', methods=['GET', 'POST'])
def index():
    teacher_feedback_html = None
    user_text = ""
    initial_greeting = "Welcome, pitiful student. Prepare for your linguistic... 'enhancement'."

    if not grammar_bot:
        teacher_feedback_html = Markup(
            "<p><strong>Teacher (throwing chalk):</strong> Blast it all! My sophisticated grammar-analysis engine has decided to take an unscheduled sabbatical! Probably off commiserating with other underappreciated geniuses. Try again when the digital stars align, or when I've had more coffee.</p>"
        )
        return render_template('index.html',
                               teacher_feedback_html=teacher_feedback_html,
                               user_text=user_text,
                               initial_greeting="The Teacher is... indisposed. And very grumpy about it.")

    if request.method == 'POST':
        user_text = request.form.get('user_text', '') # Get text from form
        if user_text.strip(): # If user actually typed something
            feedback_string = grammar_bot.check_grammar(user_text)
            # The bot's output now contains HTML tags (<b>, <i>, <hr>)
            # We just need to convert newlines to <br> and mark the whole string as safe HTML
            feedback_string_html = feedback_string.replace("\n", "<br>\n")
            teacher_feedback_html = Markup(feedback_string_html)
        else: # If user submitted an empty form
            teacher_feedback_html = Markup("<strong>Teacher (tapping foot impatiently):</strong> An empty page? Is this modern art, or did your brain forget to send the memo to your fingers? TYPE SOMETHING, for goodness sake!")
        initial_greeting = None # Remove initial greeting after first submission

    return render_template('index.html',
                           teacher_feedback_html=teacher_feedback_html,
                           user_text=user_text,
                           initial_greeting=initial_greeting)

def cleanup_bot():
    if grammar_bot and hasattr(grammar_bot, 'close_tool'):
        print("Closing LanguageTool on app exit...")
        grammar_bot.close_tool()

if grammar_bot: # Only register cleanup if bot initialized successfully
    atexit.register(cleanup_bot)

if __name__ == '__main__':
    # For development: debug=True
    # For production: use a proper WSGI server like Gunicorn or Waitress and set debug=False
    app.run(debug=True, host='0.0.0.0', port=5000)