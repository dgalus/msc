from app import app
from .. import user_config

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=user_config['admin_panel']['port'], debug=True)