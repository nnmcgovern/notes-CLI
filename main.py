from peewee import *
import datetime

# SETUP

db = PostgresqlDatabase('notes', user='notes_admin',
                        password='notescliadminpass', host='localhost', port=5432)

db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Note(BaseModel):
    title = CharField()
    content = CharField()
    date_created = DateTimeField(default=datetime.datetime.now)


class Label(BaseModel):
    name = CharField()


class Labelization(BaseModel):
    note_id = IntegerField()
    label_id = IntegerField()


db.drop_tables([Note, Label, Labelization])
db.create_tables([Note, Label, Labelization])

# TEST

note1 = Note(title='My first note',
             content='this is the content of my first note')
note1.save()

# APPLICATION


def print_notes_menu():
    print('Welcome to Notes')
    print('1. See all notes')


print_notes_menu()

while True:
    user_input = input('Enter input: ')

    if user_input == 'q' or user_input == 'quit':
        break

    elif user_input == '1':
        notes = Note.select()
        print('\nAll Notes')
        print('---------')

        for note in notes:
            print(note.title)

        print()

    else:
        print('Invalid input')
