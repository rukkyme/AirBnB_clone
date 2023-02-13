#!/usr/bin/python3
from models.base_model import BaseModel
import unittest
import json
import os
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.storage = FileStorage()
        return super().setUp()

    def tearDown(self) -> None:
        FileStorage._FileStorage__objects = {}
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        return super().tearDown()


class TestAll(TestFileStorage):
    def test_no_objects(self):
        self.tearDown()
        obj = self.storage.all()
        self.assertIsInstance(obj, dict)
        self.assertEqual(obj, {})

    def test_non_empty_objects(self):
        self.tearDown()
        newobj = BaseModel()
        key = f"{newobj.__class__.__name__}.{newobj.id}"
        obj = self.storage.all()
        self.assertIs(newobj, obj[key])


class TestNew(TestFileStorage):
    def test_new_with_valid_object(self):
        objects = self.storage.all()
        newobj = BaseModel()
        key = f"{newobj.__class__.__name__}.{newobj.id}"
        self.storage.new(newobj)
        self.assertIs(objects[key], newobj)

    def test_new_with_invalid_object(self):
        with self.assertRaises(AttributeError):
            self.s.new(str())


class TestSave(TestFileStorage):
    def test_save_non_empty_object(self):
        newobj = BaseModel()
        self.storage.new(newobj)
        self.storage.save()
        __objects = self.storage.all()
        filename = "file.json"
        self.assertTrue(os.path.isfile(filename))
        objects = {key: obj.to_dict() for key, obj in __objects.items()}
        with open(filename) as f:
            fromjsonstr = json.load(f)
            self.assertEqual(fromjsonstr, objects)
        os.remove(filename)

    def test_save_empty_object(self):

        self.storage.save()
        __objects = self.storage.all()
        filename = "file.json"
        self.assertTrue(os.path.isfile(filename))
        objects = {key: obj.to_dict() for key, obj in __objects.items()}
        with open(filename) as f:
            fromjsonstr = json.load(f)
            self.assertEqual(fromjsonstr, objects)
        os.remove(filename)


class TestReload(TestFileStorage):

    def test_correct_obj_reload(self):
        newobj = BaseModel()
        key = f"{newobj.__class__.__name__}.{newobj.id}"
        self.storage.new(newobj)
        self.storage.save()
        self.storage.reload()
        objects = self.storage.all()
        self.assertEqual(str(objects[key]), str(newobj))

    def test_valid_file_content(self):

        newobj = BaseModel()
        self.storage.new(newobj)
        self.storage.save()
        self.storage.reload()
        objects = self.storage.all()
        self.assertTrue(objects)
        self.assertEqual(len(objects), 1)
        self.assertIsInstance(objects, dict)

    def test_invalid_file_content(self):
        with open("file.json", 'w') as f:
            print("x", file=f)
        store = FileStorage()

        with self.assertRaises(json.decoder.JSONDecodeError):
            store.reload()


if __name__ == '__main__':
    unittest.main()
