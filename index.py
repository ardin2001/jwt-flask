import datetime
from functools import wraps
from flask import Flask, jsonify, make_response, render_template, request, session
import jwt
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tester'

def check_for_token(func):
    @wraps(func)
    def wrapped(*args,**kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'Missing token'}), 403
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Invalid token'}),403
        return func(*args,**kwargs)
    return wrapped

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('welcome.html')

@app.route('/public')
def public():
    return render_template('public.html')

@app.route('/auth')
@check_for_token
def authorised():
    return render_template('welcome.html')

@app.route('/login',methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == 'password':
        session['logged_in'] = True
        token = jwt.encode({
            'user' : request.form['username'],
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        },
        app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('utf-8')})
    else:
        return 'password false'
    
if __name__ == '__main__':
    app.run(debug=True)