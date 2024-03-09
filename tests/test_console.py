#!/usr/bin/python3
"""Unittest for console.py has been established"""
import sys
import json
import models
import unittest
import StringIO from io
from unittest.mock import patch
from os import rename, remove
from console import HBNBCommand


class TestHBNBCommandprompt(unittest.TestCase):
    """Unittest for the 'prompt' command of the HBNB Command interpreter"""

    def testpromptstr(self):
        """Test: to ensure the right 'prompt' str is set"""
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def testemptylineinput(self):
        """Test: to handle empty command line input"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", result.getvalue().strip())


class TestHBNBCommandhelp(unittest.TestCase):
    """Unittest for the 'help' command within the HBNB Command interpreter"""

    def testhelpEOF(self):
        """Test: 'help' message for the EOF command"""
        expmsg = "signal to exit the program in non-interactive mode"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testhelpall(self):
        """Test: 'help' message for the all command"""
        expmsg = ("prints all string representation of all"
                  " class based instances")
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testhelpcount(self):
        """Test: 'help' message for the count command"""
        expmsg = "gets and returns the number of instances in a class"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testhelpcreate(self):
        """Test: 'help' message for the create command"""
        expmsg = "creates a new instance of a class, save it and print the id"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testhelpdestroy(self):
        """Test: 'help' message for the destroy command"""
        expmsg = "deletes an instance based on the class name and its id"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testhelp(self):
        """Test: 'help' message is printed correctly"""
        expmsg = ("Documented commands (type help <topic>):\n"
                  "========================================\n"
                  "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testhelphelp(self):
        """Test: 'help' message for the help command"""
        expmsg = ('List available commands with "help" or detailed'
                  ' help with "help cmd".')
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help help"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testhelpquit(self):
        """Test: 'help' message for the quit command"""
        expmsg = "the command quit to exit the program"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testhelpshow(self):
        """Test: 'help' message for the show command"""
        expmsg = "prints the string representation of a class instance and id"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testhelpupdate(self):
        """Test: 'help' message for the update command"""
        expmsg = "updates an instance based on the class name and id"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(expmsg, result.getvalue().strip())


class TestHBNBCommandexit(unittest.TestCase):
    """Unittest for the 'exit' command of the HBNB Command interpreter"""

    def testquitexits(self):
        """Test if the 'quit' cmd exits the command interpreter"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def testEOFexits(self):
        """Test if the 'EOF' cmd exits the command interpreter"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommandall(unittest.TestCase):
    """Unittest for the 'all' command of the HBNB Command interpreter"""

    @classmethod
    def setUp(self):
        """SetUp environment for testing the 'all' command"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass
        models.FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """Cleanup environment after testing the 'all' command"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testallinvalidclassname(self):
        """Test 'all' cmd with invalid class name"""
        expmsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("all InvalidModel"))
            self.assertEqual(expmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("InvalidModel.all()"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testallobjectsnotation(self):
        """Test 'all' cmd for all objects with space,dot notation"""
        def validobjt(classnm):
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd("all"))
                self.assertIn(classnm, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(".all()"))
                self.assertIn(classnm, result.getvalue().strip())
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")

    def testsingleobjectnotation(self):
        """Test 'all' cmd for single object with space,dot notation"""
        clstest = ["BaseModel", "User", "State", "City", "Amenity",
                   "Place", "Review"]

        def validobjt(classnm):
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"all {classnm}"))
                self.assertIn(classnm, result.getvalue().strip())
                if classnm != "BaseModel":
                    self.assertNotIn("BaseModel", result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.all()"))
                self.assertIn(classnm, result.getvalue().strip())
                if classnm != "BaseModel":
                    self.assertNotIn("BaseModel", result.getvalue().strip())
        for cls in clstest:
            validobjt(cls)


class TestHBNBCommandcount(unittest.TestCase):
    """Unittest for the 'count' command of the HBNB Command Interpreter"""

    @classmethod
    def setUp(self):
        """SetUp environment for testing the 'count' command"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass
        models.FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDown(self):
        """Clean up environment after testing the 'count' command"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testcountinvalidclassname(self):
        """Test 'count' cmd with invlaid class name"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("InvModel.count()"))
            self.assertEqual("0", result.getvalue().strip())

    def testcountobject(self):
        """Test 'count' cmd for objects of various classes"""
        def validobjt(classnm):
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.count()"))
                self.assertEqual("1", result.getvalue().strip())
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")


