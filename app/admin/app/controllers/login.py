from .. import app

@app.route('/login', methods=['GET'])
def login():
    return "test"