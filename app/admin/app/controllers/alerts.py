from .. import *

@app.route('/alerts', methods=['GET'])
def index():
    return render_template('alerts/index.html')