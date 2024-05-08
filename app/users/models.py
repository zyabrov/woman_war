from app.extensions import db
from app.manychat.models import ManychatRequest
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True)
    telegram_id = db.Column(db.Integer, unique=True)
    birthdate = db.Column(db.Date, nullable=False)
    where_is = db.Column(db.String(80), nullable=False)
    where_is_city = db.Column(db.String(80), nullable=False)
    worked_with_psychologist_before = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    how_known = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer)

    def __init__(self, id=None, name=None, username=None, telegram_id=None, birthdate=None, where_is=None, where_is_city=None, worked_with_psychologist_before=None, phone=None, how_known=None, age=None):
        self.id = id
        self.name = name
        self.username = username
        self.telegram_id = telegram_id
        self.birthdate = birthdate
        self.where_is = where_is
        self.where_is_city = where_is_city
        self.worked_with_psychologist_before = worked_with_psychologist_before
        self.phone = phone
        self.how_known = how_known
        self.age = age


    def __repr__(self):
        return '<%r>' % self.name
    
    @classmethod
    def add_user(cls, id, name, username, telegram_id, birthdate:str, where_is, where_is_city, worked_with_psychologist_before, phone, how_known):
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        age = age_calc(birthdate)
        user = cls(id, name, username, telegram_id, birthdate, where_is, where_is_city, worked_with_psychologist_before, phone, how_known, age)
        db.session.add(user)
        db.session.commit()
        return user
    

    def update_user(self, name=None, username=None, where_is=None, where_is_city=None, worked_with_psychologist_before=None, phone=None):
        if name:
            self.name = name
        if username:
            self.username = username

        if where_is:
            self.where_is = where_is
        if where_is_city:
            self.where_is_city = where_is_city
        if worked_with_psychologist_before:
            self.worked_with_psychologist_before = worked_with_psychologist_before
        if phone:
            self.phone = phone
        self.age = datetime.now().year - self.birthdate.year
        db.session.commit()

    @classmethod
    def get(cls, id):
        return cls.query.get(id)


    @classmethod 
    def get_and_update_or_create_from_request(cls, request:ManychatRequest):
        user = cls.get(request.user_id)
        if not user:
            user = cls.add_user(
                request.user_id,
                request.full_name,
                request.username,
                request.telegram_id,
                request.birthdate,
                request.where_is,
                request.where_is_city,
                request.worked_with_psychologist_before,
                request.phone,
                request.how_known
            )
        else:
            user.update_user(
                name=request.full_name,
                username=request.username,
                where_is=request.where_is,
                where_is_city = request.where_is_city,
                worked_with_psychologist_before=request.worked_with_psychologist_before,
                phone=request.phone)
        return user
    

def age_calc(birthdate:datetime):
    age = datetime.now().year - birthdate.year - ((datetime.now().month, datetime.now().day) < (birthdate.month, birthdate.day))
    print('/n/n----------------/n')
    print('age: ', age)
    return age
        