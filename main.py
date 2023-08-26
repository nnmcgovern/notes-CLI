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

label1 = Label(name='Personal')
label1.save()
label2 = Label(name='Work')
label2.save()

# APPLICATION


def print_main_menu():
    print('Welcome to Notes')
    print('1. View notes')
    print('2. View labels')


def print_notes_menu():
    print('1. View note details')
    print('2. Create new note')
    print('3. Delete note')


print_main_menu()

while True:
    user_input = input('Enter choice: ')

    if user_input == 'q' or user_input == 'quit':
        break

    # NOTES
    elif user_input == '1':
        notes = Note.select()
        print('\nAll Notes')
        print('---------')

        for note in notes:
            print(f'{note.id}. {note.title}')

        print()
        print_notes_menu()

        user_input = input('Enter choice: ')

        # VIEW NOTE DETAILS
        if user_input == '1':
            user_input = input('Enter note id: ')
            note = Note.get_by_id(user_input)

            print(f'\n{note.title}')
            print('-' * len(note.title))
            print(note.content)
            print(f'\nCreated: {note.date_created}\n')

    # LABELS
    elif user_input == '2':
        labels = Label.select()
        print('\nLabels')
        print('------')

        for label in labels:
            print(label.name)

        print()

    else:
        print('Invalid input')
