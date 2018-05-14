# Import Form and RecaptchaField (optional)

from flask_wtf import Form # , RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
# Import Form elements such as TextField and BooleanField (optional)
from wtforms import StringField, PasswordField, RadioField, SelectField, TextAreaField, SubmitField, HiddenField, validators # BooleanField
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField
# Import Form validators
from wtforms.validators import Email, EqualTo, required, optional, length, ValidationError, DataRequired
from app.mod_auth.models import User


class SearchForm(Form):
    search = StringField('search', [DataRequired()],render_kw={'class': 'form-control'})
    submit = SubmitField('Search', render_kw={'class': 'btn btn-success btn-block'})


class LoginForm(Form):
    email    = StringField('Email Address', [Email(),
                required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                required(message='Must provide a password. ;-)')])
    submit = SubmitField('Logg inn')


class NewEventForm(Form):
    id = HiddenField('id',)
    deleted = HiddenField('deleted',)
    name = StringField('Arrangement Tittel', [required(message='Skriv arrangement navn')])
    event_type = RadioField('Arrangement Type', choices=[('public', 'PUBLIC'), ('private', 'PRIVATE'),
                                                         ('community', 'COMMUNITY'), ('group', 'GROUP')], default='public')

    categoryList = [('Familie', 'Familie/Barn'),
                    ('Friluftsliv', 'Friluftsliv'),
                     ('Underholdning', 'Underholdning'),
                     ('Kultur', 'Kultur'),
                     ('Festival', 'Festival/merknad'),
                     ('Sport', 'Sport/idrett'),
                     ('Kjøretøy', 'Kjøretøy'),
                     ('Dyr', 'Dyr/jordbruk'),
                     ('Handel', 'Handel'),
                     ('Mat/drikke', 'Mat & drikke'),
                     ('Reise', 'Reise'),
                     ('Helse', 'Helse, kropp og sinn'),
                     ('Religion', 'Religion'),
                     ('Solsial', 'Solsiale treff'),
                     ('Hus', 'Hus - hage')]

    category = SelectField(label='Kategori', choices=categoryList, default=['1'])
    description = TextAreaField('Beskrivelse', [optional(), length(max=500)])
    startDate = DateField('Start Dato', [DataRequired()])
    startTime = TimeField('Start Tidspunkt', [DataRequired()])
    endDate = DateField('Slutt Dato', [DataRequired()])
    endTime = TimeField('Slutt Tidspunkt', [DataRequired()])

    location_name = StringField('Lokasjon navn')
    country = SelectField('Land', choices=[('norge', 'Norge'), ])
    city = StringField('By', [required(message='Please add city')])
    zip = StringField('Postnummer', [required(message='Please add zip')])
    street = StringField('Gate', [required(message='Please add street')])
    image = FileField('Bilde', validators=[ FileAllowed(["txt", "pdf", "png", "jpg", "jpeg", "gif"], 'Images only!')])
    submit = SubmitField('Legg til')


class Registration(Form):
    name = StringField('Name', [required(message='Must provide name')])
    phone = StringField('Phone')
    email = StringField('Email Address', [Email(),
                required(message='Forgot your email address?')])
    password = PasswordField('Password', [
                required(message='Must provide a password. ;-)')])
    company = StringField('Company Name')
    role = RadioField('Role', choices=[('Administrator', 'ADMIN'), ('Company', 'COMPANY'),
                                                         ('user', 'USER'), ('prime user', 'PRIME USER')])
    submit = SubmitField('Registrer Bruker')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email er allerede i bruk")
