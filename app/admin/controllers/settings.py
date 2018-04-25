from .. import *

@app.route('/settings/web_panel', methods=['GET'])
def web_panel():
    return render_template('settings/web_panel.html')