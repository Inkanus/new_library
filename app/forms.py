from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, TextAreaField
from wtforms.validators import DataRequired

class EditBook(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    authors = FieldList(
        StringField('author'), validators=[DataRequired()], min_entries=3)
    genres = FieldList(StringField("genre"), min_entries=3)
    description = TextAreaField('description')
    year = IntegerField(
        'year',validators=[DataRequired(message="Invalid number")])
    pages = IntegerField(
        'pages', validators=[DataRequired(message="Invalid number")])

    def load_data(self, book):
        if book is None:
            return EditBook()
        self.title.data = book["title"]
        for author in book["authors"]:
            self.authors.pop_entry()
        for author in book["authors"]:
            self.authors.append_entry(author)
        self.authors = self.authors[::-1]
        self.year.data = str(book["year"])
        for genre in book["genres"]:
            self.genres.pop_entry()
        for genre in book["genres"]:
            self.genres.append_entry(genre)
        # self.genres = self.genres[::-1]
        self.pages.data = str(book["pages"])
        self.description.data = book["description"]
        return self

