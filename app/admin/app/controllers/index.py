from .. import *

@app.route('/', methods=['GET'])
def index():
    return render_template('index/index.html')