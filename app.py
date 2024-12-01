from flask import Flask, render_template

app = Flask(__name__) 

@app.route('/')
def home():
    return render_template('templates/MAIN.html')

@app.route('/facility')
def facility():
    return render_template('templates/FACILITY.html')

@app.route('/admission')
def admission():
    return render_template('templates/ADDMISION.html')

@app.route('/contact')
def contact():
    return render_template('templates/CONTACT.html')

@app.route('/about')
def about():
    return render_template('templates/ABOUT.html')

if __name__ == '_main_': 
    app.run(debug=True)