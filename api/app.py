from flask import Flask

#Add the needed import paths
from api.controllers.people_controller import people_controller
from api.controllers.transaction_controller import transaction_controller

app = Flask(__name__)
app.register_blueprint(people_controller, url_prefix='/venmito-felixdasta')
app.register_blueprint(transaction_controller, url_prefix='/venmito-felixdasta')

if __name__ == '__main__':
    app.run(debug=True)
