from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal
from flask import request
import os
import sqlite3
import json
from models import Schema as SchemaModel
from exts import db
from common.comm import auth_admin, auth_all
from config import *

# Define schema fields for serialization
schema_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'keywords': fields.String
}

class Schema(Resource):
    @auth_all(inject=False)
    @marshal_with(schema_fields)
    def get(self, schema_id):
        schema = SchemaModel.query.filter_by(id=schema_id).first()
        if schema:
            return schema, HTTP_OK
        else:
            return {}, HTTP_NotFound

    @auth_admin(inject=False)
    def delete(self, schema_id):
        schema = SchemaModel.query.filter_by(id=schema_id).first()
        if schema:
            os.remove(schema.path)
            db.session.delete(schema)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {}, HTTP_NotFound

class SchemaList(Resource):
    @auth_all(inject=False)
    def get(self):
        schemas = SchemaModel.query.all()
        data = [marshal(schema, schema_fields) for schema in schemas]
        return {'data': data}, HTTP_OK

    @auth_admin(inject=False)
    def post(self):
        request_data = request.get_json()
        schema_name = request_data.get('name')
        schema_description = request_data.get('description')

        if not schema_name:
            return get_shortage_error_dic('name'), HTTP_Bad_Request

        schema = SchemaModel(
            name=schema_name,
            description=schema_description,
            keywords=schema_name,
            path=os.path.join(save_db_path, f'{schema_name}.db')
        )

        db.session.add(schema)
        db.session.commit()

        # Create a new SQLite database for the schema
        with sqlite3.connect(schema.path) as conn:
            pass

        return {}, HTTP_Created
