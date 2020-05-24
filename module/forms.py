# forms.py

from wtforms import Form, StringField, SelectField, validators

class MusicSearchForm(Form):
   choices = [('Colleges & Universities', 'Colleges & Universities'),
              ('Food', 'Food'),
              ('Events', 'Events')]
   select = SelectField('Search:', choices=choices)
   search = StringField('Search ')
   locationcity = StringField('Location City')
   locationstate = StringField('Location State')
  
