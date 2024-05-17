from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SearchField, SelectField, BooleanField, HiddenField, SelectMultipleField, IntegerField, FieldList
from wtforms.validators import InputRequired, URL, DataRequired


class NewSpecialistForm(FlaskForm):
    name_input = StringField("Ім'я", id='name_input', validators=[InputRequired()])
    manychat_username_input = StringField("ManyChat username", id='manychat_username_input', validators=[])
    description_input = TextAreaField("Опис", id='description_input', validators=[InputRequired()])
    image_input = StringField("URL зображення", id='image_input', validators=[])
    cv_input = StringField("URL резюме", id='cv_input', validators=[])
    tags_select = SelectMultipleField("Теги", id='tags_select', choices=[], validators=[DataRequired()])
    # , render_kw={
    #     'hx-trigger': "change", 
    #     'hx-post': "/specialists/form/update_selected_tags",
    #     'hx-target': "#tags_selected_list",
    #     })
    cost_input = IntegerField("Вартість години консультації", id='cost_input', validators=[InputRequired()])
    submit = SubmitField("Створити спеціаліста")

    # tags_selected_list = FieldList(tags_select, id='tags_selected_list')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.tags.models import Tag
        self.tags_select.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
