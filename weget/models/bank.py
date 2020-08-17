from weget.extensions import db


class Bank(db.Model):
    """Bank model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __rep__(self):
        return "<Bank %s>" % self.name
