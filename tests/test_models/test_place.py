#!/usr/bin/python3
"""Unittest for place.py has been established"""
import time
import models
import unittest
import datetime from datetime
from os import rename, remove
import Place from models.place


class TestPlaceinstance(unittest.TestCase):
    """Unittest for instantiation of Place class instances"""

    def testPlaceinstancenoargs(self):
        """Test Place instance without any arguments"""
        self.assertEqual(type(Place()), Place)

    def testPlacenewinstancestorage(self):
        """Test instances of Place are stored in objects set"""
        self.assertIn(Place(), models.storage.all().values())

    def testPlaceidattr(self):
        """Test if 'id' attr of Place is public string"""
        self.assertEqual(str, type(Place().id))

    def testPlacecreated_atattr(self):
        """Test if 'created_at' attr of Place is pub datetime obj"""
        self.assertEqual(datetime, type(Place().created_at))

    def testPlaceupdated_atattr(self):
        """Test if 'updated_at' attr of Place is pub datetime obj"""
        self.assertEqual(datetime, type(Place().updated_at))

    def testPlacecity_idattr(self):
        """Test if 'city_id' of Place is public class attribute"""
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(Place()))
        self.assertNotIn("city_id", Place().__dict__)

    def testPlaceuser_idattr(self):
        """Test if 'user_id' of Place is public class attribute"""
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(Place()))
        self.assertNotIn("user_id", Place().__dict__)

    def testPlacenameattr(self):
        """Test if Place 'name' of Place is public class attribute"""
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(Place()))
        self.assertNotIn("name", Place().__dict__)

    def testPlacedescriptionattr(self):
        """Test if 'description' of Place is public class attribute"""
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(Place()))
        self.assertNotIn("description", Place().__dict__)

    def testPlacenumber_roomsattr(self):
        """Test if 'number_rooms' of Place is public class attribute"""
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(Place()))
        self.assertNotIn("number_rooms", Place().__dict__)

    def testPlacenumber_bathroomsattr(self):
        """Test if 'number_bathrooms' of Place is public class attribute"""
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(Place()))
        self.assertNotIn("number_bathrooms", Place().__dict__)

    def testPlacemax_guestattr(self):
        """Test if 'max_guest' of Place is public class attribute"""
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(Place()))
        self.assertNotIn("max_guest", Place().__dict__)

    def testPlaceprice_by_nightattr(self):
        """Test if 'price_by_night' of Place is public class attribute"""
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(Place()))
        self.assertNotIn("price_by_night", Place().__dict__)

    def testPlacelatitudeattr(self):
        """Test if 'latitude' of Place is public class attribute"""
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(Place()))
        self.assertNotIn("latitude", Place().__dict__)

    def testPlacelongitudeattr(self):
        """Test if 'longitude' of Place is public class attribute"""
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(Place()))
        self.assertNotIn("longitude", Place().__dict__)

    def testPlaceamenity_idsattr(self):
        """Test if 'amenity_ids' of Place is public class attribute"""
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(Place()))
        self.assertNotIn("amenity_ids", Place().__dict__)

    def testPlacetwoids(self):
        """Test that two instances Place have unique 'ids'"""
        plce1 = Place()
        plce2 = Place()
        self.assertNotEqual(plce1.id, plce2.id)

    def testPlacetwocreated_at(self):
        """Test the 'created_at' timestamp of two instances Place"""
        plce1 = Place()
        time.sleep(0.07)
        plce2 = Place()
        self.assertLess(plce1.created_at, plce2.created_at)

    def testPlacetwoupdated_at(self):
        """Test the 'updated_at' timestamp of two instances Place"""
        plce1 = Place()
        time.sleep(0.07)
        plce2 = Place()
        self.assertLess(plce1.updated_at, plce2.updated_at)

    def testPlacestrrep(self):
        """Test the string representation of a Place instance"""
        currentdt = datetime.today()
        daterepr = repr(currentdt)
        plce = Place()
        plce.id = "28557"
        plce.created_at = plce.updated_at = currentdt
        plcestr = plce.__str__()
        self.assertIn("[Place] (28557)", plcestr)
        self.assertIn("'id': '28557'", plcestr)
        self.assertIn("'created_at': " + daterepr, plcestr)
        self.assertIn("'updated_at': " + daterepr, plcestr)

    def testPlaceunusedargs(self):
        """Test that unused arguments has no impact BaseModel instances"""
        self.assertNotIn(None, Place(None).__dict__.values())

    def testPlaceinstancekwargs(self):
        """Test instantiation of Place with specified keywordargs(kwargs)"""
        currentdt = datetime.today()
        dateiso = currentdt.isoformat()
        plce = Place(id="433", created_at=dateiso, updated_at=dateiso)
        self.assertEqual(plce.id, "433")
        self.assertEqual(plce.created_at, currentdt)
        self.assertEqual(plce.updated_at, currentdt)

    def testPlaceinstanceNonekwargs(self):
        """Test instantiation Place with None as kwargs"""
        self.assertRaises(TypeError, lambda: Place(id=None,
                          created_at=None, updated_at=None))


