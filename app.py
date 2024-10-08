from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_graphql import GraphQLView
import graphene
from graphene import ObjectType, String, Int, List, DateTime, Boolean, InputObjectType, Mutation
from database import fetch_todos_from_database
import stripe
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from .config import KEYCLOAK_CONFIG, keycloak_openid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object('config.Config')
app.config.update(KEYCLOAK_CONFIG)
db.init_app(app)

stripe.api_key = 'your stripe api key here'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/templates/<path:path>')
def serve_templates(path):
    return send_from_directory('templates', path)
  

class Todo(ObjectType):
    id = Int()
    title = String()
    description = String()
    image_url = String()
    created_at = DateTime()

class Query(ObjectType):
    todos = List(Todo)

    def resolve_todos(self, info):
        return fetch_todos_from_database()

class AddTodoInput(InputObjectType):
    title = String(required=True)
    description = String()
    image_url = String()

class AddTodo(Mutation):
    class Arguments:
        input = AddTodoInput(required=True)

    ok = Boolean()

    def mutate(self, info, input):
        # add new todo to database
        return AddTodo(ok=True)

class DeleteTodoInput(InputObjectType):
    id = Int(required=True)

class DeleteTodo(Mutation):
    class Arguments:
        input = DeleteTodoInput(required=True)

    ok = Boolean()

    def mutate(self, info, input):
        # delete todo with given id from database
        return DeleteTodo(ok=True)

class EditTodoInput(InputObjectType):
    id = Int(required=True)
    title = String(required=True)
    description = String()
    image_url = String()

class EditTodo(Mutation):
    class Arguments:
        input = EditTodoInput(required=True)

    ok = Boolean()

    def mutate(self, info, input):
        # update todo with given id in database
        return EditTodo(ok=True)

class Mutation(ObjectType):
    add_todo = AddTodo.Field()
    delete_todo = DeleteTodo.Field()
    edit_todo = EditTodo.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True, **app.config))


schema = graphene.Schema(query=Query, mutation=Mutation)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

@app.route('/login/callback')
def login_callback():
    keycloak_openid.callback()
    return redirect(url_for('index'))

@app.route('/graphql', methods=['POST'])
@keycloak_openid.requires_authentication
def graphql_endpoint():
    # Your GraphQL endpoint implementation
    pass
  
if __name__ == '__main__':
    app.run(host='0.0.0.0' , debug=True)