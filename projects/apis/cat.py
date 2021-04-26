from flask_restplus import Namespace, Resource, fields
from flask import Response


from dao.models import Cat
import uuid


class NoResultFound(Exception):
    pass


api = Namespace('cats', description='Cats related operations')

cat = api.model(
    'Cat',
    {'name': fields.String(description='The name', required=True),
     'color': fields.String(description='The color', required=True),
     'id': fields.String(description='The color', required=True),
     'sex': fields.String(enum=["Male", "Female", "Other"]),
     'foods': fields.List(
        fields.String(description='Favourite foods')
    ), })


cat_list = {
    'cats': fields.List(fields.Nested(cat))
}


@ api.errorhandler(NoResultFound)
def handle_no_result_exception(error):
    '''Return a custom not found error message and 404 status code'''
    return {'message': 'Not Found'}, 404


@ api.route('/')
class CatsHandler(Resource):
    '''handle cats'''

    @ api.doc(params={'limit': {'description': 'limit', 'in': 'query', 'type': 'int'}})
    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.marshal_with(cat_list)
    def get(self):
        cats = Cat.objects.all()
        return {'cats': cats}, 200

    @ api.doc(body=cat)
    @ api.doc(responses={201: 'Created'})
    @ api.doc(responses={403: 'Not Authorized'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.expect(cat, validate=True)
    def post(self):
        body = api.payload
        body["id"] = str(uuid.uuid4())
        cat = Cat(**body).save()
        return {'id': cat.id}, 201

    @ api.doc(responses={201: 'Created'})
    @ api.doc(responses={403: 'Not Authorized'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.expect(cat, validate=True)
    def put(self):
        body = api.payload

        try:
            Cat.objects.get(id=body['id']).update(**body)

        except Cat.DoesNotExist:
            raise NoResultFound

        return Response(status=200)


@ api.route('/<id>')
class CatHandler(Resource):

    '''handle single cat'''

    @ api.doc(params={'id': 'cat_id'})
    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.marshal_with(cat, code=200)
    def get(self, id):
        try:
            return Cat.objects.get(id=id)
        except Cat.DoesNotExist:
            raise NoResultFound

    @ api.doc(responses={204: 'Deleted'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    def delete(self, id):
        try:
            Cat.objects.get(id=id).delete()
            return Response(status=204)

        except Cat.DoesNotExist:
            raise NoResultFound
