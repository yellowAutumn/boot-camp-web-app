from flask import Flask, render_template, request, redirect, url_for
import logging
import sys
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

@app.route('/', methods=['GET', 'POST'])
def home():
    celsius = None
    fahrenheit = None
    if request.method == 'POST':
        user_input = request.form.get('fahrenheit', 'N/A')
        if isinstance(user_input, str) and user_input.strip().lower() == 'crash':
            logging.critical("Received 'crash' input. Crashing the application as requested.")
            sys.exit(1)
        try:
            fahrenheit = float(user_input)
            if fahrenheit < -100 or fahrenheit > 100:
                logging.warning(f"Validation failed: Input {fahrenheit} is out of range (-100 to 100)")
                return redirect(url_for('error', msg=f'Input must be between -100 and 100 Fahrenheit.'))
            celsius = (fahrenheit - 32) * 5.0/9.0
            logging.info(f"Valid input: {fahrenheit}°F, Result: {celsius}°C")
        except (ValueError, KeyError):
            logging.error(f"Validation failed: Invalid input '{user_input}'")
            return redirect(url_for('error', msg=f"Invalid input '{user_input}'. Please enter a number between -100 and 100."))
    return render_template('index.html', celsius=celsius, fahrenheit=fahrenheit)

@app.route('/error')
def error():
    msg = request.args.get('msg', 'An error occurred.')
    return render_template('error.html', msg=msg)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
