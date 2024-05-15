from app.extensions import db
from app.tags.models import Tag
from app.specialists.forms import NewSpecialistForm
from app.requests.models import Request


specialist_tag = db.Table(
    "specialist_tag",
    db.Column("specialist_id", db.Integer, db.ForeignKey("specialist.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
)


class Specialist(db.Model):
    __tablename__ = "specialist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))
    cv = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    tags = db.relationship("Tag", secondary=specialist_tag, back_populates="specialists")
    telegram_username = db.Column(db.String(255))


    def __repr__(self) -> str:
        return f"{self.name}"

    @classmethod
    def find_by_tag(cls, tag):
        return cls.query.filter(Specialist.tags.any(id=tag.id)).all()
    

    @classmethod
    def get_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()
    

    @classmethod
    def add(cls, form: NewSpecialistForm):
        new_specialist = cls(
            name = form.name_input.data,
            description = form.description_input.data,
            cv = form.cv_input.data,
            id = form.id_input.data,
            tags = [Tag.get_by_name(tag_name) for tag_name in form.tags_select.data]
        )
        db.session.add(new_specialist)
        db.session.commit()
        return new_specialist
    

    def edit(self, form: NewSpecialistForm):
        self.name = form.name_input.data
        self.description = form.description_input.data
        self.cv = form.cv_input.data
        self.id = form.id_input.data
        self.tags = [Tag.get_by_name(tag_name) for tag_name in form.tags_select.data]
        db.session.commit()


    def delete(self):
        db.session.delete(self)
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
    def find_by_telegram_username(cls, username):
        return cls.query.filter_by(telegram_username=username).first()
    

