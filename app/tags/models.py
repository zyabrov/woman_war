from app.extensions import db

class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    specialists = db.relationship("Specialist", secondary="specialist_tag", back_populates="tags")
    
    @classmethod
    def get_by_name(cls, name):
        print('tag name', name)
        print('tag name', name.split(" - ")[1])
        return cls.query.filter_by(name=name.split(" - ")[1]).first()