from flask import Flask

from login_user import loginUser
from give_dataset import loadDataset

# Initiating App
app = Flask(__name__)

# Registering Blueprints
app.register_blueprint(loginUser)
app.register_blueprint(loadDataset)
 
if __name__ == "__main__":
    app.run(debug=True)