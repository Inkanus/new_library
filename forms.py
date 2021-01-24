from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
    IntegerField, FieldList, TextAreaField
from wtforms.validators import DataRequired


class EditBook(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    author = StringField('author', validators=[DataRequired()])
    genres = FieldList(StringField("genre"), min_entries=1)
    description = TextAreaField('description')
    year = IntegerField(
        'year', validators=[DataRequired(message="Invalid number")])
    pages = IntegerField(
        'pages', validators=[DataRequired(message="Invalid number")])

    def load_data(self, book):
        self.title.data = book.title
        self.author.data = book.author
        self.year.data = str(book.year) if book.year else ""
        self.genres.pop_entry()
        for genre in book.genres:
            self.genres.append_entry(genre)
        self.pages.data = str(book.pages) if book.pages else ""
        self.description.data = book.description
