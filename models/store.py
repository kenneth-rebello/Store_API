from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"id": self.id, "name": self.name, "items": [item.json() for item in self.items]}

    @classmethod
    def find_by_name(cls, name):
       return cls.query.filter_by(name=name).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()