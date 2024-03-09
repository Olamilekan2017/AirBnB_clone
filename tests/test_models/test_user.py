#!/usr/bin/python3
"""Unittest for usr.py has been established"""
import time
import models
import unittest
from os import rename, remove
from datetime import datetime
from models.user import User


class TestUserinstance(unittest.TestCase):
    """Unittest for instantiation of User class instances"""

    def testUserinstancenoargs(self):
        """Test User instance without any arguments"""
        self.assertEqual(type(User()), User)

    def testUsernewinstancestorage(self):
        """Test instances of User are stored in objects set"""
        self.assertIn(User(), models.storage.all().values())

    def testUseridattr(self):
        """Test if 'id' attr of User is public string"""
        self.assertEqual(str, type(User().id))

    def testUsercreated_atattr(self):
        """Test if 'created_at' attr of User is pub datetime obj"""
        self.assertEqual(datetime, type(User().created_at))

    def testUserupdated_atattr(self):
        """Test if 'updated_at' attr of User is pub datetime obj"""
        self.assertEqual(datetime, type(User().updated_at))

    def testUseremailattr(self):
        """Test if 'email' attr of User isa public string"""
        self.assertEqual(str, type(User.email))

    def testUserpasswordattr(self):
        """Test if 'password' attr of User is public string"""
        self.assertEqual(str, type(User.password))

    def testUserfirst_nameattr(self):
        """Test if 'first_name' attr of User is public string"""
        self.assertEqual(str, type(User.first_name))

    def testUserlast_nameattr(self):
        """Test if 'last_name' attr of User is public string"""
        self.assertEqual(str, type(User.last_name))

    def testUsertwoids(self):
        """Test that two instances User have unique 'ids'"""
        usr1 = User()
        usr2 = User()
        self.assertNotEqual(usr1.id, usr2.id)

    def testUsertwocreated_at(self):
        """Test the 'created_at' timestamp of two instances User"""
        usr1 = User()
        time.sleep(0.07)
        usr2 = User()
        self.assertLess(usr1.created_at, usr2.created_at)

    def testUsertwoupdated_at(self):
        """Test the 'updated_at' timestamp of two instances User"""
        usr1 = User()
        time.sleep(0.07)
        usr2 = User()
        self.assertLess(usr1.updated_at, usr2.updated_at)

    def testUserstrrep(self):
        """Test the string representation of a User instance"""
        currentdt = datetime.today()
        daterepr = repr(currentdt)
        usr = User()
        usr.id = "28557"
        usr.created_at = usr.updated_at = currentdt
        usrstr = usr.__str__()
        self.assertIn("[User] (28557)", usrstr)
        self.assertIn("'id': '28557'", usrstr)
        self.assertIn("'created_at': " + daterepr, usrstr)
        self.assertIn("'updated_at': " + daterepr, usrstr)

    def testUserunusedargs(self):
        """Test that unused arguments has no impact BaseModel instances"""
        self.assertNotIn(None, User(None).__dict__.values())

    def testUserinstancekwargs(self):
        """Test instantiation User with specified keywordargs(kwargs)"""
        currentdt = datetime.today()
        dateiso = currentdt.isoformat()
        usr = User(id="433", created_at=dateiso, updated_at=dateiso)
        self.assertEqual(usr.id, "433")
        self.assertEqual(usr.created_at, currentdt)
        self.assertEqual(usr.updated_at, currentdt)

    def testUserinstanceNonekwargs(self):
        """Test instantiation User with None as kwargs"""
        self.assertRaises(TypeError, lambda: User(id=None,
                          created_at=None, updated_at=None))


class TestUsersave(unittest.TestCase):
    """Unittest for the save method of the User class"""

    @classmethod
    def setUp(self):
        """SetUp environment for testing the 'save' method"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """Cleanup environment after testing the 'save' method"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testUseronesave(self):
        """Test that User 'save' call updates 'updated_at' timestamp"""
        usr = User()
        time.sleep(0.08)
        frstupdated_at = usr.updated_at
        usr.save()
        self.assertLess(frstupdated_at, usr.updated_at)

    def testUsertwosaves(self):
        """Test two User 'save' calls updates 'updated_at' timestamps"""
        usr = User()
        time.sleep(0.06)
        frstupdated_at = usr.updated_at
        usr.save()
        secndupdated_at = usr.updated_at
        self.assertLess(frstupdated_at, secndupdated_at)
        time.sleep(0.06)
        usr.save()
        self.assertLess(secndupdated_at, usr.updated_at)

    def testUsersaveargs(self):
        """Test 'save' method of User call with arguments"""
        self.assertRaises(TypeError, lambda: User().save(None))

    def testUsersaveJSONfile(self):
        """Test 'save' method of User updates the corresponding JSON file"""
        usr = User()
        usr.save()
        usrid = "User." + usr.id
        with open("file.json", "r") as fl:
            self.assertIn(usrid, fl.read())


class TestUserto_dict(unittest.TestCase):
    """Unittest for the 'to_dict' method of the User class"""

    def testUserto_dcittype(self):
        """Test if output User 'to_dict' is a dictionary"""
        self.assertTrue(dict, type(User().to_dict()))

    def testUserto_dictkeys(self):
        """Test if dict User 'to_dict' contains the correct keys"""
        self.assertIn("id", User().to_dict())
        self.assertIn("created_at", User().to_dict())
        self.assertIn("updated_at", User().to_dict())
        self.assertIn("__class__", User().to_dict())

    def testBasemodelto_dictaddattr(self):
        """Test if dict User 'to_dict' has additional attributes"""
        usr = User()
        usr.name = "Kehinde_and_Ahmed"
        usr.number = 122
        self.assertIn("name", usr.to_dict())
        self.assertIn("number", usr.to_dict())

    def testUserto_dictdatetimeattr(self):
        """Test if dict User 'to_dict' datetime attr are string reps"""
        usrdict = User().to_dict()
        self.assertEqual(str, type(usrdict["created_at"]))
        self.assertEqual(str, type(usrdict["updated_at"]))

    def testUserto_dictoutput(self):
        """Test if output User 'to_dict' matches the expected dict"""
        currentdt = datetime.today()
        usr = User()
        usr.id = "433810"
        usr.created_at = usr.updated_at = currentdt
        exptdict = {'id': '433810', '__class__': 'User',
                    'created_at': currentdt.isoformat(),
                    'updated_at': currentdt.isoformat()}
        self.assertDictEqual(usr.to_dict(), exptdict)

    def testUserto_dictand__dict__(self):
        """Test the output of User 'to_dict' to __dict__"""
        self.assertNotEqual(User().to_dict, User().__dict__)

    def testUserto_dictargs(self):
        """Test User 'to_dict' with handling passed  arguments"""
        self.assertRaises(TypeError, lambda: User().to_dict(None))


if __name__ == "__main__":
    unittest.main()
