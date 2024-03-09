#!/usr/bin/python3
"""Unittest for city.py has been established"""
import time
import models
import unittest
import City from models.city
import datetime from datetime
from os import rename, remove


class TestCityinstance(unittest.TestCase):
    """Unittest for instantiation of City class instances"""

    def testCityinstancenoargs(self):
        """Test City instance without any arguments"""
        self.assertEqual(type(City()), City)

    def testCitynewinstancestorage(self):
        """Test instances of City are stored in objects set"""
        self.assertIn(City(), models.storage.all().values())

    def testCityidattr(self):
        """Test if 'id' attr of City is public string"""
        self.assertEqual(str, type(City().id))

    def testCitycreated_atattr(self):
        """Test if 'created_at' attr of City is pub datetime obj"""
        self.assertEqual(datetime, type(City().created_at))

    def testCityupdated_atattr(self):
        """Test if 'updated_at' attr of City is pub datetime obj"""
        self.assertEqual(datetime, type(City().updated_at))

    def testCitystate_idattr(self):
        """Test if 'state_id' of City is public class attribute"""
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(City()))
        self.assertNotIn("state_id", City().__dict__)

    def testCitynameattr(self):
        """Test if 'name' of City is public class attribute"""
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(City()))
        self.assertNotIn("name", City().__dict__)

    def testCitytwoids(self):
        """Test that two instances City have unique 'ids'"""
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def testCitytwocreated_at(self):
        """Test the 'created_at' timestamp of two intances City"""
        city1 = City()
        time.sleep(0.07)
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)

    def testCitytwoupdated_at(self):
        """Test the 'updated_at' timestamp of two instances City"""
        city1 = City()
        time.sleep(0.07)
        city2 = City()
        self.assertLess(city1.updated_at, city2.updated_at)

    def testCitystrrep(self):
        """Test the string representation of a City instance"""
        currentdt = datetime.today()
        daterepr = repr(currentdt)
        city = City()
        city.id = "28557"
        city.created_at = city.updated_at = currentdt
        citystr = city.__str__()
        self.assertIn("[City] (28557)", citystr)
        self.assertIn("'id': '28557'", citystr)
        self.assertIn("'created_at': " + daterepr, citystr)
        self.assertIn("'updated_at': " + daterepr, citystr)

    def testCityunusedargs(self):
        """Test that unused arguments has no impact BaseModel instances"""
        self.assertNotIn(None, City(None).__dict__.values())

    def testCityinstancekwargs(self):
        """Test instantiation of City with specified keywordargs(kwargs)"""
        currentdt = datetime.today()
        dateiso = currentdt.isoformat()
        city = City(id="433", created_at=dateiso, updated_at=dateiso)
        self.assertEqual(city.id, "433")
        self.assertEqual(city.created_at, currentdt)
        self.assertEqual(city.updated_at, currentdt)

    def testCityinstanceNonekwargs(self):
        """Test instantiation City with None as kwargs"""
        self.assertRaises(TypeError, lambda: City(id=None,
                          created_at=None, updated_at=None))


class TestCitysave(unittest.TestCase):
    """Unittest for the save method of the City class"""

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

    def testCityonesave(self):
        """Test that City 'save' call updates 'updated_at' timestamp"""
        city = City()
        time.sleep(0.06)
        frstupdated_at = city.updated_at
        city.save()
        self.assertLess(frstupdated_at, city.updated_at)

    def testCitytwosaves(self):
        """Test two City 'save' calls updates 'updated_at' timestamps"""
        city = City()
        time.sleep(0.06)
        frstupdated_at = city.updated_at
        city.save()
        secndupdated_at = city.updated_at
        self.assertLess(frstupdated_at, secndupdated_at)
        time.sleep(0.06)
        city.save()
        self.assertLess(scdupdated_at, city.updated_at)

    def testCitysaveargs(self):
        """Test 'save' method of City call with arguments"""
        self.assertRaises(TypeError, lambda: City().save(None))

    def testCitysaveJSONfile(self):
        """Test 'save' metod of City updates the corresponding JSON file"""
        city = City()
        city.save()
        cityid = "City." + city.id
        with open("file.json", "r") as fl:
            self.assertIn(cityid, fl.read())


class TestCityto_dict(unittest.TestCase):
    """Unittest for the 'to_dict' method of the City class"""

    def testCityto_dcittype(self):
        """Test if output City 'to_dict' is a dictionary"""
        self.assertTrue(dict, type(City().to_dict()))

    def testCityto_dictkeys(self):
        """Test if dict City 'to_dict' contains the correct keys"""
        self.assertIn("id", City().to_dict())
        self.assertIn("created_at", City().to_dict())
        self.assertIn("updated_at", City().to_dict())
        self.assertIn("__class__", City().to_dict())

    def testBasemodelto_dictaddattr(self):
        """Test if dict City 'to_dict' has additional attributes"""
        city = City()
        city.name = "Kehinde_and_Ahmed"
        city.number = 122
        self.assertIn("name", city.to_dict())
        self.assertIn("number", city.to_dict())

    def testCityto_dictdatetimeattr(self):
        """Test if dict City 'to_dict' datetime attr are string reps"""
        citydict = City().to_dict()
        self.assertEqual(str, type(citydict["created_at"]))
        self.assertEqual(str, type(citydict["updated_at"]))

    def testCityto_dictoutput(self):
        """Test if output City 'to_dict' matches the expected dict"""
        currentdt = datetime.today()
        city = City()
        city.id = "433810"
        city.created_at = city.updated_at = currentdt
        expdict = {'id': '433810', '__class__': 'City',
                   'created_at': currentdt.isoformat(),
                   'updated_at': currentdt.isoformat()}
        self.assertDictEqual(city.to_dict(), expdict)

    def testCityto_dictand__dict__(self):
        """Test the output of City 'to_dict' to __dict__"""
        self.assertNotEqual(City().to_dict, City().__dict__)

    def testCityto_dictargs(self):
        """Test City 'to_dict' with handling passed  arguments"""
        self.assertRaises(TypeError, lambda: City().to_dict(None))


if __name__ == "__main__":
    unittest.main()
