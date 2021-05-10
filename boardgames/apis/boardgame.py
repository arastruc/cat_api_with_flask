import uuid
from dao.models import Boardgame
from flask_restplus import Namespace, Resource, fields
from flask import Response
import uuid

from dao.db import db


api = Namespace('boardgames', description='Boardgames related operations')

boardgame = api.model(
    'Boardgame',
    {'id': fields.String(description='The id', attribute="boardgame_id"),
     'name': fields.String(description='The name', required=True),
     'publisher': fields.String(description='The color', required=True),
     'minplayer': fields.Integer(description='The minimum required number of player'),
     'maxplayer': fields.Integer(description='The maximum number of player'),
     'duration': fields.Integer(description='The duration of the game (in min)'),
     'author': fields.String(description='The author of the game', required=True),
     })

boardgame_list = {
    'boardgames': fields.List(fields.Nested(boardgame), description='List of boardgames'),
}


@ api.route('')
class BoardgamesHandler(Resource):
    '''handle cats'''

    # Add a security to check that parameters are integers

    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.marshal_with(boardgame_list)
    def get(self):
        return {'boardgames': Boardgame.query.all()}

    @ api.doc(body=boardgame)
    @ api.doc(responses={201: 'Created'})
    @ api.doc(responses={400: 'Bad Request'})
    @ api.doc(responses={403: 'Not Authorized'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.expect(boardgame, validate=True)
    def post(self):
        body = api.payload
        print(body)
        del body["id"]
        body["boardgame_id"] = str(uuid.uuid4())

        db.session.add(Boardgame(**body))
        db.session.commit()
        db.session.close()

        return {"id": body["boardgame_id"]}, 201


@ api.route('/<id>')
class BoardgameHandler(Resource):

    '''handle single cat'''

    @ api.doc(params={'id': 'Technical boardgame id'})
    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.marshal_with(boardgame)
    def get(self, id):
        if not is_uuid4(id):
            return api.abort(404)

        return Boardgame.query.filter_by(boardgame_id=id).first_or_404()

        # using if using id primarykey
        # return Boardgame.query.get_or_404(id)

    @ api.doc(params={'id': 'Technical boardgame id'})
    @ api.doc(responses={204: 'Deleted'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    def delete(self, id):
        if not is_uuid4(id):
            return api.abort(404)

        boardgame_to_delete = Boardgame.query.filter_by(
            boardgame_id=id).first_or_404()

        db.session.delete(boardgame_to_delete)
        db.session.commit()
        db.session.close()
        return Response(status=204)

    @ api.doc(params={'id': 'Technical boardgame id'})
    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={400: 'Bad Request'})
    @ api.doc(responses={403: 'Not Authorized'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.expect(boardgame, validate=True)
    def put(self, id):

        if not is_uuid4(id):
            return api.abort(404)

        Boardgame.query.filter_by(boardgame_id=id).first_or_404()

        body = api.payload
        del body["id"]

        Boardgame.query.filter_by(boardgame_id=id).update({**body})
        db.session.commit()
        db.session.close()

        return Response(status=200)

    @ api.doc(params={'id': 'Technical boardgame id'})
    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={400: 'Bad Request'})
    @ api.doc(responses={403: 'Not Authorized'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.expect(boardgame, validate=False)
    def patch(self, id):
        body = api.payload

        Boardgame.query.filter_by(
            boardgame_id=id).first_or_404()

        del body["id"]
        body = api.payload

        Boardgame.query.filter_by(boardgame_id=id).update({**body})
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
