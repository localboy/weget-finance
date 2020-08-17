from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from weget.api.schemas import BankSchema
from weget.models import Bank
from weget.extensions import db
from weget.commons.pagination import paginate


class BankResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: bank_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  bank: BankSchema
        404:
          description: bank does not exists
    put:
      tags:
        - api
      parameters:
        - in: path
          name: bank_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              BankSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: bank updated
                  bank: BankSchema
        404:
          description: bank does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: bank_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: bank deleted
        404:
          description: bank does not exists
    """

    method_decorators = [jwt_required]
    def get(self, bank_id):
        schema = BankSchema()
        bank = Bank.query.get_or_404(bank_id)
        return {"bank": schema.dump(bank)}

    def put(self, bank_id):
        schema = BankSchema(partial=True)
        bank = Bank.query.get_or_404(bank_id)
        bank = schema.load(request.json, instance=bank)

        db.session.commit()

        return {"msg": "bank updated", "bank": schema.dump(bank)}

    def delete(self, bank_id):
        bank = Bank.query.get_or_404(bank_id)
        db.session.delete(bank)
        db.session.commit()

        return {"msg": "bank deleted"}


class BankList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/BankSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              BankSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: bank created
                  bank: BankSchema
    """
    method_decorators = [jwt_required]

    def get(self):
        schema = BankSchema(many=True)
        query = Bank.query
        return paginate(query, schema)

    def post(self):
        schema = BankSchema()
        bank = schema.load(request.json)

        db.session.add(bank)
        db.session.commit()

        return {"msg": "bank created", "bank": schema.dump(bank)}, 201
