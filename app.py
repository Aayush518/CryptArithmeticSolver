from flask import Flask, render_template, request
from general import solve_cryptarithmetic, solve_extended_cryptarithmetic


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_string = request.form['first_string'].upper()
        second_string = request.form['second_string'].upper()
        third_string = request.form['third_string'].upper()

        solutions, statistics = solve_cryptarithmetic(first_string, second_string, third_string)

        return render_template('index.html', solutions=solutions, statistics=statistics)
    else:
        return render_template('index.html')

@app.route('/extended', methods=['GET', 'POST'])
def extended():
    if request.method == 'POST':
        first_string = request.form['first_string'].upper()
        second_string = request.form['second_string'].upper()
        third_string = request.form['third_string'].upper()
        fourth_string = request.form['fourth_string'].upper()

        solutions, statistics = solve_extended_cryptarithmetic(first_string, second_string, third_string, fourth_string)

        return render_template('extended.html', solutions=solutions, statistics=statistics)
    else:
        return render_template('extended.html')

if __name__ == '__main__':
    app.run(debug=True)
