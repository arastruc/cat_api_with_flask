import uuid
from dao.models import Boardgame
from flask_restplus import Namespace, Resource, fields
from flask import Response

from dao.db import db


api = Namespace('boardgames', description='Boardgames related operations')

boardgame = api.model(
    'Boardgame',
    {'id': fields.String(description='The technical id'),
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
        del body["id"]
        db.session.add(Boardgame(**body))
        db.session.commit()
        db.session.close()
        return Response(status=201)


@ api.route('/<id>')
class BoardgameHandler(Resource):

    '''handle single cat'''

    @ api.doc(params={'id': 'Technical boardgame id'})
    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.marshal_with(boardgame, code=200)
    def get(self, id):
        return Boardgame.query.get_or_404(id)

    @ api.doc(params={'id': 'Technical boardgame id'})
    @ api.doc(responses={204: 'Deleted'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    def delete(self, id):
        boardgame_to_delete = Boardgame.query.get_or_404(id)
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
        Boardgame.query.get_or_404(id)
        body = api.payload

        Boardgame.query.filter_by(id=id).update({**body})
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

        Boardgame.query.get_or_404(id)
        body = api.payload

        Boardgame.query.filter_by(id=id).update({**body})
        db.session.commit()
        db.session.close()

        return Response(status=200)


# def getFilteredCats(*, search_criteria):

#     criteria_dict = {}

#     for criteria in search_criteria:
#         criteria_value = request.args.get(criteria)
#         if criteria_value:
#             criteria_dict[criteria] = criteria_value

#     return Cat.objects(**criteria_dict) if search_criteria else Cat.objects()
