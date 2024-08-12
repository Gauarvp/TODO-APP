from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

class TodoModel(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    done = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Todo {self.id}>"

class TodoObject(SQLAlchemyObjectType):
    class Meta:
        model = TodoModel
        interfaces = (graphene.relay.Node, )

    def fetch_todos_from_database(self):
        todos = TodoModel.query.all()
        return [todo(
            id=todo.id,
            title=todo.title,
            completed=todo.completed
        ) for todo in todos]

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_todos = SQLAlchemyConnectionField(TodoObject.connection)

class CreateTodoMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        done = graphene.Boolean(required=True)

    todo = graphene.Field(lambda: TodoObject)