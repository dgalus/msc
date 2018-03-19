from .. import *

@app.route('/alerts', methods=['GET'])
def alerts():
    return render_template('alerts/index.html')