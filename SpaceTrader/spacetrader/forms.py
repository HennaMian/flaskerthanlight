"""Creates SpaceTrader Form to Setup Game and Implements Form Logic"""
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, InputRequired


def custom_validate(form, difficulty):
    """Creates Form Logic"""
    total_skill_points = form.pilotskillpoints.data + form.fighterskillpoints.data \
                         + form.merchantskillpoints.data + form.engineerskillpoints.data
    if form.difficulty.data == 'Easy':
        if total_skill_points > 16:
            raise ValidationError("For difficulty Easy, skill points must add up to"
                                  " a number between 4 and 16.")
    if form.difficulty.data == 'Medium':
        if total_skill_points > 12:
            raise ValidationError("For difficulty Medium, skill points must add up"
                                  " to a number between 4 and 12.")
    if form.difficulty.data == 'Hard':
        if total_skill_points > 8:
            raise ValidationError("For difficulty Hard, skill points must add up"
                                  " to a number between 4 and 8.")
    result = ""
    result += str(difficulty)

    return True

class PlayerInfo(FlaskForm):
    """Creates Player Class"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=16)])
    difficulty = RadioField('Difficulty', choices=[('Easy', 'Easy'), ('Medium', 'Medium'),
                                                   ('Hard', 'Hard')], validators=[InputRequired()])
    pilotskillpoints = IntegerField('Pilot Skill Points',
                                    validators=[DataRequired(), NumberRange(min=0, max=16),
                                                custom_validate])
    fighterskillpoints = IntegerField('Fighter Skill Points',
                                      validators=[DataRequired(), NumberRange(min=0, max=16),
                                                  custom_validate])
    merchantskillpoints = IntegerField('Merchant Skill Points',
                                       validators=[DataRequired(), NumberRange(min=0, max=16),
                                                   custom_validate])
    engineerskillpoints = IntegerField('Engineer Skill Points',
                                       validators=[DataRequired(), NumberRange(min=0, max=16),
                                                   custom_validate])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Submit')
