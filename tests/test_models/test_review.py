#!/usr/bin/python3
"""Unittest for review.py has been established"""
import time
import models
import unittest
from os import rename, remove
import datetime from datetime
from models.review import Review


class TestReviewinstance(unittest.TestCase):
    """Unittest instantiation of Review class instances"""

    def testReviewinstancenoargs(self):
        """Test Review instance without any arguments"""
        self.assertEqual(type(Review()), Review)

    def testReviewnewinstancestorage(self):
        """Test instances of Review are stored in objects set"""
        self.assertIn(Review(), models.storage.all().values())

    def testReviewidattr(self):
        """Test if 'id' attr of Review is public string"""
        self.assertEqual(str, type(Review().id))

    def testReviewcreated_atattr(self):
        """Test if 'created_at' attr of Review is pub datetime obj"""
        self.assertEqual(datetime, type(Review().created_at))

    def testReviewupdated_atattr(self):
        """Test if 'updated_at' attr of Review is pub datetime obj"""
        self.assertEqual(datetime, type(Review().updated_at))

    def testReviewplace_idattr(self):
        """Test if 'place_id' of Review is public class attribute"""
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(Review()))
        self.assertNotIn("place_id", Review().__dict__)

    def testReviewuser_idattr(self):
        """Test if 'user_id' of Review is public class attribute"""
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(Review()))
        self.assertNotIn("user_id", Review().__dict__)

    def testReviewtextattr(self):
        """Test if 'text' of Review is public class attribute"""
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(Review()))
        self.assertNotIn("text", Review().__dict__)

    def testReviewtwoids(self):
        """Test that two Review instances have unique 'ids'"""
        revw1 = Review()
        revw2 = Review()
        self.assertNotEqual(revw1.id, revw2.id)

    def testReviewtwocreated_at(self):
        """Test the 'created_at' timestamp of two instances Review"""
        revw1 = Review()
        time.sleep(0.07)
        revw2 = Review()
        self.assertLess(revw1.created_at, revw2.created_at)

    def testReviewtwoupdated_at(self):
        """Test the 'updated_at' timestamp of two instances Review"""
        revw1 = Review()
        time.sleep(0.07)
        revw2 = Review()
        self.assertLess(revw1.updated_at, revw2.updated_at)

    def testReviewstrrep(self):
        """Test the string representation of a Review instance"""
        currentdt = datetime.today()
        daterepr = repr(currentdt)
        revw = Review()
        revw.id = "28557"
        revw.created_at = revw.updated_at = currentdt
        revwstr = revw.__str__()
        self.assertIn("[Review] (28557)", revwstr)
        self.assertIn("'id': '28557'", revwstr)
        self.assertIn("'created_at': " + daterepr, revwstr)
        self.assertIn("'updated_at': " + daterepr, revwstr)

    def testReviewunusedargs(self):
        """Test that unused arguments has no impact BaseModel instances"""
        self.assertNotIn(None, Review(None).__dict__.values())

    def testReviewinstancekwargs(self):
        """Test instantiation of Review with specified keywordargs(kwargs)"""
        currentdt = datetime.today()
        dateiso = currentdt.isoformat()
        revw = Review(id="433", created_at=dateiso, updated_at=dateiso)
        self.assertEqual(revw.id, "433")
        self.assertEqual(revw.created_at, currentdt)
        self.assertEqual(revw.updated_at, currentdt)

    def testReviewinstanceNonekwargs(self):
        """Test instantiation Review with None as kwargs"""
        self.assertRaises(TypeError, lambda: Review(id=None,
                          created_at=None, updated_at=None))


class TestReviewsave(unittest.TestCase):
    """Unittest for the save method of the Review class"""

    @classmethod
    def setUp(self):
        """SetUp environment for testing the 'save' method tests"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """Cleanup environment after testing the 'save' method tests"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass

    def testReviewonesave(self):
        """Test that Review 'save' call updates 'updated_at' timestamp"""
        revw = Review()
        time.sleep(0.06)
        frstupdated_at = revw.updated_at
        revw.save()
        self.assertLess(frstupdated_at, revw.updated_at)

    def testReviewtwosaves(self):
        """Test two Review 'save' calls updates 'updated_at' timestamps"""
        revw = Review()
        time.sleep(0.06)
        frstupdated_at = revw.updated_at
        revw.save()
        secndupdated_at = revw.updated_at
        self.assertLess(frstupdated_at, secndupdated_at)
        time.sleep(0.06)
        revw.save()
        self.assertLess(secndupdated_at, revw.updated_at)

    def testReviewsaveargs(self):
        """Test 'save' method of Review call with arguments"""
        self.assertRaises(TypeError, lambda: Review().save(None))

    def testReviewsaveJSONfile(self):
        """Test 'save' method of Review updates the corresponding JSON file"""
        revw = Review()
        revw.save()
        revwid = "Review." + revw.id
        with open("file.json", "r") as fl:
            self.assertIn(revwid, fl.read())


class TestReviewto_dict(unittest.TestCase):
    """Unittest for the 'to_dict' method of the Review class"""

    def testReviewto_dcittype(self):
        """Test if output Review 'to_dict' is a dictionary"""
        self.assertTrue(dict, type(Review().to_dict()))

    def testReviewto_dictkeys(self):
        """Test if dict Review 'to_dict' contains the correct keys"""
        self.assertIn("id", Review().to_dict())
        self.assertIn("created_at", Review().to_dict())
        self.assertIn("updated_at", Review().to_dict())
        self.assertIn("__class__", Review().to_dict())

    def testBasemodelto_dictaddattr(self):
        """Test if dict Review 'to_dict' has additional attributes"""
        revw = Review()
        revw.name = "Kehinde_and_Ahmed"
        revw.number = 122
        self.assertIn("name", revw.to_dict())
        self.assertIn("number", revw.to_dict())

    def testReviewto_dictdatetimeattr(self):
        """Test if dict Review 'to_dict' datetime attr are string reps"""
        dictrevw = Review().to_dict()
        self.assertEqual(str, type(dictrevw["created_at"]))
        self.assertEqual(str, type(dictrevw["updated_at"]))

    def testReviewto_dictoutput(self):
        """Test if output Review 'to_dict' matches the expected dict"""
        currentdt = datetime.today()
        revw = Review()
        revw.id = "433810"
        revw.created_at = revw.updated_at = currentdt
        exptdict = {'id': '433810', '__class__': 'Review',
                    'created_at': currentdt.isoformat(),
                    'updated_at': currentdt.isoformat()}
        self.assertDictEqual(revw.to_dict(), expdict)

    def testReviewto_dictand__dict__(self):
        """Test the output of Review 'to_dict' to __dict__"""
        self.assertNotEqual(Review().to_dict, Review().__dict__)

    def testReviewto_dictargs(self):
        """Test Review 'to_dict' with handling passed  arguments"""
        self.assertRaises(TypeError, lambda: Review().to_dict(None))


if __name__ == "__main__":
    unittest.main()
