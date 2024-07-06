from app.extensions import db
from datetime import datetime
from app.requests.models import Request

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    user = db.relationship("User", backref="feedbacks")
    request = db.relationship("Request", backref="feedbacks")
    specialist_id = db.Column(db.Integer, db.ForeignKey('specialist.id'))
    specialist = db.relationship("Specialist", backref="feedbacks")
    question_1 = db.Column(db.Text)
    question_2 = db.Column(db.Text)
    question_3 = db.Column(db.Text)
    question_4 = db.Column(db.Text)
    question_5 = db.Column(db.Text)
    question_6 = db.Column(db.Text)
    question_7 = db.Column(db.Text)
    question_8 = db.Column(db.Text)
    question_9 = db.Column(db.Text)
    question_10 = db.Column(db.Text)



    def __repr__(self):
        return f'{self.message}'
    
    @classmethod
    def get(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def add(cls, user_id, request_id, specialist_id, question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10):
        feedback = cls(
            user_id = user_id,
            request_id = request_id,
            specialist_id = specialist_id,
            question_1 = question_1,
            question_2 = question_2,
            question_3 = question_3,
            question_4 = question_4,
            question_5 = question_5,
            question_6 = question_6,
            question_7 = question_7,
            question_8 = question_8,
            question_9 = question_9,
            question_10 = question_10
        )
        db.session.add(feedback)
        db.session.commit()
        return feedback
    
    @classmethod
    def delete(cls, id):
        feedback = cls.query.get(id)
        db.session.delete(feedback)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_by_request(cls, request_id):
        return cls.query.filter_by(request_id=request_id).all()


    @classmethod
    def add_from_request(cls, request: Request, questions: list):
        return cls.add(
            request_id = request.id,
            user_id = request.user_id,
            specialist_id = request.specialist_id,
            question_1 = questions[0],
            question_2 = questions[1],
            question_3 = questions[2],
            question_4 = questions[3],
            question_5 = questions[4],
            question_6 = questions[5],
            question_7 = questions[6],
            question_8 = questions[7],
            question_9 = questions[8],
            question_10 = questions[9]
        )
    
    
    
