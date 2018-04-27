from .. import *

@app.route('/layer3/overall_traffic', methods=['GET'])
def l3_overall_traffic():
    return render_template('layer3/overall_traffic.html')

@app.route('/layer3/ip', methods=['GET'])
def ip():
    return render_template('layer3/ip.html')

@app.route('/layer3/other', methods=['GET'])
def other():
    return render_template('layer3/other.html')