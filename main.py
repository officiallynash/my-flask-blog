from flask import Flask, Blueprint, session
import app.index as ind
import app.admin as adm

# Blueprint
index = ind.pub
admin = adm.adm

app = Flask(__name__)
app.secret_key = "very_secret_key" # SECRET_KEY
app.register_blueprint(index)
app.register_blueprint(admin)

app.run(host='0.0.0.0', port=5000)
