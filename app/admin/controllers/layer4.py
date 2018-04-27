from .. import *

@app.route('/layer4/overall_traffic', methods=['GET'])
def l4_overall_traffic():
    return render_template('layer4/overall_traffic.html')

@app.route('/layer4/tcp', methods=['GET'])
def tcp():
    return render_template('layer4/tcp.html')

@app.route('/layer4/udp', methods=['GET'])
def udp():
    return render_template('layer4/udp.html')

@app.route('/layer4/icmp', methods=['GET'])
def icmp():
    return render_template('layer4/icmp.html')