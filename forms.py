
from flask_wtf import Form
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired

csrf = CSRFProtect()

class JournalEntryForm(Form):
    title = StringField("Title", validators=[DataRequired()])
    date = DateField("Date (DD/MM/YYYY)",
                     format='%d/%m/%Y',
                     validators=[DataRequired()])
    timespent = IntegerField("Time Spent")
    content = TextAreaField("What I Learned", validators=[DataRequired()])
    resources = TextAreaField("Resources to Remember")
