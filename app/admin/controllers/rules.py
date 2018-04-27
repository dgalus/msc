from .. import *

@app.route('/rules/iptables', methods=['GET'])
def iptables():
    return render_template('rules/iptables.html')