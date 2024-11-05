from app.extensions import db
from datetime import datetime
from app.manychat.models import ManychatRequest


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, nullable=False)
    user_full_name = db.Column(db.String(80), nullable=False)
    user_username = db.Column(db.String(80))
    user_telegram_id = db.Column(db.Integer)
    user_birthdate = db.Column(db.Date)
    user_where_is = db.Column(db.String(80))
    user_where_is_city = db.Column(db.String(80))
    user_worked_with_psychologist_before = db.Column(db.String(80))
    help_type = db.Column(db.String(80), nullable=False)
    user_how_known = db.Column(db.String(80))
    user_phone = db.Column(db.Integer)
    request_type = db.Column(db.String(80), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=True)
    tag = db.relationship("Tag", backref="requests")
    user_age = db.Column(db.Integer)
    request_name = db.Column(db.String(80))
    status = db.Column(db.String(80), nullable=False, default="new")
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="requests")
    
    specialist_id = db.Column(db.Integer, db.ForeignKey("specialist.id"), nullable=True)
    specialist = db.relationship("Specialist", backref="requests")

    message_id = db.Column(db.Integer)




    def __repr__(self):
        return f"Запит {self.id}"
    

    @classmethod
    def get(cls, id) -> "Request":
        return cls.query.get(id)


    @classmethod
    def add(cls, manychat_request: ManychatRequest):
        # user_/age = (datetime.now().date() - datetime.strptime(user_birthdate, "%Y-%m-%d").date()).days // 365
        new_request = cls(
            id = manychat_request.id,
            created_date = datetime.now(),
            user_full_name = manychat_request.full_name,
            user_username = manychat_request.username,
            user_telegram_id = manychat_request.telegram_id,
            # user_birthdate = datetime.strptime(user_birthdate, "%Y-%m-%d").date(), #user_birthdate,
            user_where_is = manychat_request.where_is,
            user_where_is_city = manychat_request.where_is_city,
            user_worked_with_psychologist_before = manychat_request.worked_with_psychologist_before,
            help_type = manychat_request.help_type,
            user_how_known = manychat_request.how_known,
            user_phone = manychat_request.phone,
            # tag_id = manychat_request.tag_id,
            user_id = manychat_request.user_id,
            # request_type = manychat_request.request_type,
            user_age = manychat_request.user_age, 
            request_name = manychat_request.tag_name,
            status = "new"
        )
        db.session.add(new_request)
        db.session.commit()
        return new_request


    @classmethod
    def add_from_request(cls, request: ManychatRequest):
        tag_id = None
        from app.tags.models import Tag
        tag = Tag.get_by_name(request.tag_name)
        if tag:
            tag_id = tag.id

        return cls.add(
            id = request.id,
            user_id = request.user_id,
            tag_id = tag_id,
            user_full_name = request.full_name,
            user_username = request.username,
            user_telegram_id = request.telegram_id,
            user_birthdate = request.birthdate,
            user_where_is = request.where_is,
            user_where_is_city = request.where_is_city,
            user_worked_with_psychologist_before = request.worked_with_psychologist_before,
            help_type = request.help_type,
            user_how_known = request.how_known,
            user_phone = request.phone,
            request_type = 'Безкоштовний',
            request_name = request.tag_name
        )

    
    def get_user(self):
        from app.users.models import User
        return User.query.get(self.user_id)
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
    def save_message_id(self, message_id):
        self.message_id = int(message_id)
        db.session.commit()


    def add_specialist(self, specialist_id):
        self.specialist_id = specialist_id
        db.session.commit()

    def save(self):
        db.session.commit()
        
