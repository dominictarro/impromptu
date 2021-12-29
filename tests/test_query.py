import unittest
from collections import OrderedDict
from impromptu.query import Query


class QueryTests(unittest.TestCase):

    def test_initialization(self):
        """Tests the post-initialization variables.
        """
        cases = [
            {
                'a': 0,
                'b': {'$lt': 0},
            },
            {
                'a': 0,
                'b': {'$lt': 0},
                'cCheck': {'$assign': {'c': 0}},
            },
            {
                'a': 0,
                'b': {'$lt': 0},
                'cCheck': {'$assign': {
                    'c': 0,
                    'cCheckPosB': {'$assign': {'b': {'$gt': 0}}}
                    }},
            },
            {
                'a': 0,
                'b': {'$lt': 0},
                'cCheck': {'$assign': {'c': 0}},
                'dCheck': {'$assign': {'d': 0}},
            },
            {
                'a': 0,
                'b': {'$lt': 0},
                'cCheck': {'$assign': {
                    'c': 0,
                    'cCheckPosB': {'$assign': {'b': {'$gt': 0}}}
                    }},
                'dCheck': {'$assign': {'d': 0}},
            },
        ]
        # case[0] - Basic Query
        # case[1] - Query with child Query
        # case[2] - Query with child Query within child Query (a.k.a. nested child Query)
        # case[3] - Query with multiple children Queries
        # case[4] - Query with multiple children Queries and a nested child Query
        
        ########
        # CASE 0
        ########
        q: Query = Query(cases[0])
        self.assertIsNone(q.parent, msg=f"Expected no parent, produced parent {q.parent}")
        expected = "#root"
        self.assertEqual(q.label, expected, msg=f"Expected label {expected}, produced label {q.label}")
        expected = {'a': 0, 'b': {'$lt': 0}}
        self.assertDictEqual(q.definition, expected, msg=f"Expected definition {expected}, produced definition {q.definition}")
        expected = []
        self.assertListEqual(list(q.children.keys()), expected, msg=f"Expected children keys {expected}, produced children {q.children}")
        
        ########
        # CASE 1
        ########
        q: Query = Query(cases[1])
        self.assertIsNone(q.parent, msg=f"Expected no parent, produced parent {q.parent}")
        expected = "#root"
        self.assertEqual(q.label, expected, msg=f"Expected label {expected}, produced label {q.label}")
        expected = {'a': 0, 'b': {'$lt': 0}}
        self.assertDictEqual(q.definition, expected, msg=f"Expected definition {expected}, produced definition {q.definition}")
        expected = ['cCheck']
        self.assertListEqual(list(q.children.keys()), expected, msg=f"Expected children keys {expected}, produced children {q.children}")

        expected = q
        q = q.children.get('cCheck')
        self.assertEqual(q.parent, expected, msg=f"Expected parent {expected}, produced parent {q.parent}")
        expected = "cCheck"
        self.assertEqual(q.label, expected, msg=f"Expected label {expected}, produced label {q.label}")
        expected = {'a': 0, 'b': {'$lt': 0}, 'c': 0}
        self.assertDictEqual(q.definition, expected, msg=f"Expected definition {expected}, produced definition {q.definition}")
        expected = []
        self.assertListEqual(list(q.children.keys()), expected, msg=f"Expected children keys {expected}, produced children {q.children}")

        ########
        # CASE 2
        ########
        q: Query = Query(cases[2])
        self.assertIsNone(q.parent, msg=f"Expected no parent, produced parent {q.parent}")
        expected = "#root"
        self.assertEqual(q.label, expected, msg=f"Expected label {expected}, produced label {q.label}")
        expected = {'a': 0, 'b': {'$lt': 0}}
        self.assertDictEqual(q.definition, expected, msg=f"Expected definition {expected}, produced definition {q.definition}")
        expected = ['cCheck']
        self.assertListEqual(list(q.children.keys()), expected, msg=f"Expected children keys {expected}, produced children {q.children}")

        expected = q
        q = q.children.get('cCheck')
        self.assertEqual(q.parent, expected, msg=f"Expected parent {expected}, produced parent {q.parent}")
        expected = "cCheck"
        self.assertEqual(q.label, expected, msg=f"Expected label {expected}, produced label {q.label}")
        expected = {'a': 0, 'b': {'$lt': 0}, 'c': 0}
        self.assertDictEqual(q.definition, expected, msg=f"Expected definition {expected}, produced definition {q.definition}")
        expected = ['cCheckPosB']
        self.assertListEqual(list(q.children.keys()), expected, msg=f"Expected children keys {expected}, produced children {q.children}")

        expected = q
        q = q.children.get('cCheckPosB')
        self.assertEqual(q.parent, expected, msg=f"Expected parent {expected}, produced parent {q.parent}")
        expected = "cCheckPosB"
        self.assertEqual(q.label, expected, msg=f"Expected label {expected}, produced label {q.label}")
        expected = {'a': 0, 'b': {'$gt': 0}, 'c': 0}
        self.assertDictEqual(q.definition, expected, msg=f"Expected definition {expected}, produced definition {q.definition}")
        expected = []
        self.assertListEqual(list(q.children.keys()), expected, msg=f"Expected children keys {expected}, produced children {q.children}")

        ########
        # CASE 3
        ########
        q: Query = Query(cases[3])
        self.assertIsNone(q.parent, msg=f"Expected no parent, produced parent {q.parent}")
        expected = "#root"
        self.assertEqual(q.label, expected, msg=f"Expected label {expected}, produced label {q.label}")
        expected = {'a': 0, 'b': {'$lt': 0}}
        self.assertDictEqual(q.definition, expected, msg=f"Expected definition {expected}, produced definition {q.definition}")
        expected = ['cCheck', 'dCheck']
        self.assertListEqual(list(q.children.keys()), expected, msg=f"Expected children keys {expected}, produced children {q.children}")

        expected = q
        q = q.children.get('cCheck')
        self.assertEqual(q.parent, expected, msg=f"Expected parent {expected}, produced parent {q.parent}")
        expected = "cCheck"
        self.assertEqual(q.label, expected, msg=f"Expected label {expected}, produced label {q.label}")
        expected = {'a': 0, 'b': {'$lt': 0}, 'c': 0}
        self.assertDictEqual(q.definition, expected, msg=f"Expected definition {expected}, produced definition {q.definition}")
        expected = []
        self.assertListEqual(list(q.children.keys()), expected, msg=f"Expected children keys {expected}, produced children {q.children}")

        expected = q.parent
        q = q.parent.children.get('dCheck')
        self.assertEqual(q.parent, expected, msg=f"Expected parent {expected}, produced parent {q.parent}")
        expected = "dCheck"
        self.assertEqual(q.label, expected, msg=f"Expected label {expected}, produced label {q.label}")
        expected = {'a': 0, 'b': {'$lt': 0}, 'd': 0}
        self.assertDictEqual(q.definition, expected, msg=f"Expected definition {expected}, produced definition {q.definition}")
        expected = []
        self.assertListEqual(list(q.children.keys()), expected, msg=f"Expected children keys {expected}, produced children {q.children}")

        ########
        # CASE 4
        ########
        q: Query = Query(cases[4])
        self.assertIsNone(q.parent, msg=f"Expected no parent, produced parent {q.parent}")
        expected = "#root"
        self.assertEqual(q.label, expected, msg=f"Expected label {expected}, produced label {q.label}")
        expected = {'a': 0, 'b': {'$lt': 0}}
        self.assertDictEqual(q.definition, expected, msg=f"Expected definition {expected}, produced definition {q.definition}")
        expected = ['cCheck', 'dCheck']
        self.assertListEqual(list(q.children.keys()), expected, msg=f"Expected children keys {expected}, produced children {q.children}")

        expected = q
        q = q.children.get('cCheck')
        self.assertEqual(q.parent, expected, msg=f"Expected parent {expected}, produced parent {q.parent}")
        expected = "cCheck"
        self.assertEqual(q.label, expected, msg=f"Expected label {expected}, produced label {q.label}")
        expected = {'a': 0, 'b': {'$lt': 0}, 'c': 0}
        self.assertDictEqual(q.definition, expected, msg=f"Expected definition {expected}, produced definition {q.definition}")
        expected = ['cCheckPosB']
        self.assertListEqual(list(q.children.keys()), expected, msg=f"Expected children keys {expected}, produced children {q.children}")

        expected = q
        q = q.children.get('cCheckPosB')
        self.assertEqual(q.parent, expected, msg=f"Expected parent {expected}, produced parent {q.parent}")
        expected = "cCheckPosB"
        self.assertEqual(q.label, expected, msg=f"Expected label {expected}, produced label {q.label}")
        expected = {'a': 0, 'b': {'$gt': 0}, 'c': 0}
        self.assertDictEqual(q.definition, expected, msg=f"Expected definition {expected}, produced definition {q.definition}")
        expected = []
        self.assertListEqual(list(q.children.keys()), expected, msg=f"Expected children keys {expected}, produced children {q.children}")

        expected = q.parent.parent
        q = q.parent.parent.children.get('dCheck')
        self.assertEqual(q.parent, expected, msg=f"Expected parent {expected}, produced parent {q.parent}")
        expected = "dCheck"
        self.assertEqual(q.label, expected, msg=f"Expected label {expected}, produced label {q.label}")
        expected = {'a': 0, 'b': {'$lt': 0}, 'd': 0}
        self.assertDictEqual(q.definition, expected, msg=f"Expected definition {expected}, produced definition {q.definition}")
        expected = []
        self.assertListEqual(list(q.children.keys()), expected, msg=f"Expected children keys {expected}, produced children {q.children}")

    def test_get(self):
        """Tests Query.get method and functionality.
        """
        case = {
            'a': 0,
            'b': {'$lt': 0},
            'cCheck': {'$assign': {
                'c': 0,
                'cCheckPosB': {'$assign': {'b': {'$gt': 0}}}
                }},
            'dCheck': {'$assign': {'d': 0}},
        }
        q: Query = Query(case)

        ##########
        # Get self
        ##########
        expected = q
        self.assertEqual(q.get(''), expected, msg=f"Expected Query {expected}, produced query {q.get('')}")
        self.assertEqual(q.get('#root'), expected, msg=f"Expected Query {expected}, produced query {q.get('')}")

        ####################
        # Get without nested
        ####################
        expected = {'a': 0, 'b': {'$lt': 0}, 'd': 0}
        self.assertDictEqual(q.get('dCheck').definition, expected, msg=f"Expected definition {expected}, produced definition {q.get('dCheck').definition}")

        #################
        # Get with nested
        #################
        expected = {'a': 0, 'b': {'$lt': 0}, 'c': 0}
        self.assertDictEqual(q.get('cCheck').definition, expected, msg=f"Expected definition {expected}, produced definition {q.get('cCheck').definition}")

        ############
        # Get nested
        ############
        expected = {'a': 0, 'b': {'$gt': 0}, 'c': 0}
        self.assertDictEqual(q.get('cCheck.cCheckPosB').definition, expected, msg=f"Expected definition {expected}, produced definition {q.get('cCheck.cCheckPosB').definition}")
        self.assertDictEqual(q.get('cCheck').get('cCheckPosB').definition, expected, msg=f"Expected definition {expected}, produced definition {q.get('cCheck').get('cCheckPosB').definition}")
    
    def test_search(self):
        """Tests Query.search method and functionality.
        """
        case = OrderedDict({
            'a': 0,
            'b': {'$lt': 0},
            'cCheck': {'$assign': {
                'c': 0,
                'dCheck': {'$assign': {'d': 0}}
                }},
            'dCheck': {'$assign': {'d': 0}},
        })
        q: Query = Query(case)

        expected = {'a': 0, 'b': {'$lt': 0}}
        result = q.search('')
        self.assertDictEqual(result.definition, expected, msg=f"Expected definition {expected}, produced definition {result.definition}")

        #############
        # Depth-first
        #############
        # basic
        expected = {'a': 0, 'b': {'$lt': 0}, 'c': 0, 'd': 0}
        result = q.search('dCheck', method='depth')
        self.assertDictEqual(result.definition, expected, msg=f"Expected definition {expected}, produced definition {result.definition}")
        # default
        expected = {}
        result = q.search('defaultCheck', default=Query({}), method='depth')
        self.assertDictEqual(result.definition, expected, msg=f"Expected definition {expected}, produced definition {result.definition}")
        # begin
        expected = {'a': 0, 'b': {'$lt': 0}, 'd': 0}
        result = q.search('dCheck', begin='dCheck', method='depth')
        self.assertDictEqual(result.definition, expected, msg=f"Expected definition {expected}, produced definition {result.definition}")

        ###############
        # Breadth-first
        ###############
        # basic
        expected = {'a': 0, 'b': {'$lt': 0}, 'd': 0}
        result = q.search('dCheck', method='breadth')
        self.assertDictEqual(result.definition, expected, msg=f"Expected definition {expected}, produced definition {result.definition}")
        # default
        expected = {}
        result = q.search('defaultCheck', default=Query({}), method='breadth')
        self.assertDictEqual(result.definition, expected, msg=f"Expected definition {expected}, produced definition {result.definition}")
        # begin
        expected = {'a': 0, 'b': {'$lt': 0}, 'c': 0, 'd': 0}
        result = q.search('dCheck', begin='cCheck', method='breadth')
        self.assertDictEqual(result.definition, expected, msg=f"Expected definition {expected}, produced definition {result.definition}")

    def test_jsonify(self):
        """Tests Query.jsonify method and functionality.
        """
        case = {
            'a': 0,
            'b': {'$lt': 0},
            'cCheck': {'$assign': {
                'c': 0,
                'cCheckPosB': {'$assign': {'b': {'$gt': 0}}}
                }},
            'dCheck': {'$assign': {'d': 0}},
        }
        q: Query = Query(case)

        expected = {
            'a': 0,
            'b': {'$lt': 0},
            'cCheck': {'$assign': {
                'a': 0,
                'b': {'$lt': 0},
                'c': 0,
                'cCheckPosB': {'$assign': {
                    'a': 0,
                    'c': 0,
                    'b': {'$gt': 0}}
                    }
                }},
            'dCheck': {'$assign': {
                'a': 0,
                'b': {'$lt': 0},
                'd': 0
                }},
        }
        result = q.jsonify(deduplicate=False)
        self.assertDictEqual(result, expected, msg=f"Expected JSON {expected}, produced JSON {result}")

        expected = case
        result = q.jsonify(deduplicate=True)
        self.assertDictEqual(result, expected, msg=f"Expected JSON {expected}, produced JSON {result}")

    def test_match(self):
        """Tests Query.match method.
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
        q: Query = Query(case)
        
        ######
        # Root
        ######
        node = q
        entry = {'a': 0, 'b': -1}
        self.assertTrue(node.match(entry), msg=f"Expected {node.definition} to match entry {entry}")
        entry = {'a': 0, 'b': 1}
        self.assertFalse(node.match(entry), msg=f"Expected {node.definition} to not match entry {entry}")

        #############
        # With nested
        #############
        node = q.get('cCheck')
        entry = {'a': 0, 'b': -1, 'c': 0, 'd': 100} # true case
        self.assertTrue(node.match(entry), msg=f"Expected {node.definition} to match entry {entry}")
        entry = {'a': 0, 'b': 1, 'c': 1, 'd': 100} # one false case
        self.assertFalse(node.match(entry), msg=f"Expected {node.definition} to not match entry {entry}")
        entry = {'a': 0, 'b': -1, 'c': -1, 'd': 100} # two false case
        self.assertFalse(node.match(entry), msg=f"Expected {node.definition} to not match entry {entry}")
        entry = {'a': 0, 'b': -1, 'd': 100} # missing case
        self.assertFalse(node.match(entry), msg=f"Expected {node.definition} to not match entry {entry}")

        ########
        # Nested
        ########
        node = q.get('cCheck.dCheck')
        entry = {'a': 0, 'b': -1, 'c': 0, 'd': 0} # true case
        self.assertTrue(node.match(entry), msg=f"Expected {node.definition} to match entry {entry}")
        entry = {'a': 0, 'b': -1, 'c': 0, 'd': 100} # one false case
        self.assertFalse(node.match(entry), msg=f"Expected {node.definition} to not match entry {entry}")
        entry = {'a': 0, 'b': -1, 'c': -1, 'd': 100} # two false case
        self.assertFalse(node.match(entry), msg=f"Expected {node.definition} to not match entry {entry}")
        entry = {'a': 0, 'c': -1, 'd': 100} # missing case
        self.assertFalse(node.match(entry), msg=f"Expected {node.definition} to not match entry {entry}")
