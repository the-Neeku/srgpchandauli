from flask import Flask, render_template

app = Flask(__name__) 

@app.route('/')
def home():
    return render_template('MAIN.html')

@app.route('/FACILITY')
def facility():
    return render_template('FACILITY.html')

@app.route('/ADDMISSION')
def admission():
    return render_template('ADDMISION.html')

@app.route('/CONTACT')
def contact():
    return render_template('CONTACT.html')

@app.route('/ABOUT')
def about():
    return render_template('ABOUT.html')

if __name__ == '_main_': 
    app.run(debug=True)