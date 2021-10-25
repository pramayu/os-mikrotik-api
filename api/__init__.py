from flask import Flask
from api.configure.def_config import Development
from api.controller import schema
from flask_graphql import GraphQLView
from api.filemodel.db import db_session
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv
from api.configure.middleware.webhook_receiver import webhook_receive

app = Flask('__main__')
CORS(app, supports_credentials=True, origins=['http://127.0.0.1:8080'])
app.secret_key = getenv('SESSION_KEY')
app.config.from_object(Development)
load_dotenv()

app.register_blueprint(webhook_receive)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql',
	schema=schema, graphiql=True))

@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()