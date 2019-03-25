from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/fieldConfig')
def fieldConfig():
    return render_template('field.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
