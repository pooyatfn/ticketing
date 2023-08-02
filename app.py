from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///templates.db'
db = SQLAlchemy(app)


class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category_id': self.category_id
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id
        }


app.app_context().push()
db.create_all()

template_parser = reqparse.RequestParser()
template_parser.add_argument('title', type=str, required=True)
template_parser.add_argument('description', type=str, required=True)
template_parser.add_argument('category_id', type=int, required=True)

category_parser = reqparse.RequestParser()
category_parser.add_argument('name', type=str, required=True)
category_parser.add_argument('parent_id', type=int)


class TemplateResource(Resource):
    def get(self, template_id):
        template = Template.query.get(template_id)
        if template:
            return template.to_dict()
        else:
            return {'message': 'Template not found'}, 404

    def put(self, template_id):
        data = template_parser.parse_args()
        # Update the template in the database
        template = Template.query.get(template_id)
        if template:
            template.title = data['title']
            template.description = data['description']
            template.category_id = data['category_id']
            db.session.commit()
            return template.to_dict()
        else:
            return {'message': 'Template not found'}, 404

    def delete(self, template_id):
        # Delete the template from the database
        template = Template.query.get(template_id)
        if template:
            db.session.delete(template)
            db.session.commit()
            return {'message': 'Template deleted successfully'}
        else:
            return {'message': 'Template not found'}, 404


class TemplateListResource(Resource):
    def get(self, category_id):
        # Retrieve the templates from the database based on the category ID
        templates = Template.query.filter_by(category_id=category_id).all()
        return [template.to_dict() for template in templates]

    def post(self, category_id):
        data = template_parser.parse_args()
        template = Template(title=data['title'], description=data['description'], category_id=category_id)
        db.session.add(template)
        db.session.commit()
        return template.to_dict(), 201


class CategoryResource(Resource):
    def get(self, category_id):
        category = Category.query.get(category_id)
        if category:
            return category.to_dict()
        else:
            return {'message': 'Category not found'}, 404


if __name__ == '__main__':
    app.run()
