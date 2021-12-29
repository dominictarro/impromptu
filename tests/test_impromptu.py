import json
import unittest
from impromptu.impromptu import Impromptu


class ImpromptuTests(unittest.TestCase):

    def test_init(self):
        """Tests the initialization methods (Impromptu.from_string, Impromptu.from_dict, Impromptu.from_file).
        """
        case = {
            'a': 0,
            'b': {'$lt': 0},
            'cCheck': {'$assign': {
                'c': 0,
                'dCheck': {'$assign': {'d': 0}}
                }},
            'dCheck': {'$assign': {'d': 0}},
        }
        # have to create the subclasses to deal with singleton behavior
        class DictImpromptu(Impromptu): pass
        class StringImpromptu(Impromptu): pass
        class FileImpromptu(Impromptu): pass

        ###########
        # From dict
        ###########
        d = DictImpromptu.from_dict(case)
        expected = {'a': 0, 'b': {'$lt': 0}}
        result = d.root.definition
        self.assertDictEqual(result, expected, msg=f"Expected root definition {expected}, produced root definition {result}")
        expected = {'a': 0, 'b': {'$lt': 0}, 'c': 0}
        result = d.root.get('cCheck').definition
        self.assertDictEqual(result, expected, msg=f"Expected child definition {expected}, produced child definition {result}")

        #############
        # From string
        #############
        d = StringImpromptu.from_string(json.dumps(case))
        expected = {'a': 0, 'b': {'$lt': 0}}
        result = d.root.definition
        self.assertDictEqual(result, expected, msg=f"Expected root definition {expected}, produced root definition {result}")

        ###########
        # From file
        ###########
        with open('tests/query.json', 'r') as f: # NOTE, expects unit testing to be executed from the project directory, not tests directory
            d = FileImpromptu.from_file(fp=f)
        expected = {'a': 0, 'b': {'$lt': 0}}
        result = d.root.definition
        self.assertDictEqual(result, expected, msg=f"Expected root definition {expected}, produced root definition {result}")

    def test_match(self):
        """Tests the Impromptu.match method.
        """
        case = {
            'a': 0,
            'b': {'$lt': 0},
            'cCheck': {'$assign': {
                'c': 0,
                'dCheck': {'$assign': {'d': 0}}
                }},
            'dCheck': {'$assign': {'d': 0}},
        }
        d: Impromptu = Impromptu.from_dict(case)
        ##############
        # Root matches
        ##############
        definition = d.root.definition
        entry = {'a': 0, 'b': -1}
        self.assertTrue(d.match(**entry), msg=f"Expected {definition} to match entry {entry}")
        self.assertTrue(d(entry=entry), msg=f"Expected {definition} to match entry {entry}")

        entry = {'a': 0, 'b': 1}
        self.assertFalse(d.match(**entry), msg=f"Expected {definition} to not match entry {entry}")
        self.assertFalse(d(entry=entry), msg=f"Expected {definition} to not match entry {entry}")

        ################
        # cCheck matches
        ################
        definition = d.root.get('cCheck').definition
        entry = {'a': 0, 'b': -1, 'c': 0}
        self.assertTrue(d.match(label='cCheck', **entry), msg=f"Expected {definition} to match entry {entry}")
        self.assertTrue(d(label='cCheck', entry=entry), msg=f"Expected {definition} to match entry {entry}")

        entry = {'a': 0, 'b': 1, 'c': 0}
        self.assertFalse(d.match(label='cCheck', **entry), msg=f"Expected {definition} to not match entry {entry}")
        self.assertFalse(d(label='cCheck', entry=entry), msg=f"Expected {definition} to not match entry {entry}")

    def test_on_match(self):
        """Tests the Impromptu.on_match wrapper and its functionality.
        """
        case = {
            'a': 0,
            'b': {'$lt': 0},
            'cCheck': {'$assign': {
                'c': 0,
                'dCheck': {'$assign': {'d': 0}}
                }},
            'dCheck': {'$assign': {'d': 0}},
        }
        d: Impromptu = Impromptu.from_dict(case)

        #####
        # get
        #####
        discovery_method='get'
        @d.on_match(discovery_method=discovery_method)
        def add(a: int, b: int) -> int:
            return a + b

        args = {'a': 0, 'b': -1}
        expected = -1
        result = add(**args)
        self.assertEqual(result, expected, msg=f"Expected {expected} with definition {d.root.definition} and arguments {args}, produced {result}")

        args = {'a': 0, 'b': 1}
        result = add(**args)
        self.assertIsNone(result, msg=f"Expected None with definition {d.root.definition} and arguments {args}, produced {result}")

        ########
        # search
        ########
        # depth
        @d.on_match(label='dCheck', discovery_method='search', method='depth')
        def add(a: int, b: int) -> int:
            return a + b

        args = {'a': 0, 'b': -1, 'c': 0, 'd': 0}
        expected = -1
        result = add(**args)
        self.assertEqual(result, expected, msg=f"Expected {expected} with definition {d.root.definition} and arguments {args}, produced {result}")

        args = {'a': 0, 'b': 1}
        result = add(**args)
        self.assertIsNone(result, msg=f"Expected None with definition {d.root.definition} and arguments {args}, produced {result}")

        args = {'a': 0, 'b': 1, 'c': 0, 'd': 0}
        result = add(**args)
        self.assertIsNone(result, msg=f"Expected None with definition {d.root.definition} and arguments {args}, produced {result}")

        # depth
        @d.on_match(label='dCheck', discovery_method='search', method='breadth')
        def add(a: int, b: int) -> int:
            return a + b

        args = {'a': 0, 'b': -1, 'c': 1, 'd': 0}
        expected = -1
        result = add(**args)
        self.assertEqual(result, expected, msg=f"Expected {expected} with definition {d.root.definition} and arguments {args}, produced {result}")

        args = {'a': 0, 'b': 1}
        result = add(**args)
        self.assertIsNone(result, msg=f"Expected None with definition {d.root.definition} and arguments {args}, produced {result}")

        args = {'a': 0, 'b': 1, 'c': 0, 'd': 0}
        result = add(**args)
        self.assertIsNone(result, msg=f"Expected None with definition {d.root.definition} and arguments {args}, produced {result}")

        #################
        # true_if_missing
        #################
        label='aMissingLabel'
        @d.on_match(label=label, false_return_value=None, true_if_missing=False)
        def add(a: int, b: int) -> int:
            return a + b

        args = {'a': 0, 'b': -1, 'c': 1, 'd': 0}
        result = add(**args)
        self.assertIsNone(result, msg=f"Expected None with label {label} and arguments {args}, produced {result}")

        @d.on_match(label=label, false_return_value=None, true_if_missing=True)
        def add(a: int, b: int) -> int:
            return a + b

        args = {'a': 0, 'b': -1, 'c': 1, 'd': 0}
        result = add(**args)
        expected = -1
        self.assertEqual(result, expected, msg=f"Expected {expected} with label {label} and arguments {args}, produced {result}")

        #########
        # inverse
        #########
        @d.on_match(inverse=False)
        def add(a: int, b: int) -> int:
            return a + b

        args = {'a': 0, 'b': -1}
        expected = -1
        result = add(**args)
        self.assertEqual(result, expected, msg=f"Expected {expected} with definition {d.root.definition} and arguments {args}, produced {result}")

        args = {'a': 0, 'b': 1}
        result = add(**args)
        self.assertIsNone(result, msg=f"Expected None with definition {d.root.definition} and arguments {args}, produced {result}")

        @d.on_match(inverse=True)
        def add(a: int, b: int) -> int:
            return a + b

        args = {'a': 0, 'b': -1}
        result = add(**args)
        self.assertIsNone(result, msg=f"Expected None with definition {d.root.definition} and arguments {args}, produced {result}")

        args = {'a': 0, 'b': 1}
        expected = 1
        result = add(**args)
        self.assertEqual(result, expected, msg=f"Expected {expected} with definition {d.root.definition} and arguments {args}, produced {result}")
