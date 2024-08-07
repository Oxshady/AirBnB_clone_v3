#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models import storage
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest

FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test that get retrieves the correct object"""
        state = State(name="Texas")
        storage.new(state)
        storage.save()
        retrieved = storage.get(State, state.id)
        self.assertEqual(state, retrieved)
        self.assertIsNone(storage.get(State, "invalid_id"))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Test that count returns the correct number of objects"""
        i = storage.count()
        state = State(name="Florida")
        storage.new(state)
        storage.save()
        self.assertEqual(storage.count(), i + 1)
        self.assertEqual(storage.count(State), 1)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_delete(self):
        """Test that delete removes an object from FileStorage.__objects"""
        storage = FileStorage()
        instance = State(name="Test State")
        storage.new(instance)
        storage.save()
        self.assertIn(instance.id, storage.all(State))
        storage.delete(instance)
        storage.save()
        self.assertNotIn(instance.id, storage.all(State))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save_empty_state(self):
        """Test saving an empty FileStorage"""
        storage = FileStorage()
        storage.save()
        self.assertTrue(os.path.isfile("file.json"))
        with open("file.json", "r") as f:
            self.assertEqual(f.read(), '{}')

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new_with_duplicate_id(self):
        """Test that adding a new object with duplicate ID updates the object"""
        storage = FileStorage()
        instance1 = State(name="State1")
        storage.new(instance1)
        storage.save()
        instance2 = State(id=instance1.id, name="State2")
        storage.new(instance2)
        storage.save()
        self.assertEqual(storage.get(State, instance1.id).name, "State2")

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new_without_id(self):
        """Test that new handles objects without IDs properly"""
        storage = FileStorage()
        instance = State(name="StateWithoutID")
        storage.new(instance)
        storage.save()
        self.assertIn(instance.id, storage.all(State))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save_after_delete(self):
        """Test that save correctly updates file.json after object deletion"""
        storage = FileStorage()
        instance = State(name="TempState")
        storage.new(instance)
        storage.save()
        storage.delete(instance)
        storage.save()
        with open("file.json", "r") as f:
            content = json.load(f)
        self.assertNotIn(instance.id, content)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_empty(self):
        """Test that all returns an empty dictionary when no objects are added"""
        storage = FileStorage()
        self.assertEqual(storage.all(), {})

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save_multiple_objects(self):
        """Test saving multiple objects and verifying they are saved"""
        storage = FileStorage()
        instances = [State(name=f"State{i}") for i in range(10)]
        for instance in instances:
            storage.new(instance)
        storage.save()
        with open("file.json", "r") as f:
            content = json.load(f)
        self.assertEqual(len(content), len(instances))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save_large_data(self):
        """Test saving a large amount of data"""
        storage = FileStorage()
        large_data = {f"State.{i}": State(name=f"State{i}") for i in range(1000)}
        for key, instance in large_data.items():
            storage.new(instance)
        storage.save()
        with open("file.json", "r") as f:
            content = json.load(f)
        self.assertEqual(len(content), len(large_data))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_non_existent_class(self):
        """Test that get returns None for non-existent class"""
        self.assertIsNone(storage.get("NonExistentClass", "id"))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_non_existent_class(self):
        """Test that count returns 0 for non-existent class"""
        self.assertEqual(storage.count("NonExistentClass"), 0)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_delete_non_existent(self):
        """Test that delete on non-existent object does nothing"""
        storage = FileStorage()
        instance = State(id="nonexistent")
        storage.delete(instance)
        storage.save()
        self.assertNotIn("nonexistent", storage.all(State))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new_empty_instance(self):
        """Test that new handles empty instances properly"""
        storage = FileStorage()
        instance = State()
        storage.new(instance)
        storage.save()
        self.assertIn(instance.id, storage.all(State))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save_with_invalid_data(self):
        """Test that save handles invalid data gracefully"""
        storage = FileStorage()
        storage._FileStorage__objects = {"invalid_key": None}
        with self.assertRaises(TypeError):
            storage.save()

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_with_filter(self):
        """Test that all can filter objects by class"""
        storage = FileStorage()
        instance1 = State(name="State1")
        instance2 = City(name="City1")
        storage.new(instance1)
        storage.new(instance2)
        storage.save()
        all_states = storage.all(State)
        self.assertIn(instance1.id, all_states)
        self.assertNotIn(instance2.id, all_states)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new_and_save_same_instance(self):
        """Test that new and save for the same instance work properly"""
        storage = FileStorage()
        instance = State(name="State1")
        storage.new(instance)
        storage.save()
        instance.name = "UpdatedState"
        storage.save()
        updated_instance = storage.get(State, instance.id)
        self.assertEqual(updated_instance.name, "UpdatedState")

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save_empty_objects(self):
        """Test saving an empty objects dictionary"""
        storage = FileStorage()
        storage._FileStorage__objects = {}
        storage.save()
        with open("file.json", "r") as f:
            content = json.load(f)
        self.assertEqual(content, {})

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_multiple(self):
        """Test that get retrieves multiple instances correctly"""
        states = [State(name=f"State{i}") for i in range(5)]
        for state in states:
            storage.new(state)
        storage.save()
        for state in states:
            self.assertEqual(storage.get(State, state.id), state)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_with_filter(self):
        """Test that count returns correct number with filter"""
        states = [State(name=f"State{i}") for i in range(5)]
        for state in states:
            storage.new(state)
        storage.save()
        self.assertEqual(storage.count(State), 5)
        self.assertEqual(storage.count(City), 0)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_delete_non_existent_key(self):
        """Test delete method with a non-existent key"""
        storage = FileStorage()
        storage.delete(State(id="nonexistent"))
        storage.save()
        with open("file.json", "r") as f:
            content = json.load(f)
        self.assertNotIn("nonexistent", content)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_without_args(self):
        """Test get method without passing arguments"""
        with self.assertRaises(TypeError):
            storage.get()

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save_empty_file(self):
        """Test saving an empty file"""
        storage = FileStorage()
        storage.save()
        self.assertTrue(os.path.getsize("file.json") > 0)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_with_non_existent_class(self):
        """Test all method with non-existent class"""
        self.assertEqual(storage.all("NonExistentClass"), {})

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_large_data(self):
        """Test count with a large number of objects"""
        storage = FileStorage()
        for i in range(1000):
            instance = State(name=f"State{i}")
            storage.new(instance)
        storage.save()
        self.assertEqual(storage.count(), 1000)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save_large_data(self):
        """Test saving a large number of objects"""
        storage = FileStorage()
        for i in range(1000):
            instance = State(name=f"State{i}")
            storage.new(instance)
        storage.save()
        with open("file.json", "r") as f:
            content = json.load(f)
        self.assertEqual(len(content), 1000)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_large_data(self):
        """Test get method with a large number of objects"""
        states = [State(name=f"State{i}") for i in range(1000)]
        for state in states:
            storage.new(state)
        storage.save()
        for state in states:
            self.assertEqual(storage.get(State, state.id), state)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_delete_large_data(self):
        """Test delete method with a large number of objects"""
        states = [State(name=f"State{i}") for i in range(1000)]
        for state in states:
            storage.new(state)
        storage.save()
        for state in states:
            storage.delete(state)
        storage.save()
        with open("file.json", "r") as f:
            content = json.load(f)
        self.assertEqual(len(content), 0)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_empty_storage(self):
        """Test count with empty storage"""
        storage = FileStorage()
        self.assertEqual(storage.count(), 0)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save_after_multiple_deletes(self):
        """Test save after multiple deletes"""
        storage = FileStorage()
        instances = [State(name=f"State{i}") for i in range(10)]
        for instance in instances:
            storage.new(instance)
        storage.save()
        for instance in instances:
            storage.delete(instance)
        storage.save()
        with open("file.json", "r") as f:
            content = json.load(f)
        self.assertEqual(len(content), 0)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_after_delete(self):
        """Test get method after object deletion"""
        storage = FileStorage()
        instance = State(name="TestState")
        storage.new(instance)
        storage.save()
        storage.delete(instance)
        storage.save()
        self.assertIsNone(storage.get(State, instance.id))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save_after_error(self):
        """Test saving after encountering an error"""
        storage = FileStorage()
        storage._FileStorage__objects = {"invalid_key": None}
        with self.assertRaises(TypeError):
            storage.save()
        storage._FileStorage__objects = {}
        storage.save()
        self.assertTrue(os.path.getsize("file.json") > 0)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_after_save(self):
        """Test count after saving objects"""
        storage = FileStorage()
        instances = [State(name=f"State{i}") for i in range(10)]
        for instance in instances:
            storage.new(instance)
        storage.save()
        self.assertEqual(storage.count(), 10)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_delete_empty_storage(self):
        """Test delete method with empty storage"""
        storage = FileStorage()
        storage.delete(State(id="nonexistent"))
        storage.save()
        self.assertEqual(len(storage.all(State)), 0)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_empty_storage(self):
        """Test get method with empty storage"""
        self.assertIsNone(storage.get(State, "nonexistent"))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save_after_update(self):
        """Test save after updating an object"""
        storage = FileStorage()
        instance = State(name="InitialName")
        storage.new(instance)
        storage.save()
        instance.name = "UpdatedName"
        storage.save()
        updated_instance = storage.get(State, instance.id)
        self.assertEqual(updated_instance.name, "UpdatedName")
