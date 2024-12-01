from flask import Flask, render_template

app = Flask(_name_) # type: ignore

@app.route('/')
def home():
    return render_template('MAIN.html')

@app.route('/facility')
def facility():
    return render_template('FACILITY.html')

@app.route('/admission')
def admission():
    return render_template('ADDMISION.html')

@app.route('/contact')
def contact():
    return render_template('CONTACT.html')

@app.route('/about')
def about():
    return render_template('ABOUT.html')

if _name_ == '_main_': # type: ignore
    app.run(debug=True)