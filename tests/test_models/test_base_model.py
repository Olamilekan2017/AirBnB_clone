#!/usr/bin/python3
"""Unittest for base_model.py has been established"""
import time
import models
import unittest
from os import rename, remove
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModelinstance(unittest.TestCase):
    """Unittest for instantiation of BaseModel class instances"""

    def testBaseModelinstancenoargs(self):
        """Test: BaseModel instance without any arguments"""
        self.assertEqual(type(BaseModel()), BaseModel)

    def testBaseModelnewinstancestorage(self):
        """Test instance of BaseModel are stored in objects set"""
        self.assertIn(BaseModel(), models.storage.all().values())

    def testBaseModelidattr(self):
        """Test if 'id' attr of BaseModel is public string"""
        self.assertEqual(str, type(BaseModel().id))

    def testBaseModelcreated_atattr(self):
        """Test if 'created_at' attr of BaseModel is pub datetime obj"""
        self.assertEqual(datetime, type(BaseModel().created_at))

    def testBaseModelupdated_atattr(self):
        """Test if 'updated_at' attr of BaseModel is pub datetime obj"""
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def testBaseModeltwoids(self):
        """Test that two instances BaseModel have unique 'ids'"""
        bsmd1 = BaseModel()
        bsmd2 = BaseModel()
        self.assertNotEqual(bsmd1.id, bsmd2.id)

    def testBaseModeltwocreated_at(self):
        """Test the 'created_at' timestamp of two instances BaseModel"""
        bsmd1 = BaseModel()
        time.sleep(0.07)
        bsmd2 = BaseModel()
        self.assertLess(bsmd1.created_at, bsmd2.created_at)

    def testBaseModeltwoupdated_at(self):
        """Test the 'updated_at' timestamp of two instances BaseModel"""
        bsmd1 = BaseModel()
        time.sleep(0.07)
        bsmd2 = BaseModel()
        self.assertLess(bsmd1.updated_at, bsmd2.updated_at)

    def testBaseModelstrrep(self):
        """Test the string representation of a BaseModel instance"""
        currentdt = datetime.today()
        daterepr = repr(currentdt)
        bsmd = BaseModel()
        bsmd.id = "28557"
        bsmd.created_at = bsmd.updated_at = currentdt
        bsmdstr = bsmd.__str__()
        self.assertIn("[BaseModel] (28557)", bsmdstr)
        self.assertIn("'id': '28557'", bsmdstr)
        self.assertIn("'created_at': " + daterepr, bsmdstr)
        self.assertIn("'updated_at': " + daterepr, bsmdstr)

    def testBaseModelunusedargs(self):
        """Test that unused arguments has no impact HaseModel instances"""
        self.assertNotIn(None, BaseModel(None).__dict__.values())

    def testBaseModelinstancekwargs(self):
        """Test instantiation of BaseModel withspecified keywordargs(kwargs)"""
        currentdt = datetime.today()
        dteiso = currentdt.isoformat()
        bsmd = BaseModel(id="433", created_at=dteiso, updated_at=dteiso)
        self.assertEqual(bsmd.id, "433")
        self.assertEqual(bsmd.created_at, currentdt)
        self.assertEqual(bsmd.updated_at, currentdt)

    def testBaseModelinstanceNonekwargs(self):
        """Test instantiation BaseModel with None as kwargs"""
        self.assertRaises(TypeError, lambda: BaseModel(id=None,
                          created_at=None, updated_at=None))

    def testBaseModelinstanceargskwargs(self):
        """Test instantiation of BaseModel with positional args and kwargs"""
        currentdt = datetime.today()
        dteiso = currentdt.isoformat()
        bsmd = BaseModel("26", id="135", created_at=dteiso, updated_at=dteiso)
        self.assertEqual(bsmd.id, "135")
        self.assertEqual(bsmd.created_at, currentdt)
        self.assertEqual(bsmd.updated_at, currentdt)


