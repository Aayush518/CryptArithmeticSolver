from flask import Flask, render_template, request
from general import solve_cryptarithmetic

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_string = request.form['first_string'].upper()
        second_string = request.form['second_string'].upper()
        third_string = request.form['third_string'].upper()
        
        # Call the function to solve the cryptarithmetic puzzle
        solutions, statistics = solve_cryptarithmetic(first_string, second_string, third_string)
        
        # Pass the solutions and statistics to the template for rendering
        return render_template('index.html', solutions=solutions, statistics=statistics)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
