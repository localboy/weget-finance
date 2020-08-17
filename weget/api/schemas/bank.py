from weget.models import Bank
from weget.extensions import ma, db


class BankSchema(ma.SQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)

    class Meta:
        model = Bank
        sqla_session = db.session
        load_instance = True