from models import *
import sqlite3
from common import for_sqlite
import json
from exts import db


def update_result(schema: Schema):
    for_sqlite.recover_schema(schema, True)
    questions = Question.query.filter_by(idSchema=schema.id)
    conn = sqlite3.connect(schema.path)
    cur = conn.cursor()
    for question in questions:
        if question.result is not None and question.result != '':
            answer = Answer.query.filter_by(idQuestion=question.id).first()
            assert answer
            result = for_sqlite.gen_answer_sql_result(schema, answer.sql)
            question.result = json.dumps(result)
            db.session.commit()
