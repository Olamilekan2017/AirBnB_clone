#!/usr/bin/python3
"""Console class serving as the projects entry point has been defined"""
import cmd
import models
from re import search
from shlex import split
from models.city import City
from models.user import User
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """HBnB project console is represented"""
    prompt = "(hbnb)"
    classes = \
        {"City", "User", "State", "Place", "Review", "Amenity", "BaseModel"}

    def do_EOF(self, args):
        """Signal for program exit in non-interactive mode"""
        return True

    def do_quit(self, args):
        """Quit command is used to exit the program"""
        return True

    def emptyline(self):
        """Prompt will not execute any action"""
        pass

    def do_create(self, args):
        """Instantiate new class instance save it display its Id"""
        classargs = parse(args)
        if len(classargs) == 0:
            print("** class name missing **")
        elif classargs[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            print(eval(classargs[0])().id)
            models.storage.save()

    def do_show(self, args):
        """Prints str representation of a class instance and id"""
        classargs = parse(args)
        dictobj = models.storage.all()
        if len(classargs) == 0:
            print("** class name missing **")
        elif classargs[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(classargs) == 1:
            print("** instance id missing **")
        elif f"{classargs[0]}.{classargs[1]}" not in dictobj:
            print("** no instance found **")
        else:
            print(dictobj[f"{classargs[0]}.{classargs[1]}"])

    def do_destroy(self, args):
        """Deletes instance based on the class name and id"""
        classargs = parse(args)
        dictobj = models.storage.all()
        if len(classargs) == 0:
            print("** class name missing **")
        elif classargs[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(classargs) == 1:
            print("** instance id missing **")
        elif f"{classargs[0]}.{classargs[1]}" not in dictobj:
            print("** no instance found **")
        else:
            del dictobj[f"{classargs[0]}.{classargs[1]}"]
            models.storage.save()

    def do_all(self, args):
        """Prints str of all instances based on class"""
        classargs = parse(args)
        if len(classargs) > 0 and classargs[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            objlist = []
            for obj in models.storage.all().values():
                objclassnm = obj.__class__.__name__
                if len(classargs) > 0 and classargs[0] == objclassnm:
                    objlist.append(obj.__str__())
                elif len(classargs) == 0:
                    objlist.append(obj.__str__())
            print(objlist)

    def do_count(self, args):
        """Gets and returns number of instances in class"""
        classargs = parse(args)
        total = 0
        for obj in models.storage.all().values():
            if classargs[0] == obj.__class__.__name__:
                total = total + 1
        print(total)

    def do_update(self, args):
        """Modify an instance in the class using name and id"""
        classargs = parse(args)
        dictobj = models.storage.all()
        if len(classargs) == 0:
            print("** class name missing **")
            return False
        if classargs[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False
        if len(classargs) == 1:
            print("** instance id missing **")
            return False
        if f"{classargs[0]}.{classargs[1]}" not in dictobj.keys():
            print("** no instance found **")
            return False
        if len(classargs) == 2:
            print("** attribute name missing **")
            return False
        if len(classargs) == 3:
            try:
                type(eval(classargs[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(classargs) == 4:
            obj = dictobj[f"{classargs[0]}.{classargs[1]}"]
            if classargs[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[classargs[2]])
                obj.__dict__[classargs[2]] = valtype(classargs[3])
            else:
                obj.__dict__[classargs[2]] = classargs[3]
        elif type(eval(classargs[2])) == dict:
            obj = dictobj[f"{classargs[0]}.{classargs[1]}"]
            for ky, val in eval(classargs[2]).items():
                if (ky in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[ky]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[ky])
                    obj.__dict__[ky] = valtype(val)
                else:
                    obj.__dict__[ky] = val
        models.storage.save()

    def default(self, args):
        """Default message for invalid module input of HBNBCommand"""
        argsdict = {
            "show": self.do_show,
            "update": self.do_update,
            "all": self.do_all,
            "count": self.do_count,
            "destroy": self.do_destroy
        }
        dotmt = re.search(r"\.", args)
        if dotmt is not None:
            classargs = [args[:dotmt.span()[0]], args[dotmt.span()[1]:]]
            dotmt = search(r"\((.*?)\)", classargs[1])
            if dotmt is not None:
                prsecmd = [classargs[1][:dotmt.span()[0]], dotmt.group()[1:-1]]
                if prsecmd[0] in argsdict.keys():
                    fulcal = f"{classargs[0]} {prsecmd[1]}"
                    return argsdict[prsecmd[0]](fulcal)
        print(f"** Invalid syntax: {args}")
        return False


def parse(args):
    """Divide str and gets items in curly braces or square brackets"""
    curlybr = search(r"\{(.*?)\}", args)
    squebr = search(r"\[(.*?)\]", args)
    if curlybr is None:
        if squebr is None:
            return [k.strip(",") for k in split(args)]
        else:
            toks = split(args[:squebr.span()[0]])
            reslist = [k.strip(",") for k in toks]
            reslist.append(squebr.group())
            return reslist
    else:
        toks = split(args[:curlybr.span()[0]])
        reslist = [k.strip(",") for k in toks]
        reslist.append(curlybr.group())
        return reslist

    if __name__ == '__main__':
        HBNBCommand().cmdloop()
