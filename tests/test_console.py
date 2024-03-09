#!/usr/bin/python3
"""Unittest for console.py is defined"""
import unittest
import sys
import json
import models
from unittest.mock import patch
from os import rename, remove
from io import StringIO
from console import HBNBCommand


class TestHBNBCommandprompt(unittest.TestCase):
    """Unittest for the 'prompt' command of the HBNB Command interpreter"""

    def testpromptstr(self):
        """test to ensure the right 'prompt' string is set"""
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def testemptylineinput(self):
        """test to handle empty command line input"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", result.getvalue().strip())


class TestHBNBCommandhelp(unittest.TestCase):
    """Unittest for the 'help' command of the HBNB Command interpreter"""

    def testhelpEOF(self):
        """test the 'help' message for the EOF command"""
        prtmsg = "Signal for program exit in non-interactive mode"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testhelpall(self):
        """test the 'help' message for the all command"""
        prtmsg = "Prints str of all instances based on class"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testhelpcount(self):
        """test the 'help' message for the count command"""
        prtmsg = "Gets and returns number of instances in class"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testhelpcreate(self):
        """test the 'help' message for the create command"""
        prtmsg = "Instantiate new class instance save it display its id"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testhelpdestroy(self):
        """test the 'help' message for the destroy command"""
        prtmsg = "Deletes instance based on the class name and id"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testhelp(self):
        """test the 'help' message is printed correctly"""
        prtmsg = ("Documented commands (type help <topic>):\n"
                  "========================================\n"
                  "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testhelphelp(self):
        """test the 'help' message for the help command"""
        prtmsg = ('List available commands with "help" or detailed'
                  ' help with "help cmd".')
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help help"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testhelpquit(self):
        """test the 'help' message for the quit command"""
        prtmsg = "Quit command is used to exit the program"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testhelpshow(self):
        """test the 'help' message for the show command"""
        prtmsg = "Prints str representation of a class instance and id"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testhelpupdate(self):
        """test the 'help' message for the update command"""
        prtmsg = "Modify an instance in the class using name and id"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(prtmsg, result.getvalue().strip())


class TestHBNBCommandexit(unittest.TestCase):
    """Unittest for the 'exit' command of the HBNB Command interpreter"""

    def testquitexits(self):
        """test if the 'quit' command exits the command interpreter"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def testEOFexits(self):
        """test if the 'EOF' command exits the command interpreter"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommandall(unittest.TestCase):
    """Unittest for the 'all' command of the HBNB Command interpreter"""

    @classmethod
    def setUp(self):
        """setUp environment for the 'all' command tests"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass
        models.FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """ clean up environment after the 'all' command tests"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testallinvalidclassname(self):
        """test 'all' command with invalid class name"""
        prtmsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("all InvalidModel"))
            self.assertEqual(prtmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("InvalidModel.all()"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testallobjectsnotation(self):
        """test 'all' command for all objects using space,dot notation"""
        def vldobj(classnm):
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
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")

    def testsingleobjectnotation(self):
        """test 'all' command for single object using space,dot notation"""
        clstest = ["BaseModel", "User", "State", "City", "Amenity",
                   "Place", "Review"]

        def vldobj(classnm):
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
            vldobj(cls)


class TestHBNBCommandcount(unittest.TestCase):
    """Unittest for the 'count' command of the HBNB Command Interpreter"""

    @classmethod
    def setUp(self):
        """setUp environment for the 'count' command tests"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass
        models.FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDown(self):
        """clean up environment after the 'count' command tests"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testcountinvalidclassname(self):
        """test 'count' command with invlaid class name"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("InvModel.count()"))
            self.assertEqual("0", result.getvalue().strip())

    def testcountobject(self):
        """test 'count' command for objects of various classes"""
        def vldobj(classnm):
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.count()"))
                self.assertEqual("1", result.getvalue().strip())
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")


