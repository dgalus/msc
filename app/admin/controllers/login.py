from .. import *

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET'])
def login():
    return render_template('login/index.html')

@app.route('/login', methods=['POST'])
def login_post():
    pass

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')