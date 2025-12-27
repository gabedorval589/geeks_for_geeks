from flask import Flask, redirect, url_for     
app = Flask(__name__)   # Flask constructor 
  
# A decorator used to tell the application 
# which URL is associated function 
@app.route('/')       
def hello(): 
    return 'HELLO'

# A decorator used to tell the application
# which URL is associated with the function
@app.route('/hello/<name>')
def hello_name(name):
    return f'Hello {name} !'  

@app.route('/blog/<int:postID>')
def show_blog(postID): 
    return 'Blog Number %d' % postID

@app.route('/admin')  # decorator for route(argument) function
def hello_admin():  # binding to hello_admin call
    return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):  # binding to hello_guest call
    return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':  # dynamic binding of URL to function
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest=name))

if __name__=='__main__': 
   app.run(debug=True, host="0.0.0.0")