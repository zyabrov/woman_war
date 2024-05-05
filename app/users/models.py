from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.username
    
    @classmethod
    def add_user(cls, id, name):
        user = cls(id=id, name=name)
        db.session.add(user)
        db.session.commit()
        return user


    @classmethod 
    def get_or_create(cls, id, name):
        user = cls.query.get(id)
        if not user:
            user = cls.add_user(id, name)
        return user
        