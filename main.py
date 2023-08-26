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
    note_id = ForeignKeyField(Note, backref='note', on_delete='CASCADE')
    label_id = ForeignKeyField(Label, backref='label', on_delete='CASCADE')


db.drop_tables([Note, Label, Labelization])
db.create_tables([Note, Label, Labelization])

# TEST

note1 = Note(title='My first note',
             content='this is the content of my first note')
note1.save()
note2 = Note(title='Some notes for work',
             content='here is some random text for my note')
note2.save()
note3 = Note(title='Another personal note', content='testing testing 1 2 3')
note3.save()

label1 = Label(name='Personal')
label1.save()
label2 = Label(name='Work')
label2.save()

labelize1 = Labelization(note_id=1, label_id=1)
labelize1.save()
labelize2 = Labelization(note_id=2, label_id=2)
labelize2.save()
labelize3 = Labelization(note_id=3, label_id=1)
labelize3.save()

# APPLICATION


def print_main_menu():
    print(chalk.yellow('\nWelcome to Notes'))
    print(chalk.yellow('1. View notes'))
    print(chalk.yellow('2. View labels'))
    print(chalk.yellow('3. Create new note'))
    print(chalk.yellow('\'q\' or \'quit\' to exit\n'))


def print_notes_menu():
    print(chalk.yellow('1. View note details'))
    print(chalk.yellow('2. Delete note'))
    print(chalk.yellow('\'m\' or \'main\' to return to main menu\n'))


def print_all_notes():
    notes = Note.select()
    print(chalk.cyan('\nAll Notes'))
    print('---------')
    for note in notes:
        print(chalk.green(f'{note.id}. {note.title}'))
    print()


def print_all_labels():
    labels = Label.select()
    print('\nLabels')
    print('------')
    for label in labels:
        print(f'{label.id}. {label.name}')
    print()


while True:
    print_main_menu()
    user_input = input('Enter choice: ')

    # QUIT
    if user_input == 'q' or user_input == 'quit':
        break

    # VIEW NOTES
    elif user_input == '1':
        while True:
            print_all_notes()
            print_notes_menu()
            user_input = input('Enter choice: ')

            # RETURN TO MAIN MENU
            if user_input == 'm' or user_input == 'main':
                break

            # VIEW NOTE DETAILS
            elif user_input == '1':
                user_input = input('Enter note id: ')

                try:
                    note = Note.get_by_id(user_input)

                    print(chalk.cyan(f'\n{note.title}'))
                    print('-' * len(note.title))
                    print(chalk.green(note.content))
                    print(chalk.cyan(f'\nDate created: {note.date_created}\n'))
                    input('Press ENTER to return to notes menu')

                except DoesNotExist:
                    print(f'\nNote with id {user_input} not found.')

            # DELETE NOTE
            elif user_input == '2':
                user_input = input('Enter note id: ')

                try:
                    Note.get_by_id(user_input)
                    Note.delete_by_id(user_input)
                    print(f'\nNote with id {user_input} deleted.')

                except DoesNotExist:
                    print(f'\nNote with id {user_input} does not exist.')

                # try, except block uses get_by_id() to determine whether note with
                # given ID exists, and to print message to the console if it doesn't.
                # delete_by_id() will actually still work (i.e. not throw an error)
                # if a note with that ID doesn't exist.

            else:
                print(chalk.red('Invalid input'))

    # VIEW LABELS
    elif user_input == '2':
        print_all_labels()

    # CREATE NEW NOTE
    elif user_input == '3':
        note_title = input('Title: ')
        note_content = input('Write your note here.\n')
        Note(title=note_title, content=note_content).save()
        print('Note saved')

    else:
        print(chalk.red('Invalid input'))
