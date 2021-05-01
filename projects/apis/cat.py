import uuid
from dao.models import Cat
from flask_restplus import Namespace, Resource, fields
from flask import Response, request


api = Namespace('cats', description='Cats related operations')

cat = api.model(
    'Cat',
    {'name': fields.String(description='The name', required=True),
     'color': fields.String(description='The color', required=True),
     'id': fields.String(description='The technical id'),
     'sex': fields.String(enum=["Male", "Female", "Other"]),
     'foods': fields.List(
        fields.String(description='Favourite foods')
    ),
    })


pagination = api.model('Pagination', {'totalItems': fields.Integer(),
                                      'totalPages': fields.Integer(),
                                      'itemsPerPage': fields.Integer(),
                                      'currentPage': fields.Integer(),
                                      }
                       )
cat_list = {
    'cats': fields.List(fields.Nested(cat), description='List of cats'),
    'pagination': fields.Nested(pagination, description="pagination")
}


class NoResultFound(Exception):
    pass


@ api.errorhandler(NoResultFound)
def handle_no_result_exception(error):
    '''Return a custom not found error message and 404 status code'''
    return {'message': 'Not Found'}, 404


@ api.route('/')
class CatsHandler(Resource):
    '''handle cats'''

    # Add a security to check that parameters are integers

    @ api.doc(params={'limit': {'description': 'Number of result per page (default 20)', 'in': 'query', 'type': 'int'}})
    @ api.doc(params={'page': {'description': 'Current Page (default 1)', 'in': 'query', 'type': 'int'}})
    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.marshal_with(cat_list)
    def get(self):

        try:
            limit = request.args.get("limit") or "20"
            page = request.args.get("page") or "1"
            cats = Cat.objects.all().paginate(page=int(page), per_page=int(limit))

            return {'cats': cats.items,
                    'pagination': {'totalItems': cats.total,
                                   'totalPages': cats.pages,
                                   'itemsPerPage': cats.per_page,
                                   'currentPage': cats.page,
                                   }}, 200

        except Cat.DoesNotExist:
            raise NoResultFound

    @ api.doc(body=cat)
    @ api.doc(responses={201: 'Created'})
    @ api.doc(responses={400: 'Bad Request'})
    @ api.doc(responses={403: 'Not Authorized'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.expect(cat, validate=True)
    def post(self):
        body = api.payload
        body["id"] = str(uuid.uuid4())
        cat = Cat(**body).save()
        return {'id': cat.id}, 201


@ api.route('/<id>')
class CatHandler(Resource):

    '''handle single cat'''

    @ api.doc(params={'id': 'Technical cat id'})
    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.marshal_with(cat, code=200)
    def get(self, id):
        try:
            return Cat.objects.get(id=id)
        except Cat.DoesNotExist:
            raise NoResultFound

    @ api.doc(params={'id': 'Technical cat id'})
    @ api.doc(responses={204: 'Deleted'})
    @ api.doc(responses={404: 'Not Found'})
    @ api.doc(responses={500: 'Internal Error'})
    def delete(self, id):
        try:
            Cat.objects.get(id=id).delete()
            return Response(status=204)

        except Cat.DoesNotExist:
            raise NoResultFound

    @ api.doc(params={'id': 'Technical cat id'})
    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={400: 'Bad Request'})
    @ api.doc(responses={403: 'Not Authorized'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.expect(cat, validate=True)
    def put(self, id):
        body = api.payload

        try:
            Cat.objects.get(id=id).update(**body)
            return Response(status=200)

        except Cat.DoesNotExist:
            raise NoResultFound

    @ api.doc(responses={200: 'OK'})
    @ api.doc(responses={400: 'Bad Request'})
    @ api.doc(responses={403: 'Not Authorized'})
    @ api.doc(responses={500: 'Internal Error'})
    @ api.expect(cat, validate=False)
    def patch(self, id):
        body = api.payload

        try:
            Cat.objects.get(id=id).update(**body)
            return Response(status=200)

        except Cat.DoesNotExist:
            raise NoResultFound
