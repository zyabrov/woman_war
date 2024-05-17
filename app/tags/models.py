from app.extensions import db

class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    specialists = db.relationship("Specialist", secondary="specialist_tag", back_populates="tags")
    
    def __repr__(self) -> str:
        return f"{self.name}"
    
    @classmethod
    def get(cls, id) -> 'Tag':
        return cls.query.get(id)
        

    @classmethod
    def get_by_name(cls, name) -> "Tag":
        print('tag name', name)
        tag_name = name
        if " - " in name:
            tag_name = name.split(" - ")[1]
        return cls.query.filter_by(name=tag_name).first()


    @classmethod
    def add(cls, name):
        new_tag = cls(name=name)
        db.session.add(new_tag)
        db.session.commit()
        return new_tag