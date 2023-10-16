from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import EmbeddedDocumentField, ListField, StringField, ReferenceField, BooleanField


class Tag(EmbeddedDocument):
    name = StringField()


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField(Author, dbref=False, reverse_delete_rule=2)
    quote = StringField()


class Contact(Document):
    fullname = StringField()
    email = StringField()
    is_sent = BooleanField(default=False)
    phone_number = StringField()
    delivery_method = StringField()    
