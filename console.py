#!/usr/bin/python3
""" le module console """
import cmd
import sys
import re
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import Column, String


class HBNBCommand(cmd.Cmd):
    """ contiens de fonctionalité de hbnb"""

    # Anformation about: determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """imprimer si isaaty est false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """reformuler la commande line de l'advance command synthax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # Anformation about: initialize line elements

        # Anformation about: scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # Anformation about: parse line left to right
            pline = line[:]  # Anformation about: parsed line

            # Anformation about: isolate <class name>
            _cls = pline[:pline.find('.')]

            # Anformation about: isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # Anformation about: if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # Anformation about: partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # Anformation about: pline convert to tuple

                # Anformation about: isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # Anformation about: possible bug here:
                # Anformation about: empty quotes register as empty _id when replaced

                # Anformation about: if arguments exist beyond _id
                pline = pline[2].strip()  # Anformation about: pline is now str
                if pline:
                    # Anformation about: check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # Anformation about: _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """imprimé si isatty est faux"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ methode pour quitter hbnb console"""
        exit()

    def help_quit(self):
        """ imprimer la documentation aide pour quitter """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ conserver eof pour quitter le program """
        print()
        exit()

    def help_EOF(self):
        """ imprimer l'aide pour eof """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ modifier la ligne vide de cmd """
        pass

    def do_create(self, args):
        """ cree un objet de n'importe quelle classes"""
        pattern = """(^\w+)((?:\s+\w+=[^\s]+)+)?"""
        m = re.match(pattern, args)
        args = [s for s in m.groups() if s] if m else []

        if not args:
            print("** class name missing **")
            return

        className = args[0]

        if className not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        kwargs = dict()
        if len(args) > 1:
            params = args[1].split(" ")
            params = [param for param in params if param]
            for param in params:
                [name, value] = param.split("=")
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:-1].replace('_', ' ')
                elif '.' in value:
                    value = float(value)
                else:
                    value = int(value)
                kwargs[name] = value

        new_instance = HBNBCommand.classes[className]()
        
        for attrName, attrValue in kwargs.items():
            setattr(new_instance, attrName, attrValue) 

        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        """ information d'aide pour cree une methode"""
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ methode pour montrer un individuel object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # Anformation about: guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ information d'aide pour show commande """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ detruire un objet specifique """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ information d'aide pour detruire commande """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ monterer tous les objets"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # Anformation about: remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all().items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ infos d'aide pou tous command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """compter nombre courant de class instance"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ update objet avec nouveau infos """
        c_name = c_id = att_name = att_val = kwargs = ''

        # Anformation about: isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # Anformation about: class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # Anformation about: class name invalid
            print("** class doesn't exist **")
            return

        # Anformation about: isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # Anformation about: id not present
            print("** instance id missing **")
            return

        # Anformation about: generate key from class and id
        key = c_name + "." + c_id

        # Anformation about: determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # Anformation about: first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # Anformation about: reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # Anformation about: isolate args
            args = args[2]
            if args and args[0] == '\"':  # Anformation about: check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # Anformation about: if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # Anformation about: check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # Anformation about: if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # Anformation about: retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # Anformation about: iterate through attr names and values
        for i, att_name in enumerate(args):
            # Anformation about: block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # Anformation about: following item is value
                if not att_name:  # Anformation about: check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # Anformation about: check for att_value
                    print("** value missing **")
                    return
                # Anformation about: type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # Anformation about: update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # Anformation about: save updates to file

    def help_update(self):
        """ info d'aide pour la mise a jours class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
