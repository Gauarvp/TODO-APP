from flask import Flask
from keycloak import KeycloakOpenID

app = Flask(__name__)

keycloak_openid = KeycloakOpenID(server_url='http://localhost:8080/auth',
                                client_id='test-web-app',
                                realm_name='Gaurav',
                                client_secret_key='3QrrgDJoYMFC7G8wN79dJTxq4BGakD4BR')

