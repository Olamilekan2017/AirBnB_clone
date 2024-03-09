#!/usr/bin/python3
"""Unittest for file_storage.py has been established"""
import unittest
import models
import datetime from datetime
from os import rename, remove


class TestFileStorageinstance(unittest.TestCase):
    """Unittests for intantiation of FileStorage class instances"""

    def testFileStorageinstancenoargs(self):
        """Test FileStorage instance without any arguments"""
        self.assertEqual(type(models.FileStorage()), models.FileStorage)

    def testFileStorageinstanceargs(self):
        """Test FileStorage instance with arguments"""
        self.assertRaises(TypeError, lambda: models.FileStorage(None))

    def testFileStorage__file_pathattr(self):
        """Test __file_path attr FileStorage is private string"""
        self.assertEqual(str, type(models.FileStorage._FileStorage__file_path))

    def testFileStorage__objectsattr(self):
        """Test __objects attr FileStorage is private dict"""
        self.assertEqual(dict, type(models.FileStorage._FileStorage__objects))

    def testFileStorage_storageinitialize(self):
        """Test FileStorage storage attr initialize as Filestorage inst"""
        self.assertEqual(type(models.storage), models.FileStorage)


class TestFileStoragemethods(unittest.TestCase):
    """Unittest for FileStorage methods"""

    @classmethod
    def setUp(self):
        """SetUp environment for testing the 'methods'"""
        try:
            rename("file.json", "tmpfile")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """Clean up environment after testing the 'methods'"""
        try:
            remove("file.json")
        except IOError:
            pass
        try:
            rename("tmpfile", "file.json")
        except IOError:
            pass
        models.FileStorage._FileStorage__objects = {}

    def testallmethods(self):
        """Test 'all methods' returns a dict"""
        self.assertEqual(dict, type(models.storage.all()))

    def testallmethodsargs(self):
        """Test 'all methods' with one argument more arguments"""
        self.assertRaises(TypeError, lambda: models.storage.all(None))

    def testnewmethods(self):
        """Test that 'new method' generates instances and adds to storage"""
        instances = {
            "BaseModel": models.base_model.BaseModel(),
            "User": models.user.User(),
            "State": models.state.State(),
            "City": models.city.City(),
            "Amenity": models.amenity.Amenity(),
            "Place": models.place.Place(),
            "Review": models.review.Review()
        }
        for classnm, instance in instances.items():
            models.storage.new(instance)
            key = f"{classnm}.{instance.id}"
            self.assertIn(key, models.storage.all().keys())
            self.assertIn(instance, models.storage.all().values())

    def testnewmethodsargs(self):
        """Test the 'new method' with arguments"""
        instance = {"BaseModel": models.base_model.BaseModel()}
        self.assertRaises(TypeError, lambda: models.storage.new(instance, 1))

    def testsavemethods(self):
        """Test that 'save method' stores storage of instances in file"""
        instances = {
            "BaseModel": models.base_model.BaseModel(),
            "User": models.user.User(),
            "State": models.state.State(),
            "City": models.city.City(),
            "Amenity": models.amenity.Amenity(),
            "Place": models.place.Place(),
            "Review": models.review.Review()
        }
        for classnm, instance in instances.items():
            models.storage.new(instance)
        models.storage.save()
        with open("file.json", "r") as fl:
            savetxt = fl.read()
            for classnm, instance in instances.items():
                key = f"{classnm}.{instance.id}"
                self.assertIn(key, savetxt)

    def testsavemethodsargs(self):
        """Test the 'save method' with arguments"""
        self.assertRaises(TypeError, lambda: models.storage.save(None))

    def testreloadmethods(self):
        """Test that 'reload methods' reloads storage and contains objs"""
        instances = {
            "BaseModel": models.base_model.BaseModel(),
            "User": models.user.User(),
            "State": models.state.State(),
            "City": models.city.City(),
            "Amenity": models.amenity.Amenity(),
            "Place": models.place.Place(),
            "Review": models.review.Review()
        }
        for classnm, instance in instances.items():
            models.storage.new(instance)
        models.storage.save()
        models.storage.reload()
        objs = models.FileStorage._FileStorage__objects
        for classnm, instance in instances.items():
            key = f"{classnm}.{instance.id}"
            self.assertIn(key, objs)

    def testreloadmethodsargs(self):
        """Test the 'reload methods' with arguments"""
        self.assertRaises(TypeError, lambda: models.storage.reload(None))


if __name__ == "__main__":
    unittest.main()
