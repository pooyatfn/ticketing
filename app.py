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


# Create the database tables
app.app_context().push()
db.create_all()

# Create a parser for request data
template_parser = reqparse.RequestParser()
template_parser.add_argument('title', type=str, required=True)
template_parser.add_argument('description', type=str, required=True)

category_parser = reqparse.RequestParser()
category_parser.add_argument('name', type=str, required=True)
category_parser.add_argument('parent_id', type=int)


# Create the resources for templates and categories
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


def category_exists(category_id):
    if Category.query.get(category_id):
        return True
    else:
        return False


class TemplateListResource(Resource):
    def get(self, category_id):
        if not category_exists(category_id):
            return {'message': 'Category does not exist'}
        # Retrieve the templates from the database based on the category ID
        templates = Template.query.filter_by(category_id=category_id).all()
        return [template.to_dict() for template in templates]

    def post(self, category_id):
        if not category_exists(category_id):
            return {'message': 'Category does not exist'}
        data = template_parser.parse_args()
        # Create a new template
        template = Template(title=data['title'], description=data['description'], category_id=category_id)
        db.session.add(template)
        db.session.commit()
        return template.to_dict(), 201


class CategoryResource(Resource):
    def get(self, category_id):
        # Retrieve the category from the database based on the ID
        category = Category.query.get(category_id)
        if category:
            return category.to_dict()
        else:
            return {'message': 'Category not found'}, 404

    def put(self, category_id):
        data = category_parser.parse_args()
        # Update the category in the database
        category = Category.query.get(category_id)
        if category:
            category.name = data['name']
            category.parent_id = data['parent_id']
            db.session.commit()
            return category.to_dict()
        else:
            return {'message': 'Category not found'}, 404

    def delete(self, category_id):
        # Delete the category from the database
        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return {'message': 'Category deleted successfully'}
        else:
            return {'message': 'Category not found'}, 404


class CategoryListResource(Resource):
    def get(self):
        # Retrieve all the categories from the database
        categories = Category.query.all()
        if categories:
            return [category.to_dict() for category in categories]
        else:
            return {'message': 'No category found'}, 404

    def post(self):
        data = category_parser.parse_args()
        parent_id = data['parent_id']

        if parent_id is not None:  # If a parent_id is provided...
            if not category_exists(parent_id):  # and if this parent_category does not exist...
                return {
                    'message': f'Category not created - parent category with id {parent_id} does not exist'}, 400

        # If no parent_id provided, or if it does exist, proceed to create the new category
        category = Category(name=data['name'], parent_id=parent_id)
        db.session.add(category)
        db.session.commit()
        return category.to_dict(), 201


# Add the resources to the API
api.add_resource(TemplateResource, '/templates/<int:template_id>')
api.add_resource(TemplateListResource, '/categories/<int:category_id>/templates')
api.add_resource(CategoryResource, '/categories/<int:category_id>')
api.add_resource(CategoryListResource, '/categories')

if __name__ == '__main__':
    app.run(debug=True)