class TestHBNBCommandcreate(unittest.TestCase):
    """Unittest for the 'create' command of the HBNB Command interpreter"""

    @classmethod
    def setUp(self):
        """setUp environment for the 'create' command tests"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass
        models.FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """clean up environment after the 'create' command tests"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testcreatemissingclassname(self):
        """test 'create' command with missing class name"""
        prtmsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testcreateinvalidclassname(self):
        """test 'create' command with invalid class name"""
        prtmsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create InvalidClass"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testcreateinvalidsyntax(self):
        """test 'create' command with invalid syntax"""
        prtmsg = "** Invalid syntax: InvClass.create()"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("InvClass.create()"))
            self.assertEqual(prtmsg, result.getvalue().strip())
        prtmsg = "** Invalid syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testcreateobjectclass(self):
        """test 'create' command for objects across various classes"""
        def vldobj(classnm):
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                self.assertLess(0, len(result.getvalue().strip()))
                objk = f"{classnm}.{result.getvalue().strip()}"
                self.assertIn(objk, models.storage.all().keys())
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")


class TestHBNBCommanddestroy(unittest.TestCase):
    """Unittest for the 'destroy' command of the HBNB Command interpreter"""

    @classmethod
    def setUp(self):
        """setUp environment for the 'destroy' command tests"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass
        models.FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """clean up environment after the 'destroy' command tests"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testdestroymissingclassname(self):
        """test 'destroy' command with missing class name"""
        prtmsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(prtmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testdestroyinvalidclassname(self):
        """test 'destroy' command with invalid class name"""
        prtmsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("destroy InvModel"))
            self.assertEqual(prtmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("InvModel.destroy()"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testdestroymnoinstanceidnotation(self):
        """test 'destroy' cmd with msng instance id using space,dot notation"""
        def vldobj(classnm):
            prtmsg = "** instance id missing **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"destroy {classnm}"))
                self.assertEqual(prtmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.destroy()"))
                self.assertEqual(prtmsg, result.getvalue().strip())
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")

    def testdestroynoinstancenotation(self):
        """test 'destroy' cmd with missing instance using space,dot notation"""
        def vldobj(classnm):
            prtmsg = "** no instance found **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"destroy {classnm} 26"))
                self.assertEqual(prtmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.destroy(3)"))
                self.assertEqual(prtmsg, result.getvalue().strip())
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")

    def testdestroyobjinfonotation(self):
        """test 'destroy' cmd to delete obj info using space,dot notation"""
        def vldobj(classnm):
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                instid = result.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                robj = models.storage.all()[f"{classnm}.{instid}"]
                delcmd = f"destroy {classnm} {instid}"
                self.assertFalse(HBNBCommand().onecmd(delcmd))
                self.assertNotIn(robj, models.storage.all())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                instid = result.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                robj = models.storage.all()[f"{classnm}.{instid}"]
                delcmd = f"{classnm}.destroy({instid})"
                self.assertFalse(HBNBCommand().onecmd(delcmd))
                self.assertNotIn(robj, models.storage.all())
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")


class TestHBNBCommandshow(unittest.TestCase):
    """Unittest for the 'show' command of the HBNB Command interpreter"""

    @classmethod
    def setUp(self):
        """setUp environment for the 'show' command tests"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass
        models.FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """clean up environment after the 'show' command tests"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testshowmissingclassname(self):
        """test 'show' command with missing class name"""
        prtmsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(prtmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testshowinvalidclassname(self):
        """test 'show' command with invalid class name"""
        prtmsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("show InvModel"))
            self.assertEqual(prtmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("InvModel.show()"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testshowmnoinstanceidnotation(self):
        """test 'show' cmd with missing instance id using space,dot notation"""
        def vldobj(classnm):
            prtmsg = "** instance id missing **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"show {classnm}"))
                self.assertEqual(prtmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.show()"))
                self.assertEqual(prtmsg, result.getvalue().strip())
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")

    def testshownoinstancenotation(self):
        """test 'show' cmd with missing instance using space,dot notation"""
        def vldobj(classnm):
            prtmsg = "** no instance found **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"show {classnm} 246"))
                self.assertEqual(prtmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.show(13)"))
                self.assertEqual(prtmsg, result.getvalue().strip())
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")

    def testshowobjinfonotation(self):
        """test 'show' cmd to display object info using space,dot notation"""
        def vldobj(classnm):
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
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")


class TestHBNBCommandupdate(unittest.TestCase):
    """Unittest for the 'update' command of the HBNB Command interpreter"""

    @classmethod
    def setUp(self):
        """setUp environment for the 'update' command tests"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass
        models.FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """clean up environment after the 'update' command tests"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testupdatemissingclassname(self):
        """test 'update' command with missing class name"""
        prtmsg = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(prtmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testupdateinvalidclassname(self):
        """test 'update' command with invalid class name"""
        prtmsg = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("update InvModel"))
            self.assertEqual(prtmsg, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("InvModel.update()"))
            self.assertEqual(prtmsg, result.getvalue().strip())

    def testupdatemnoinstanceidnotation(self):
        """test 'update' cmd with msng instance id using space,dot notation"""
        def vldobj(classnm):
            prtmsg = "** instance id missing **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"update {classnm}"))
                self.assertEqual(prtmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.update()"))
                self.assertEqual(prtmsg, result.getvalue().strip())
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")

    def testupdatenoinstancenotation(self):
        """test 'update' cmd with missing instance using space,dot notation"""
        def vldobj(classnm):
            prtmsg = "** no instance found **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"update {classnm} 2"))
                self.assertEqual(prtmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{classnm}.update(3)"))
                self.assertEqual(prtmsg, result.getvalue().strip())
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")

    def testupdateattrnamenotation(self):
        """test 'update' cmd with msng attr name using space,dot notation"""
        def vldobj(classnm):
            prtmsg = "** attribute name missing **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objid = result.getvalue().strip()
                uptcmd = f"update {classnm} {objid}"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(uptcmd))
                self.assertEqual(prtmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objid = result.getvalue().strip()
                uptcmd = f"{classnm}.update({objid})"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(uptcmd))
                self.assertEqual(prtmsg, result.getvalue().strip())
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")

    def testupdateattrvaluenotation(self):
        """test 'update' cmd with msng attr value using space,dot notation"""
        def vldobj(classnm):
            prtmsg = "** value missing **"
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objid = result.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                uptcmd = f"update {classnm} {objid} attrnm"
                self.assertFalse(HBNBCommand().onecmd(uptcmd))
                self.assertEqual(prtmsg, result.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objid = result.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                uptcmd = f"{classnm}.update({objid}, attrnm)"
                self.assertFalse(HBNBCommand().onecmd(uptcmd))
                self.assertEqual(prtmsg, result.getvalue().strip())
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")

    def testupdatestrattrnotation(self):
        """test 'update' cmd with string attr using space,dot notation"""
        def vldobj(classnm):
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objid = result.getvalue().strip()
                uptcmd = f"update {classnm} {objid} attrnm 'attrval'"
                self.assertFalse(HBNBCommand().onecmd(uptcmd))
                updict = models.storage.all()[f"{classnm}.{objid}"].__dict__
                self.assertEqual("attrval", updict["attrnm"])
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objid = result.getvalue().strip()
                uptcmd = f"{classnm}.update({objid}, attrnm, 'attrval')"
                self.assertFalse(HBNBCommand().onecmd(uptcmd))
                updict = models.storage.all()[f"{classnm}.{objid}"].__dict__
                self.assertEqual("attrval", updict["attrnm"])
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")

    def testupdateintattrnotation(self):
        """test 'update' cmd with int attr using space,dot notation"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objid = result.getvalue().strip()
            uptcmd = f"update Place {objid} gstct 5"
            self.assertFalse(HBNBCommand().onecmd(uptcmd))
            updict = models.storage.all()[f"Place.{objid}"].__dict__
            self.assertEqual(5, int(updict["gstct"]))
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objid = result.getvalue().strip()
            uptcmd = f"Place.update({objid}, gstct, 8)"
            self.assertFalse(HBNBCommand().onecmd(uptcmd))
            updict = models.storage.all()[f"Place.{objid}"].__dict__
            self.assertEqual(8, int(updict["gstct"]))

    def testupdatefloatattrnotation(self):
        """test 'update' cmd with float attr using space,dot notation"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objid = result.getvalue().strip()
            uptcmd = f"update Place {objid} latitude 5.6"
            self.assertFalse(HBNBCommand().onecmd(uptcmd))
            updict = models.storage.all()[f"Place.{objid}"].__dict__
            self.assertEqual(5.6, (updict["latitude"]))
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objid = result.getvalue().strip()
            uptcmd = f"Place.update({objid}, latitude, 8.9)"
            self.assertFalse(HBNBCommand().onecmd(uptcmd))
            updict = models.storage.all()[f"Place.{objid}"].__dict__
            self.assertEqual(8.9, (updict["latitude"]))

    def testupdatedictattrnotation(self):
        """test 'update' cmd with dict attr using space,dot notation"""
        def vldobj(classnm):
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objid = result.getvalue().strip()
                uptcmd = f"update {classnm} {objid} "
                uptcmd += "{'attrnm': 'attrval'}"
                self.assertFalse(HBNBCommand().onecmd(uptcmd))
                updict = models.storage.all()[f"{classnm}.{objid}"].__dict__
                self.assertEqual("attrval", updict["attrnm"])
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {classnm}"))
                objid = result.getvalue().strip()
                uptcmd = f"{classnm}.update('{objid}', "
                uptcmd += "{'attrnm': 'attrval'})"
                self.assertFalse(HBNBCommand().onecmd(uptcmd))
                updict = models.storage.all()[f"{classnm}.{objid}"].__dict__
                self.assertEqual("attrval", updict["attrnm"])
        vldobj("BaseModel")
        vldobj("User")
        vldobj("State")
        vldobj("City")
        vldobj("Amenity")
        vldobj("Place")
        vldobj("Review")

    def testupdatedictintnotation(self):
        """test 'update' cmd with dict int using space,dot notation"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objid = result.getvalue().strip()
            uptcmd = f"update Place {objid} "
            uptcmd += "{'gstct': 7}"
            self.assertFalse(HBNBCommand().onecmd(uptcmd))
            updict = models.storage.all()[f"Place.{objid}"].__dict__
            self.assertEqual(7, updict["gstct"])
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objid = result.getvalue().strip()
            uptcmd = f"Place.update({objid}, "
            uptcmd += "{'gstct': 7})"
            self.assertFalse(HBNBCommand().onecmd(uptcmd))
            updict = models.storage.all()[f"Place.{objid}"].__dict__
            self.assertEqual(7, updict["gstct"])

    def testupdatedictfloatnotation(self):
        """test 'update' cmd with dict float using space,dot nottion"""
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objid = result.getvalue().strip()
            uptcmd = f"update Place {objid} "
            uptcmd += "{'longitude': 4.6}"
            self.assertFalse(HBNBCommand().onecmd(uptcmd))
            updict = models.storage.all()[f"Place.{objid}"].__dict__
            self.assertEqual(4.6, updict["longitude"])
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            objid = result.getvalue().strip()
            uptcmd = f"Place.update({objid}, "
            uptcmd += "{'latitude': 7.9})"
            self.assertFalse(HBNBCommand().onecmd(uptcmd))
            updict = models.storage.all()[f"Place.{objid}"].__dict__
            self.assertEqual(7.9, updict["latitude"])
