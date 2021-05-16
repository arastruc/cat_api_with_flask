import uuid
from dao.models import Author
from flask_restplus import Namespace, Resource, fields
from flask import Response

from dao.db import db


api = Namespace('authors', description='Authors related operations')

author = api.model(
    'Author',
    {'id': fields.String(description='The id', attribute="author_id"),
     'firstName': fields.String(description='The first name', required=True, attribute="first_name"),
     'lastName': fields.String(description='The last name', required=True, attribute="last_name"),
     'nationality': fields.String(description='The nationality of the author'),
     })

author_list = {
    'datas': fields.List(fields.Nested(author), description='List of authors'),
}


@ api.route('')
class AuthorsHandler(Resource):
    '''handle authors'''

    # Add a security to check that parameters are integers

    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.marshal_with(author_list)
    def get(self):
        return {'datas': Author.query.all()}

    @ api.doc(body=author)
    @ api.doc(responses={201: 'Created'})
    @ api.doc(responses={400: 'Bad Request'})
    @ api.doc(responses={403: 'Not Authorized'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.expect(author, validate=True)
    def post(self):
        body = api.payload
        del body["id"]
        body["boardgame_id"] = str(uuid.uuid4())

        db.session.add(Author(**body))
        db.session.commit()
        db.session.close()

        return {"id": body["boardgame_id"]}, 201


@ api.route('/<id>')
class AuthorHandler(Resource):

    '''handle single author'''

    @ api.doc(params={'id': 'Technical boardgame id'})
    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.marshal_with(author)
    def get(self, id):
        if not is_uuid4(id):
            return api.abort(404)

        return Author.query.filter_by(author_id=id).first_or_404()

        # using if using id primarykey
        # return Boardgame.query.get_or_404(id)

    @ api.doc(params={'id': 'Technical boardgame id'})
    @ api.doc(responses={204: 'Deleted'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    def delete(self, id):
        if not is_uuid4(id):
            return api.abort(404)

        author_to_delete = Author.query.filter_by(
            author_id=id).first_or_404()

        db.session.delete(author_to_delete)
        db.session.commit()
        db.session.close()
        return Response(status=204)

    @ api.doc(params={'id': 'Technical boardgame id'})
    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={400: 'Bad Request'})
    @ api.doc(responses={403: 'Not Authorized'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.expect(author, validate=True)
    def put(self, id):

        if not is_uuid4(id):
            return api.abort(404)

        Author.query.filter_by(boardgame_id=id).first_or_404()

        body = api.payload
        del body["id"]

        Author.query.filter_by(boardgame_id=id).update({**body})
        db.session.commit()
        db.session.close()

        return Response(status=200)

    @ api.doc(params={'id': 'Technical boardgame id'})
    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={400: 'Bad Request'})
    @ api.doc(responses={403: 'Not Authorized'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.expect(author, validate=False)
    def patch(self, id):
        body = api.payload

        Author.query.filter_by(
            boardgame_id=id).first_or_404()

        del body["id"]
        body = api.payload

        Author.query.filter_by(boardgame_id=id).update({**body})
        db.session.commit()
        db.session.close()

        return Response(status=200)


# custom validation to improve
def is_uuid4(uuid_string, version=4):
    try:
        uid = uuid.UUID(uuid_string, version=version)
        return uid.hex == uuid_string.replace('-', '')
    except ValueError:
        return False
