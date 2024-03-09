#!/usr/bin/python3
"""Unittest for state.py has been established"""
import time
import models
import unittest
import datetime from datetime
from os import rename, remove
from models.state import State


class TestStateinstance(unittest.TestCase):
    """Unittest for instantiation of State class instances"""

    def testStateinstancenoargs(self):
        """Test instance of State without any arguments"""
        self.assertEqual(type(State()), State)

    def testStatenewinstancestorage(self):
        """Test instances of State are stored in objects set"""
        self.assertIn(State(), models.storage.all().values())

    def testStateidattr(self):
        """Test if 'id' attr of State is public string"""
        self.assertEqual(str, type(State().id))

    def testStatecreated_atattr(self):
        """Test if 'created_at' attr of State is pub datetime obj"""
        self.assertEqual(datetime, type(State().created_at))

    def testStateupdated_atattr(self):
        """Test if 'updated_at' attr of State is pub datetime obj"""
        self.assertEqual(datetime, type(State().updated_at))

    def testStatenameattr(self):
        """Test if 'name' of State is public class attribute"""
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(State()))
        self.assertNotIn("name", State().__dict__)

    def testStatetwoids(self):
        """Test that two instances State have unique 'ids'"""
        stt1 = State()
        stt2 = State()
        self.assertNotEqual(stt1.id, stt2.id)

    def testStatetwocreated_at(self):
        """Test the 'created_at' timestamp of two instances State"""
        stt1 = State()
        time.sleep(0.07)
        stt2 = State()
        self.assertLess(stt1.created_at, stt2.created_at)

    def testStatetwoupdated_at(self):
        """Test the 'updated_at' timestamp of two instances State"""
        stt1 = State()
        time.sleep(0.07)
        stt2 = State()
        self.assertLess(stt1.updated_at, stt2.updated_at)

    def testStatestrrep(self):
        """Test the string representation of a State instance"""
        currentdt = datetime.today()
        daterepr = repr(currentdt)
        stt = State()
        stt.id = "28557"
        stt.created_at = stt.updated_at = currentdt
        sttstr = stt.__str__()
        self.assertIn("[State] (28557)", sttstr)
        self.assertIn("'id': '28557'", sttstr)
        self.assertIn("'created_at': " + daterepr, sttstr)
        self.assertIn("'updated_at': " + daterepr, sttstr)

    def testStateunusedargs(self):
        """Test that unused arguments has no impact BaseModel instances"""
        self.assertNotIn(None, State(None).__dict__.values())

    def testStateinstancekwargs(self):
        """Test instantiation State with specified keywordargs(kwargs)"""
        currentdt = datetime.today()
        dateiso = currentdt.isoformat()
        stt = State(id="433", created_at=dateiso, updated_at=dateiso)
        self.assertEqual(stt.id, "433")
        self.assertEqual(stt.created_at, currentdt)
        self.assertEqual(stt.updated_at, currentdt)

    def testStateinstanceNonekwargs(self):
        """Test instantiation State with None as kwargs"""
        self.assertRaises(TypeError, lambda: State(id=None,
                          created_at=None, updated_at=None))


class TestStatesave(unittest.TestCase):
    """Unittest for the save method of the State class"""

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

    def testStateonesave(self):
        """Test that State 'save' call updates 'updated_at' timestamp"""
        stt = State()
        time.sleep(0.06)
        frstupdated_at = stt.updated_at
        stt.save()
        self.assertLess(frstupdated_at, stt.updated_at)

    def testStatetwosaves(self):
        """Test two State 'save' calls updates 'updated_at' timestamps"""
        stt = State()
        time.sleep(0.06)
        frstupdated_at = stt.updated_at
        stt.save()
        secndupdated_at = stt.updated_at
        self.assertLess(frstupdated_at, secndupdated_at)
        time.sleep(0.06)
        stt.save()
        self.assertLess(secndupdated_at, stt.updated_at)

    def testStatesaveargs(self):
        """Test 'save' method of state call with arguments"""
        self.assertRaises(TypeError, lambda: State().save(None))

    def testStatesaveJSONfile(self):
        """Test 'save' method of State updates the corresponding JSON file"""
        stt = State()
        stt.save()
        sttid = "State." + stt.id
        with open("file.json", "r") as fl:
            self.assertIn(sttid, fl.read())


class TestStateto_dict(unittest.TestCase):
    """Unittest for the 'to_dict' method of the State class"""

    def testStateto_dcittype(self):
        """Test if output State 'to_dict' is a dictionary"""
        self.assertTrue(dict, type(State().to_dict()))

    def testStateto_dictkeys(self):
        """Test if dict State 'to_dict' contains the correct keys"""
        self.assertIn("id", State().to_dict())
        self.assertIn("created_at", State().to_dict())
        self.assertIn("updated_at", State().to_dict())
        self.assertIn("__class__", State().to_dict())

    def testBasemodelto_dictaddattr(self):
        """Test if dict State 'to_dict' has additional attributes"""
        stt = State()
        stt.name = "Kehinde_and_Ahmed"
        stt.number = 122
        self.assertIn("name", stt.to_dict())
        self.assertIn("number", stt.to_dict())

    def testStateto_dictdatetimeattr(self):
        """Test if dict State 'to_dict' datetime attr are string reps"""
        sttdict = State().to_dict()
        self.assertEqual(str, type(sttdict["created_at"]))
        self.assertEqual(str, type(sttdict["updated_at"]))

    def testStateto_dictoutput(self):
        """Test if output State 'to_dict' matches the expected dict"""
        currentdt = datetime.today()
        stt = State()
        stt.id = "433810"
        stt.created_at = stt.updated_at = currentdt
        exptdict = {'id': '433810', '__class__': 'State',
                    'created_at': currentdt.isoformat(),
                    'updated_at': currentdt.isoformat()}
        self.assertDictEqual(stt.to_dict(), expdict)

    def testStateto_dictand__dict__(self):
        """Test the output of State 'to_dict' to __dict__"""
        self.assertNotEqual(State().to_dict, State().__dict__)

    def testStateto_dictargs(self):
        """Test State 'to_dict' with handling passed  arguments"""
        self.assertRaises(TypeError, lambda: State().to_dict(None))


if __name__ == "__main__":
    unittest.main()
