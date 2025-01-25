from app.extensions import db
from app.manychat.models import ManychatRequest
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=False)
    telegram_id = db.Column(db.Integer, unique=True)
    birthdate = db.Column(db.Date)
    where_is = db.Column(db.String(80))
    where_is_city = db.Column(db.String(80))
    worked_with_psychologist_before = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    how_known = db.Column(db.String(80))
    age = db.Column(db.Integer)
    pcychiatry = db.Column(db.String(80))

    specialists = db.relationship("Specialist", secondary="specialist_user", back_populates="users")

    def __init__(self, id=None, name=None, username=None, telegram_id=None, birthdate=None, where_is=None, where_is_city=None, worked_with_psychologist_before=None, phone=None, how_known=None, age=None, pcychiatry=None):
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
        self.pcychiatry = pcychiatry


    def __repr__(self):
        return '%r' % self.name
    
    @classmethod
    def add_user(cls, id, name, username, telegram_id, age, phone, where_is=None, where_is_city=None, worked_with_psychologist_before=None, how_known=None, pcychiatry=None):
        user = cls(
            id=id,
            name=name,
            username=username,
            telegram_id=telegram_id,
            age=age,
            phone=phone,
            where_is=where_is,
            where_is_city=where_is_city,
            worked_with_psychologist_before=worked_with_psychologist_before,
            how_known=how_known,
            pcychiatry=pcychiatry
        )
        db.session.add(user)
        db.session.commit()
        return user
    

    def update_user(self, name=None, username=None, age=None, where_is=None, where_is_city=None, worked_with_psychologist_before=None, phone=None, how_known=None, pcychiatry=None):
        if name:
            self.name = name
        if username:
            self.username = username
        if age:
            self.age = age

        if where_is:
            self.where_is = where_is
        if where_is_city:
            self.where_is_city = where_is_city
        if worked_with_psychologist_before:
            self.worked_with_psychologist_before = worked_with_psychologist_before
        if phone:
            self.phone = phone
        if pcychiatry:
            self.pcychiatry = pcychiatry
        db.session.commit()

    @classmethod
    def get(cls, id):
        return cls.query.get(id)


    @classmethod 
    def get_and_update_or_create_from_request(cls, request:ManychatRequest) -> "User":
        user = cls.get(request.user_id)
        if not user:
            user = cls.add_user(
                id=request.user_id,
                name=request.full_name,
                username=request.username,
                telegram_id=request.telegram_id,
                age=request.user_age,
                phone=request.phone
            )
            print('/n/n----------------/n')
            print('new user added: ', user)
        else:
            print('/n/n----------------/n')
            print('user exists')
            user.update_user(
                name=request.full_name,
                username=request.username,
                age=request.user_age,
                phone=request.phone
                )
            print('user: ', user)
        return user
    

def age_calc(birthdate:datetime):
    age = datetime.now().year - birthdate.year - ((datetime.now().month, datetime.now().day) < (birthdate.month, birthdate.day))
    print('/n/n----------------/n')
    print('age: ', age)
    return age
        