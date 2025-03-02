from app.extensions import db
from app.tags.models import Tag
from app.specialists.forms import NewSpecialistForm, EditSpecialistForm
from app.requests.models import Request


specialist_tag = db.Table(
    "specialist_tag",
    db.Column("specialist_id", db.Integer, db.ForeignKey("specialist.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
)

specialist_user = db.Table(
    "specialist_user",
    db.Column("specialist_id", db.Integer, db.ForeignKey("specialist.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
)


class Specialist(db.Model):
    __tablename__ = "specialist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))
    cv = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    tags = db.relationship("Tag", secondary='specialist_tag', back_populates="specialists")
    telegram_username = db.Column(db.String(255))
    manychat_username = db.Column(db.String(255))
    cost = db.Column(db.Integer)
    manychat_img = db.Column(db.String(255))
    users = db.relationship("User", secondary='specialist_user', back_populates="specialists")


    def __repr__(self) -> str:
        return f"{self.name}"
    
    @classmethod
    def get(cls, id) -> "Specialist":
        return cls.query.get(id)

    @classmethod
    def find_by_tag(cls, tag):
        return cls.query.filter(Specialist.tags.any(id=tag.id)).all()
    

    @classmethod
    def get_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()
    
    @classmethod
    def add_free(cls, manychat_id, manychat_username, telegram_username=None) -> "Specialist":
        specialist = cls(
            id = manychat_id,
            manychat_username = manychat_username,
            telegram_username = telegram_username,
            name = manychat_username
        )
        db.session.add(specialist)
        db.session.commit()
        return specialist
    

    @classmethod
    def add(cls, name, manychat_id, telegram_username, manychat_username, phone=None, description=None, cv=None, tags=None, cost=None, manychat_img=None) -> "Specialist":
        if tags and isinstance(tags, list):
            tags = [Tag.get(tag_id) for tag_id in tags]
        else:
            tags = []
        new_specialist = cls(
            id = manychat_id,
            name = name,
            description = description,
            cv = cv,
            tags = tags,
            cost = cost,
            manychat_username = manychat_username,
            telegram_username = telegram_username,
            phone = phone,
            manychat_img = manychat_img
        )
        db.session.add(new_specialist)
        db.session.commit()
        return new_specialist
    

    def edit(self, form: EditSpecialistForm):
        self.name = form.name_input.data
        self.telegram_username = form.tg_username.data
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, form: EditSpecialistForm):
        self.name = form.name_input.data
        self.telegram_username = form.tg_username.data
        self.description = form.description_input.data
        self.phone = form.phone.data
        db.session.commit()


    @classmethod
    def find_by_request_id(cls, request_id):
        request = Request.get(request_id)
        if request:
            request_tag = request.tag
            if request_tag:
                print('/n/n----------------/n')
                print('find_by_request_id: ', request_tag)
                return cls.query.filter(Specialist.tags.any(id=request_tag.id)).all()
            else:
                print('/n/n----------------/n')
                print('request tag not found')
        else:
            print('/n/n----------------/n')
            print('request not found')
        return []

    
    @classmethod
    def find_by_telegram_username(cls, username) -> 'Specialist':
        return cls.query.filter_by(telegram_username=username).first()
    

