from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SearchField, SelectField, BooleanField, HiddenField, SelectMultipleField
from wtforms.validators import InputRequired, URL


class NewSpecialistForm(FlaskForm):
    name_input = StringField("Ім'я", id='name_input', validators=[InputRequired()])
    id_input = StringField("Manychat ID", id='id_input', validators=[InputRequired()])
    description_input = TextAreaField("Опис", id='description_input', validators=[InputRequired()])
    image_input = StringField("URL зображення", id='image_input', validators=[InputRequired(), URL()])
    cv_input = StringField("URL резюме", id='cv_input', validators=[InputRequired(), URL()])
    tags_select = SelectMultipleField("Теги", id='tags_select', choices=[], validators=[InputRequired()])
    submit = SubmitField("Створити спеціаліста")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.tags.models import Tag
        self.tags_select.choices = [
            (tag.id, tag.name) for tag in Tag.query.all()
        ]