class TestPlacesave(unittest.TestCase):
    """Unittest for the save method of the Place class"""

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

    def testPlaceonesave(self):
        """Test that Place 'save' call updates 'updated_at' timestamp"""
        plce = Place()
        time.sleep(0.06)
        frstupdated_at = plce.updated_at
        plce.save()
        self.assertLess(frstupdated_at, plce.updated_at)

    def testPlacetwosaves(self):
        """Test two Place 'save' calls updates 'updated_at' timestamps"""
        plce = Place()
        time.sleep(0.06)
        frstupdated_at = plce.updated_at
        plce.save()
        secndupdated_at = plce.updated_at
        self.assertLess(frstupdated_at, secndupdated_at)
        time.sleep(0.06)
        plce.save()
        self.assertLess(secndupdated_at, plce.updated_at)

    def testPlacesaveargs(self):
        """Test 'save' method of place call with arguments"""
        self.assertRaises(TypeError, lambda: Place().save(None))

    def testPlacesaveJSONfile(self):
        """Test 'save' method of place updates the corresponding JSON file"""
        plce = Place()
        plce.save()
        plceid = "Place." + plce.id
        with open("file.json", "r") as fl:
            self.assertIn(plceid, fl.read())


class TestPlaceto_dict(unittest.TestCase):
    """Unittest for the 'to_dict' method of the Place class"""

    def testPlaceto_dcittype(self):
        """Test if output Place 'to_dict' is a dictionary"""
        self.assertTrue(dict, type(Place().to_dict()))

    def testPlaceto_dictkeys(self):
        """Test if dict Place 'to_dict' contains the correct keys"""
        self.assertIn("id", Place().to_dict())
        self.assertIn("created_at", Place().to_dict())
        self.assertIn("updated_at", Place().to_dict())
        self.assertIn("__class__", Place().to_dict())

    def testBasemodelto_dictaddattr(self):
        """Test if dict Place 'to_dict' has additional attributes"""
        plce = Place()
        plce.name = "Kehinde_and_Ahmed"
        plce.number = 122
        self.assertIn("name", plce.to_dict())
        self.assertIn("number", plce.to_dict())

    def testPlaceto_dictdatetimeattr(self):
        """Test if dict Place 'to_dict' datetime attr are string reps"""
        plcedict = Place().to_dict()
        self.assertEqual(str, type(plcedict["created_at"]))
        self.assertEqual(str, type(plcedict["updated_at"]))

    def testPlaceto_dictoutput(self):
        """Test if output Place 'to_dict' matches the expected dict"""
        currentdt = datetime.today()
        plce = Place()
        plce.id = "433810"
        plce.created_at = plce.updated_at = currentdt
        expdict = {'id': '433810', '__class__': 'Place',
                   'created_at': currentdt.isoformat(),
                   'updated_at': currentdt.isoformat()}
        self.assertDictEqual(plce.to_dict(), expdict)

    def testPlaceto_dictand__dict__(self):
        """Test the output of Place 'to_dict' to __dict__"""
        self.assertNotEqual(Place().to_dict, Place().__dict__)

    def testPlaceto_dictargs(self):
        """Test Place 'to_dict' with handling passed  arguments"""
        self.assertRaises(TypeError, lambda: Place().to_dict(None))


if __name__ == "__main__":
    unittest.main()
