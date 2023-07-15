from flask_app import app
from flask_app.controllers import controllers_user
from flask_app.controllers import controllers_entry
from flask_app.controllers import controllers_favorite


if __name__=='__main__':
    app.run(debug=True)