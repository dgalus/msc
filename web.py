from app.admin import app
import json

if __name__ == '__main__':
    config = json.load(open("config.json"))
    app.run(host='0.0.0.0', port=config["admin_panel"]["port"], debug=True)