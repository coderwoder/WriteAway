from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired(),Length(min=5,max=200)])
    content=TextAreaField('Content',validators=[DataRequired()])
    submit=SubmitField('Create!')

