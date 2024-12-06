from flask import Flask, render_template

app = Flask(__name__) 

@app.route('/')
def home():
    return render_template('MAIN.html')

@app.route('/facility')
def facility():
    return render_template('FACILITY.html')

@app.route('/addmission')
def addmission():
    return render_template('ADDMISSION.html')

@app.route('/contact')
def contact():
    return render_template('CONTACT.html')

@app.route('/about')
def about():
    return render_template('ABOUT.html')

if __name__ == '_main_': 
    app.run(debug=True)