from db import db

class VisitorModel(db.Model):
    __tablename__ = 'visitors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone = db.Column(db.String(80))

    def __init__(self, name, first_name, last_name, email, phone):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def json(self):
        return {'name': self.name,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'phone': self.phone
                }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
