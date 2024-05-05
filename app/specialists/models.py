from app.extensions import db
from app.tags.models import Tag


specialist_tag = db.Table(
    "specialist_tag",
    db.Column("specialist_id", db.Integer, db.ForeignKey("specialist.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
)


class Specialist(db.Model):
    __tablename__ = "specialist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    image = db.Column(db.String(255))
    description = db.Column(db.String(255))
    cv = db.Column(db.String(255))
    tags = db.relationship("Tag", secondary=specialist_tag, back_populates="specialists")


    @classmethod
    def find_by_tag(cls, tag):
        return cls.query.filter(Specialist.tags.any(id=tag.id)).all()
