from flask import Flask
from flask_cors import CORS
from api.controllers.people_controller import people_controller
from api.controllers.transaction_controller import transaction_controller
from api.controllers.store_controller import store_controller
from api.controllers.items_controller import items_controller

app = Flask(__name__)
app.register_blueprint(people_controller, url_prefix='/venmito-felixdasta')
app.register_blueprint(transaction_controller, url_prefix='/venmito-felixdasta')
app.register_blueprint(store_controller, url_prefix='/venmito-felixdasta')
app.register_blueprint(items_controller, url_prefix='/venmito-felixdasta')

CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
