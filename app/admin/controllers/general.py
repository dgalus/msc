from .. import *

@app.route('/general/network_activity', methods=['GET'])
def network_activity():
    return render_template('general/network_activity.html')

@app.route('/general/popular_destinations', methods=['GET'])
def popular_destinations():
    return render_template('general/popular_destinations.html')

@app.route('/general/popular_sources', methods=['GET'])
def popular_sources():
    return render_template('general/popular_sources.html')