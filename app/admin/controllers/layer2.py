from .. import *

@app.route('/layer2/overall_traffic', methods=['GET'])
def l2_overall_traffic():
    return render_template('layer2/overall_traffic.html')