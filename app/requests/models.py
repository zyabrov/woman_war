from app.extensions import db
from datetime import datetime


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, nullable=False)
    
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False)
    tag = db.relationship("Tag", backref="requests")
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="requests")
    
    specialist_id = db.Column(db.Integer, db.ForeignKey("specialist.id"), nullable=True)
    specialist = db.relationship("Specialist", backref="requests")

    server_url = 'http://127.0.0.1:5000'


    def __repr__(self):
        return f"<Request {self.id}>"
    

    @classmethod
    def add(cls, id, user_id, tag_id):
        new_request = cls(
            id = id,
            created_date = datetime.now(),
            user_id = user_id,
            tag_id = tag_id,
        )
        db.session.add(new_request)
        db.session.commit()
        return new_request
    

    def add_specialist(self, specialist):
        self.specialist = specialist
        db.session.commit()
        