class TestBaseModelsave(unittest.TestCase):
    """Unittest for the save method of the BaseModel class"""

    @classmethod
    def setUp(self):
        """SetUp environment for testing the 'save' method"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """CleanUp environment after testing the 'save' method"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testBaseModelonesave(self):
        """Test that BaseModel 'save' call updates 'updated_at' timestamp"""
        bsmd = BaseModel()
        time.sleep(0.06)
        frstupdated_at = bsmd.updated_at
        bsmd.save()
        self.assertLess(frstupdated_at, bsmd.updated_at)

    def testBaseModeltwosaves(self):
        """Test two BaseModel 'save' calls updates 'updated_at' timestamps"""
        bsmd = BaseModel()
        time.sleep(0.06)
        frstupdated_at = bsmd.updated_at
        bsmd.save()
        secndupdated_at = bsmd.updated_at
        self.assertLess(frstupdated_at, secndupdated_at)
        time.sleep(0.06)
        bsmd.save()
        self.assertLess(secndupdated_at, bsmd.updated_at)

    def testBaseModelsaveargs(self):
        """Test 'save' method of BaseModel call with arguments"""
        self.assertRaises(TypeError, lambda: BaseModel().save(None))

    def testBaseModelsaveJSONfile(self):
        """Test 'save' method of BaseModel updates corresponding JSON file"""
        bsmd = BaseModel()
        bsmd.save()
        bsmdid = "BaseModel." + bsmd.id
        with open("file.json", "r") as fl:
            self.assertIn(bsmdid, fl.read())


class TestBaseModelto_dict(unittest.TestCase):
    """Unittest for the 'to_dict' method of the BaseModel class"""

    def testBaseModelto_dcittype(self):
        """Test if output BaseModel 'to_dict' is a dictionary"""
        self.assertTrue(dict, type(BaseModel().to_dict()))

    def testBaseModelto_dictkeys(self):
        """Test if dict BaseModel 'to_dict' contains the correct keys"""
        self.assertIn("id", BaseModel().to_dict())
        self.assertIn("created_at", BaseModel().to_dict())
        self.assertIn("updated_at", BaseModel().to_dict())
        self.assertIn("__class__", BaseModel().to_dict())

    def testBasemodelto_dictaddattr(self):
        """Test if dict BaseModel 'to_dict' has additional attributes"""
        bsmd = BaseModel()
        bsmd.name = "Kehinde_and_Ahmed"
        bsmd.number = 122
        self.assertIn("name", bsmd.to_dict())
        self.assertIn("number", bsmd.to_dict())

    def testBaseModelto_dictdatetimeattr(self):
        """Test if dict BaseModel 'to_dict' datetime attr are string reps"""
        bsmddict = BaseModel().to_dict()
        self.assertEqual(str, type(bsmddict["created_at"]))
        self.assertEqual(str, type(bsmddict["updated_at"]))

    def testBaseModelto_dictoutput(self):
        """Test if output BaseModel 'to_dict' matches the expected dict"""
        currentdt = datetime.today()
        bsmd = BaseModel()
        bsmd.id = "433810"
        bsmd.created_at = bsmd.updated_at = currentdt
        exptdict = {'id': '433810', '__class__': 'BaseModel',
                    'created_at': currentdt.isoformat(),
                    'updated_at': currentdt.isoformat()}
        self.assertDictEqual(bsmd.to_dict(), exptdict)

    def testBaseModelto_dictand__dict__(self):
        """Test the output of BaseModel 'to_dict' to __dict__"""
        self.assertNotEqual(BaseModel().to_dict, BaseModel().__dict__)

    def testBaseModelto_dictargs(self):
        """Test BaseModel 'to_dict' with handling passed  arguments"""
        self.assertRaises(TypeError, lambda: BaseModel().to_dict(None))


if __name__ == "__main__":
    unittest.main()
