from flask import Flask, request
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Project Management API', description='A simple project management API')

# Data storage for projects and their dependencies (you can replace this with a database)
projects = {}
dependencies = {}

# Define a namespace for projects
project_ns = api.namespace('projects', description='Project operations')

# Define a data model for a project
project_model = api.model('Project', {
    'name': fields.String(required=True, description='Project name'),
    'description': fields.String(required=True, description='Project description')
})

# Define a data model for a dependency
dependency_model = api.model('Dependency', {
    'dependency_id': fields.String(required=True, description='Dependency project ID')
})

# Helper function to generate a unique project ID
def generate_project_id():
    project_ids = [int(pid.split('-')[1]) for pid in projects.keys() if pid.startswith('PN-')]
    if project_ids:
        new_id = max(project_ids) + 1
    else:
        new_id = 1
    return f'PN-{new_id:05d}'

@project_ns.route('/')
class ProjectList(Resource):
    @api.doc('list_projects')
    def get(self):
        '''List all projects'''
        return projects

    @api.doc('create_project')
    @api.expect(project_model)
    def post(self):
        '''Create a new project'''
        data = api.payload
        name = data.get('name')
        description = data.get('description')
        project_id = generate_project_id()
        projects[project_id] = {"name": name, "description": description, "dependencies": []}
        return {"message": "Project created successfully", "project_id": project_id}, 201

@project_ns.route('/<project_id>')
@api.response(404, 'Project not found')
class Project(Resource):
    @api.doc('get_project')
    def get(self, project_id):
        '''Get project details'''
        project = projects.get(project_id)
        if project:
            return project
        else:
            api.abort(404, "Project not found")

@project_ns.route('/<project_id>/dependencies')
@api.response(404, 'Project not found')
class ProjectDependencies(Resource):
    @api.doc('list_dependencies')
    def get(self, project_id):
        '''List project dependencies'''
        project = projects.get(project_id)
        if project:
            dependency_ids = project.get('dependencies', [])
            dependencies_list = [projects.get(dep_id) for dep_id in dependency_ids]
            return dependencies_list
        else:
            api.abort(404, "Project not found")

    @api.doc('add_dependency')
    @api.expect(dependency_model)
    @api.response(400, 'Invalid project or dependency')
    def post(self, project_id):
        '''Add a dependency to a project'''
        data = api.payload
        dependency_id = data.get('dependency_id')

        if project_id in projects and dependency_id in projects:
            projects[project_id]["dependencies"].append(dependency_id)
            return {"message": "Dependency added successfully"}
        else:
            api.abort(400, "Invalid project or dependency")

if __name__ == '__main__':
    app.run(debug=True)
