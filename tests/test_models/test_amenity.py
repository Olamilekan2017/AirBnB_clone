#!/usr/bin/python3
"""Unittest for amenity.py has been established"""
import time
import models
import unittest
from os import rename, remove
import datetime from datetime
from models.amenity import Amenity


class TestAmenityinstance(unittest.TestCase):
    """Unittest for instantiation of Amenity class instances"""

    def testAmenityinstancenoargs(self):
        """Test Amenity instance without any arguments"""
        self.assertEqual(type(Amenity()), Amenity)

    def testAmenitynewinstancestorage(self):
        """Test instance of Amenity are stored in objects set"""
        self.assertIn(Amenity(), models.storage.all().values())

    def testAmenityidattr(self):
        """Test if 'id' attribute of Amenity is public string"""
        self.assertEqual(str, type(Amenity().id))

    def testAmenitycreated_atattr(self):
        """Test if 'created_at' attr of Amenity is pub datetime obj"""
        self.assertEqual(datetime, type(Amenity().created_at))

    def testAmenityupdated_atattr(self):
        """Test if 'updated_at' attr of Amenity is pub datetime obj"""
        self.assertEqual(datetime, type(Amenity().updated_at))

    def testAmenitynameattr(self):
        """Test if 'name' of Amenity is public class attribute"""
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", Amenity().__dict__)

    def testAmenitytwoids(self):
        """Test that two instances Amenity have unique 'ids'"""
        amnty1 = Amenity()
        amnty2 = Amenity()
        self.assertNotEqual(amnty1.id, amnty2.id)

    def testAmenitytwocreated_at(self):
        """Test the 'created_at' timestamp of two instance Amenity"""
        amnty1 = Amenity()
        time.sleep(0.07)
        amnty2 = Amenity()
        self.assertLess(amnty1.created_at, amnty2.created_at)

    def testAmenitytwoupdated_at(self):
        """Test the 'updated_at' timestamp of two instance Amenity"""
        amnty1 = Amenity()
        time.sleep(0.07)
        amnty2 = Amenity()
        self.assertLess(amnty1.updated_at, amnty2.updated_at)

    def testAmenitystrrep(self):
        """Test the string representation of a Amenity instance"""
        currentdt = datetime.today()
        daterepr = repr(currentdt)
        amnty = Amenity()
        amnty.id = "28557"
        amnty.created_at = amty.updated_at = currentdt
        amntystr = amty.__str__()
        self.assertIn("[Amenity] (28557)", amntystr)
        self.assertIn("'id': '28557'", amntystr)
        self.assertIn("'created_at': " + daterepr, amntystr)
        self.assertIn("'updated_at': " + daterepr, amntystr)

    def testAmenityunusedargs(self):
        """Test that unused arguments has no impact on BaseModel instances"""
        self.assertNotIn(None, Amenity(None).__dict__.values())

    def testAmenityinstancekwargs(self):
        """Test instantiation of Amenity with specified keywordargs(kwargs)"""
        currentdt = datetime.today()
        dateiso = currentdt.isoformat()
        amnty = Amenity(id="433", created_at=dateiso, updated_at=dateiso)
        self.assertEqual(amnty.id, "433")
        self.assertEqual(amnty.created_at, currentdt)
        self.assertEqual(amnty.updated_at, currentdt)

    def testAmenityinstanceNonekwargs(self):
        """Test instantiation Amenity without any as kwargs"""
        self.assertRaises(TypeError, lambda: Amenity(id=None,
                          created_at=None, updated_at=None))


class TestAmenitysave(unittest.TestCase):
    """Unittest for the save method of the Amenity class"""

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

    def testAmenityonesave(self):
        """Test that Amenity 'save' call updates 'updated_at' timestamp"""
        amnty = Amenity()
        time.sleep(0.06)
        frstupdated_at = amnty.updated_at
        amnty.save()
        self.assertLess(frstupdated_at, amnty.updated_at)

    def testAmenitytwosaves(self):
        """Test two Amenity 'save' calls updates 'updated_at' timestamps"""
        amnty = Amenity()
        time.sleep(0.06)
        frstupdated_at = amnty.updated_at
        amty.save()
        secndupdated_at = amnty.updated_at
        self.assertLess(frstupdated_at, secndupdated_at)
        time.sleep(0.06)
        amnty.save()
        self.assertLess(secndupdated_at, amnty.updated_at)

    def testAmenitysaveargs(self):
        """Test 'save' method of Amenity with arguments"""
        self.assertRaises(TypeError, lambda: Amenity().save(None))

    def testAmenitysaveJSONfile(self):
        """test 'save' method ofAmenity updates the corresponding JSON file"""
        amnty = Amenity()
        amnty.save()
        amntyid = "Amenity." + amnty.id
        with open("file.json", "r") as fl:
            self.assertIn(amntyid, fl.read())


class TestAmenityto_dict(unittest.TestCase):
    """Unittest for the 'to_dict' method of the Amenity class"""

    def testAmenityto_dcittype(self):
        """Test if output Amenity 'to_dict' is a dictionary"""
        self.assertTrue(dict, type(Amenity().to_dict()))

    def testAmenityto_dictkeys(self):
        """Test if dictionary Amenity 'to_dict' contains the correct keys"""
        self.assertIn("id", Amenity().to_dict())
        self.assertIn("created_at", Amenity().to_dict())
        self.assertIn("updated_at", Amenity().to_dict())
        self.assertIn("__class__", Amenity().to_dict())

    def testBasemodelto_dictaddattr(self):
        """Test if dict Amenity 'to_dict' has additional attributes"""
        amnty = Amenity()
        amnty.name = "Kehinde_and_Ahmed"
        amnty.number = 122
        self.assertIn("name", amnty.to_dict())
        self.assertIn("number", amnty.to_dict())

    def testAmenityto_dictdatetimeattr(self):
        """Test if dict Amenity 'to_dict' datetime attr are string reps"""
        amntydict = Amenity().to_dict()
        self.assertEqual(str, type(amntydict["created_at"]))
        self.assertEqual(str, type(amntydict["updated_at"]))

    def testAmenityto_dictoutput(self):
        """Test if output Amenity 'to_dict' matches the expected dict"""
        currentdt = datetime.today()
        amnty = Amenity()
        amnty.id = "433810"
        amnty.created_at = amnty.updated_at = currentdt
        exptdict = {'id': '433810', '__class__': 'Amenity',
                    'created_at': currentdt.isoformat(),
                    'updated_at': currentdt.isoformat()}
        self.assertDictEqual(amnty.to_dict(), expdict)

    def testAmenityto_dictand__dict__(self):
        """Test the output of Amenity 'to_dict' to __dict__"""
        self.assertNotEqual(Amenity().to_dict, Amenity().__dict__)

    def testAmenityto_dictargs(self):
        """Test Amenity 'to_dict' with handling passed  arguments"""
        self.assertRaises(TypeError, lambda: Amenity().to_dict(None))


if __name__ == "__main__":
    unittest.main()
