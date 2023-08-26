from peewee import *
from yachalk import chalk
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
    print(chalk.yellow('Welcome to Notes'))
    print(chalk.yellow('1. View notes'))
    print(chalk.yellow('2. View labels'))
    print(chalk.yellow('\'q\' or \'quit\' to exit\n'))


def print_notes_menu():
    print(chalk.yellow('1. View note details'))
    print(chalk.yellow('2. Delete note'))
    print(chalk.yellow('\'m\' or \'main\' to return to main menu\n'))


print_main_menu()

while True:
    user_input = input('Enter choice: ')

    # QUIT
    if user_input == 'q' or user_input == 'quit':
        break

    # VIEW NOTES
    elif user_input == '1':
        notes = Note.select()
        print(chalk.cyan('\nAll Notes'))
        print('---------')

        for note in notes:
            print(chalk.green(f'{note.id}. {note.title}'))

        print()

        while True:
            print_notes_menu()
            user_input = input('Enter choice: ')

            # RETURN TO MAIN MENU
            if user_input == 'm' or user_input == 'main':
                print_main_menu()
                break

            # VIEW NOTE DETAILS
            elif user_input == '1':
                user_input = input('Enter note id: ')

                try:
                    note = Note.get_by_id(user_input)

                    print(chalk.cyan(f'\n{note.title}'))
                    print('-' * len(note.title))
                    print(chalk.green(note.content))
                    print(chalk.cyan(f'\nCreated: {note.date_created}\n'))

                except DoesNotExist:
                    print(f'\nNote with id {user_input} not found.\n')

            # DELETE NOTE
            elif user_input == '2':
                user_input = input('Enter note id: ')

                try:
                    Note.get_by_id(user_input)
                    Note.delete_by_id(user_input)
                    print(f'\nNote with id {user_input} deleted.\n')

                except DoesNotExist:
                    print(f'\nNote with id {user_input} does not exist.')

                # try, except block uses get_by_id() to determine whether note with
                # given ID exists, and to print message to the console if it doesn't.
                # delete_by_id() will actually still work (i.e. not throw an error)
                # if a note with that ID doesn't exist.

    # VIEW LABELS
    elif user_input == '2':
        labels = Label.select()
        print('\nLabels')
        print('------')

        for label in labels:
            print(label.name)

        print()

    else:
        print('Invalid input')
