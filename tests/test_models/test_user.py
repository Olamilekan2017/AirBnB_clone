#!/usr/bin/python3
"""Unittest for user.py has been established"""
import time
import models
import unittest
from os import rename, remove
import datetime from datetime
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
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def testUsertwocreated_at(self):
        """Test the 'created_at' timestamp of two instances User"""
        user1 = User()
        time.sleep(0.07)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def testUsertwoupdated_at(self):
        """Test the 'updated_at' timestamp of two instances User"""
        user1 = User()
        time.sleep(0.07)
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def testUserstrrep(self):
        """Test the string representation of a User instance"""
        currentdt = datetime.today()
        daterepr = repr(currentdt)
        user = User()
        user.id = "28557"
        user.created_at = user.updated_at = currentdt
        userstr = user.__str__()
        self.assertIn("[User] (28557)", userstr)
        self.assertIn("'id': '28557'", userstr)
        self.assertIn("'created_at': " + daterepr, userstr)
        self.assertIn("'updated_at': " + daterepr, userstr)

    def testUserunusedargs(self):
        """Test that unused arguments has no impact BaseModel instances"""
        self.assertNotIn(None, User(None).__dict__.values())

    def testUserinstancekwargs(self):
        """Test instantiation User with specified keywordargs(kwargs)"""
        currentdt = datetime.today()
        dateiso = currentdt.isoformat()
        user = User(id="433", created_at=dateiso, updated_at=dateiso)
        self.assertEqual(user.id, "433")
        self.assertEqual(user.created_at, currentdt)
        self.assertEqual(user.updated_at, currentdt)

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
        user = User()
        time.sleep(0.08)
        frstupdated_at = user.updated_at
        user.save()
        self.assertLess(frstupdated_at, user.updated_at)

    def testUsertwosaves(self):
        """Test two User 'save' calls updates 'updated_at' timestamps"""
        user = User()
        time.sleep(0.06)
        frstupdated_at = user.updated_at
        user.save()
        secndupdated_at = user.updated_at
        self.assertLess(frstupdated_at, secndupdated_at)
        time.sleep(0.06)
        user.save()
        self.assertLess(secndupdated_at, user.updated_at)

    def testUsersaveargs(self):
        """Test 'save' method of User call with arguments"""
        self.assertRaises(TypeError, lambda: User().save(None))

    def testUsersaveJSONfile(self):
        """Test 'save' method of User updates the corresponding JSON file"""
        user = User()
        user.save()
        userid = "User." + user.id
        with open("file.json", "r") as fl:
            self.assertIn(userid, fl.read())


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
        user = User()
        user.name = "Kehinde_and_Ahmed"
        user.number = 122
        self.assertIn("name", user.to_dict())
        self.assertIn("number", user.to_dict())

    def testUserto_dictdatetimeattr(self):
        """Test if dict User 'to_dict' datetime attr are string reps"""
        userdict = User().to_dict()
        self.assertEqual(str, type(userdict["created_at"]))
        self.assertEqual(str, type(userdict["updated_at"]))

    def testUserto_dictoutput(self):
        """Test if output User 'to_dict' matches the expected dict"""
        currentdt = datetime.today()
        user = User()
        user.id = "433810"
        user.created_at = user.updated_at = currentdt
        exptdict = {'id': '433810', '__class__': 'User',
                    'created_at': currentdt.isoformat(),
                    'updated_at': currentdt.isoformat()}
        self.assertDictEqual(user.to_dict(), expdict)

    def testUserto_dictand__dict__(self):
        """Test the output of User 'to_dict' to __dict__"""
        self.assertNotEqual(User().to_dict, User().__dict__)

    def testUserto_dictargs(self):
        """Test User 'to_dict' with handling passed  arguments"""
        self.assertRaises(TypeError, lambda: User().to_dict(None))


if __name__ == "__main__":
    unittest.main()
