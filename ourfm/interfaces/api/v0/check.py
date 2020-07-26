from flask_restplus import Resource
from flask import current_app as app
from ourfm import db

logger = app.logger


class Ok(Resource):

    def get(self):
        """Check the stack version and the database status."""
        response = {}
        error = False
        try:
            response["is_db_ok"] = db.session.execute("select true;").scalar()
        except Exception:
            response["is_db_ok"] = False
            error = True
        return response, 500 if error else 200
