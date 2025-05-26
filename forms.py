from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Regexp
from datetime import datetime
from models import get_categories_choice

class SerchForm(FlaskForm):
    YEAR_CHOICE = [('', 'Выберите год')] + [(str(year), str(year)) for year in range(1900, datetime.now().year + 1)][::-1]
    CATEGORY_CHOICE = [('', 'Выберите категорию')] + get_categories_choice()

    film = StringField('Фильм', validators=[
        Optional(),
        Regexp(r'^[A-Za-z0-9\s]+$', message="Только латинские буквы и цифры")
    ])
    actor = StringField('Актер', validators=[
        Optional(),
        Regexp(r'^[A-Za-z\s]+$', message="Только латинские буквы и пробелы")
    ])
    category = SelectField('Категория', choices=CATEGORY_CHOICE, validators=[Optional()])
    year = SelectField('Год', choices=YEAR_CHOICE, validators=[Optional()])
    submit = SubmitField('Поиск')