class TestHBNBCommandcreate(unittest.TestCase):
    """Unittest for the 'create' command of the HBNB Command interpreter"""

    @classmethod
    def setUp(self):
        """SetUp environment for testing the 'create' cmd"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass
        models.FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """Cleanup environment after testing the 'create' command"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testcreatemissingclassname(self):
        """Test 'create' cmd with missing class name"""
        expmsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testcreateinvalidclassname(self):
        """Test 'create' cmd with invalid class name"""
        expmsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create InvalidClass"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testcreateinvalidsyntax(self):
        """Test 'create' cmd with invalid syntax"""
        expmsg = "** Invalid syntax: InvClass.create()"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("InvClass.create()"))
            self.assertEqual(expmsg, result.getvalue().strip())
        expmsg = "** Invalid syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testcreateobjectclass(self):
        """Test 'create' cmd for objects across various classes"""
        def validobjt(classnm):
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                self.assertLess(0, len(result.getvalue().strip()))
                objk = f"{classnm}.{result.getvalue().strip()}"
                self.assertIn(objk, models.storage.all().keys())
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")


class TestHBNBCommanddestroy(unittest.TestCase):
    """Unittest for the 'destroy' command of the HBNB Command interpreter"""

    @classmethod
    def setUp(self):
        """SetUp environment for testing the 'destroy' command"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass
        models.FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """Cleanup environment after testing the 'destroy' command"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testdestroymissingclassname(self):
        """Test 'destroy' cmd with missing class name"""
        expmsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(expmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testdestroyinvalidclassname(self):
        """Test 'destroy' cmd with invalid class name"""
        expmsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("destroy InvModel"))
            self.assertEqual(expmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("InvModel.destroy()"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testdestroymnoinstanceidnotation(self):
        """Test 'destroy' cmd with text instance id with space,dot notation"""
        def validobjt(classnm):
            expmsg = "** instance id missing **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"destroy {classnm}"))
                self.assertEqual(expmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.destroy()"))
                self.assertEqual(expmsg, result.getvalue().strip())
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")

    def testdestroynoinstancenotation(self):
        """Test 'destroy' cmd with missing instance with space,dot notation"""
        def validobjt(classnm):
            expmsg = "** no instance found **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"destroy {classnm} 26"))
                self.assertEqual(expmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.destroy(3)"))
                self.assertEqual(expmsg, result.getvalue().strip())
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")

    def testdestroyobjinfonotation(self):
        """Test 'destroy' cmd to delete obj info with space,dot notation"""
        def validobjt(classnm):
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                instid = result.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                robj = models.storage.all()[f"{classnm}.{instid}"]
                dstcmd = f"destroy {classnm} {instid}"
                self.assertFalse(HBNBCommand().onecmd(dstcmd))
                self.assertNotIn(robj, models.storage.all())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                instid = result.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                robj = models.storage.all()[f"{classnm}.{instid}"]
                dstcmd = f"{classnm}.destroy({instid})"
                self.assertFalse(HBNBCommand().onecmd(dstcmd))
                self.assertNotIn(robj, models.storage.all())
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")


class TestHBNBCommandshow(unittest.TestCase):
    """Unittest for the 'show' command of the HBNB Command interpreter"""

    @classmethod
    def setUp(self):
        """SetUp environment for testing the 'show' command"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass
        models.FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """Cleanup environment after testing the 'show' command"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testshowmissingclassname(self):
        """Test 'show' cmd with missing class name"""
        expmsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(expmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testshowinvalidclassname(self):
        """Test 'show' cmd with invalid class name"""
        expmsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("show InvModel"))
            self.assertEqual(expmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("InvModel.show()"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testshowmnoinstanceidnotation(self):
        """Test 'show' cmd with missing instance id with space,dot notation"""
        def validobjt(classnm):
            expmsg = "** instance id missing **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"show {classnm}"))
                self.assertEqual(expmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.show()"))
                self.assertEqual(expmsg, result.getvalue().strip())
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")

    def testshownoinstancenotation(self):
        """Test 'show' cmd with missing instance with space,dot notation"""
        def validobjt(classnm):
            expmsg = "** no instance found **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"show {classnm} 246"))
                self.assertEqual(expmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.show(13)"))
                self.assertEqual(expmsg, result.getvalue().strip())
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")

    def testshowobjinfonotation(self):
        """Test 'show' cmd to display object info with space,dot notation"""
        def validobjt(classnm):
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                instid = result.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                robj = models.storage.all()[f"{classnm}.{instid}"]
                shwcmd = f"show {classnm} {instid}"
                self.assertFalse(HBNBCommand().onecmd(shwcmd))
                self.assertEqual(robj.__str__(), result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                instid = result.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                robj = models.storage.all()[f"{classnm}.{instid}"]
                shwcmd = f"{classnm}.show({instid})"
                self.assertFalse(HBNBCommand().onecmd(shwcmd))
                self.assertEqual(robj.__str__(), result.getvalue().strip())
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")


class TestHBNBCommandupdate(unittest.TestCase):
    """Unittest for the 'update' command of the HBNB Command interpreter"""

    @classmethod
    def setUp(self):
        """SetUp environment for testing the 'update' cmd"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass
        models.FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """Cleanup environment after testing the 'update' cmd"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testupdatemissingclassname(self):
        """Test 'update' cmd with missing class name"""
        expmsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(expmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testupdateinvalidclassname(self):
        """Test 'update' cmd with invalid class name"""
        expmsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("update InvModel"))
            self.assertEqual(expmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("InvModel.update()"))
            self.assertEqual(expmsg, result.getvalue().strip())

    def testupdatemnoinstanceidnotation(self):
        """Test 'update' cmd with text instance id with space,dot notation"""
        def validobjt(classnm):
            expmsg = "** instance id missing **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"update {classnm}"))
                self.assertEqual(expmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.update()"))
                self.assertEqual(expmsg, result.getvalue().strip())
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")

    def testupdatenoinstancenotation(self):
        """Test 'update' cmd with missing instance with space,dot notation"""
        def validobjt(classnm):
            expmsg = "** no instance found **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"update {classnm} 2"))
                self.assertEqual(expmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.update(3)"))
                self.assertEqual(expmsg, result.getvalue().strip())
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")

    def testupdateattrnamenotation(self):
        """Test 'update' cmd with text attr name wiht space,dot notation"""
        def validobjt(classnm):
            expmsg = "** attribute name missing **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objtid = result.getvalue().strip()
                updtcmd = f"update {classnm} {objtid}"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(updtcmd))
                self.assertEqual(expmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objtid = result.getvalue().strip()
                updtcmd = f"{classnm}.update({objtid})"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(updtcmd))
                self.assertEqual(expmsg, result.getvalue().strip())
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")

    def testupdateattrvaluenotation(self):
        """Test 'update' cmd with msng attr value with space,dot notation"""
        def validobjt(classnm):
            expmsg = "** value missing **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objtid = result.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                updtcmd = f"update {classnm} {objtid} attrnm"
                self.assertFalse(HBNBCommand().onecmd(updtcmd))
                self.assertEqual(expmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objtid = result.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                updtcmd = f"{classnm}.update({objtid}, attrnm)"
                self.assertFalse(HBNBCommand().onecmd(updtcmd))
                self.assertEqual(expmsg, result.getvalue().strip())
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")

    def testupdatestrattrnotation(self):
        """Test 'update' cmd with string attr with space,dot notation"""
        def validobjt(classnm):
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objtid = result.getvalue().strip()
                updtcmd = f"update {classnm} {objtid} attrnm 'attrval'"
                self.assertFalse(HBNBCommand().onecmd(updtcmd))
                updtdict = models.storage.all()[f"{classnm}.{objtid}"].__dict__
                self.assertEqual("attrval", updtdict["attrnm"])
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objtid = result.getvalue().strip()
                updtcmd = f"{classnm}.update({objtid}, attrnm, 'attrval')"
                self.assertFalse(HBNBCommand().onecmd(updtcmd))
                updtdict = models.storage.all()[f"{classnm}.{objtid}"].__dict__
                self.assertEqual("attrval", updtdict["attrnm"])
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")

    def testupdateintattrnotation(self):
        """Test 'update' cmd with int attr with space,dot notation"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objtid = result.getvalue().strip()
            updtcmd = f"update Place {objtid} gstct 5"
            self.assertFalse(HBNBCommand().onecmd(updtcmd))
            updtdict = models.storage.all()[f"Place.{objtid}"].__dict__
            self.assertEqual(5, int(updtdict["gstct"]))
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objtid = result.getvalue().strip()
            updtcmd = f"Place.update({objtid}, gstct, 8)"
            self.assertFalse(HBNBCommand().onecmd(updtcmd))
            updtdict = models.storage.all()[f"Place.{objtid}"].__dict__
            self.assertEqual(8, int(updtdict["gstct"]))

    def testupdatefloatattrnotation(self):
        """Test 'update' cmd with float attr with space,dot notation"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objtid = result.getvalue().strip()
            updtcmd = f"update Place {objtid} latitude 5.6"
            self.assertFalse(HBNBCommand().onecmd(updtcmd))
            updtdict = models.storage.all()[f"Place.{objtid}"].__dict__
            self.assertEqual(5.6, (updtdict["latitude"]))
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objtid = result.getvalue().strip()
            updtcmd = f"Place.update({objtid}, latitude, 8.9)"
            self.assertFalse(HBNBCommand().onecmd(updtcmd))
            updtdict = models.storage.all()[f"Place.{objtid}"].__dict__
            self.assertEqual(8.9, (updtdict["latitude"]))

    def testupdatedictattrnotation(self):
        """Test 'update' cmd with dict attr with space,dot notation"""
        def validobjt(classnm):
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objtid = result.getvalue().strip()
                updtcmd = f"update {classnm} {objtid} "
                updtcmd = updtcmd + "{'attrnm': 'attrval'}"
                self.assertFalse(HBNBCommand().onecmd(updtcmd))
                updtdict = models.storage.all()[f"{classnm}.{objtid}"].__dict__
                self.assertEqual("attrval", updtdict["attrnm"])
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objtid = result.getvalue().strip()
                updtcmd = f"{classnm}.update('{objtid}', "
                updtcmd = updtcmd + "{'attrnm': 'attrval'})"
                self.assertFalse(HBNBCommand().onecmd(updtcmd))
                updtdict = models.storage.all()[f"{classnm}.{objtid}"].__dict__
                self.assertEqual("attrval", updtdict["attrnm"])
        validobjt("BaseModel")
        validobjt("User")
        validobjt("State")
        validobjt("City")
        validobjt("Amenity")
        validobjt("Place")
        validobjt("Review")

    def testupdatedictintnotation(self):
        """Test 'update' cmd with dict int with space,dot notation"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objtid = result.getvalue().strip()
            updtcmd = f"update Place {objtid} "
            updtcmd = updtcmd + "{'gstct': 7}"
            self.assertFalse(HBNBCommand().onecmd(updtcmd))
            updtdict = models.storage.all()[f"Place.{objtid}"].__dict__
            self.assertEqual(7, updtdict["gstct"])
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objtid = result.getvalue().strip()
            updtcmd = f"Place.update({objtid}, "
            updtcmd = updtcmd + "{'gstct': 7})"
            self.assertFalse(HBNBCommand().onecmd(updtcmd))
            updtdict = models.storage.all()[f"Place.{objtid}"].__dict__
            self.assertEqual(7, updtdict["gstct"])

    def testupdatedictfloatnotation(self):
        """Test 'update' cmd with dict float with space,dot nottion"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objtid = result.getvalue().strip()
            updtcmd = f"update Place {objtid} "
            updtcmd = updtcmd + "{'longitude': 4.6}"
            self.assertFalse(HBNBCommand().onecmd(updtcmd))
            updtdict = models.storage.all()[f"Place.{objtid}"].__dict__
            self.assertEqual(4.6, updtdict["longitude"])
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objtid = result.getvalue().strip()
            updtcmd = f"Place.update({objtid}, "
            updtcmd = updtcmd + "{'latitude': 7.9})"
            self.assertFalse(HBNBCommand().onecmd(updtcmd))
            updtdict = models.storage.all()[f"Place.{objtid}"].__dict__
            self.assertEqual(7.9, updtdict["latitude"])
