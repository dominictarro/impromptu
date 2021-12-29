import unittest
from impromptu.argdefiner import ArgDefiner


class ArgDefinerTests(unittest.TestCase):

    def test_package(self):
        """Tests the ArgDefiner.package method.
        """
        # Positional Arguments
        # - Exact positional
        # - Excessive positional
        # - With variable positional argument
        #
        # Default Positional Arguments
        # - Rely on default
        # - Exact positional
        # - Exact w/ keyword
        # - Excessive positional
        # - With variable positional argument
        # - Exact w/ contradictory keyword
        #
        # Keyword Only Arguments
        # - Rely on default
        # - Keyword
        # - Excessive keyword
        # - With variable keyword
        #
        # Mix & Match
        # - Positional & keyword
        # - Positional & keyword w/ variable positional
        # - Positional & keyword w/ variable keyword
        # - Positional & keyword w/ variable positional & variable keyword

        ###################################################
        #
        # Positional
        #
        ###################################################
        def func_test(a,b,c):
            return a+b+c
        ad = ArgDefiner(func_test)
        args, kwds = (0,0,1), {}
        pck = ad.package(args, kwds)
        expected = (0,0,1), {}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        
        ######################
        # Positional w/ excess
        ######################
        def func_test(a,b,c):
            return a+b+c
        ad = ArgDefiner(func_test)
        args, kwds = (0,0,1,1), {}
        pck = ad.package(args, kwds)
        expected = (0,0,1), {}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")

        #######################
        # Positional w/ varargs
        #######################
        def func_test(a,b,c, *args):
            return a+b+c+sum(args)
        ad = ArgDefiner(func_test)
        args, kwds = (0,0,1,1), {}
        pck = ad.package(args, kwds)
        expected = (0,0,1,1), {}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")

        ###################################################
        #
        # Default positional
        #
        ###################################################
        def func_test(a,b=0,c=0):
            return a+b+c
        ad = ArgDefiner(func_test)
        # rely on default
        args, kwds = (0,1), {}
        pck = ad.package(args, kwds)
        expected = (0,1), {'c': 0}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        expected = 1
        result = func_test(*pck[0], **pck[1])
        self.assertEqual(result, expected, msg=f"Expected result {expected} with args {pck[0]} and kwds {pck[1]}, produced result {result}")
        # as keyword
        args, kwds = (0,), {'c': 0, 'b': 1}
        pck = ad.package(args, kwds)
        expected = (0,), {'c': 0, 'b': 1}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        expected = 1
        result = func_test(*pck[0], **pck[1])
        self.assertEqual(result, expected, msg=f"Expected result {expected} with args {pck[0]} and kwds {pck[1]}, produced result {result}")        

        ##############################
        # Default positional w/ excess
        ##############################
        ad = ArgDefiner(func_test)
        args, kwds = (0,1,1,1,1,1), {}
        pck = ad.package(args, kwds)
        expected = (0,1,1), {}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        expected = 2
        result = func_test(*pck[0], **pck[1])
        self.assertEqual(result, expected, msg=f"Expected result {expected} with args {pck[0]} and kwds {pck[1]}, produced result {result}")

        ##############################
        # Default positional w/ varags
        ##############################
        def func_test(a,b=0,c=0, *args):
            return a+b+c+sum(args)
        ad = ArgDefiner(func_test)
        #################
        # rely on default
        #################
        args, kwds = (0,1), {}
        pck = ad.package(args, kwds)
        expected = (0,1), {'c': 0}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        expected = 1
        result = func_test(*pck[0], **pck[1])
        self.assertEqual(result, expected, msg=f"Expected result {expected} with args {pck[0]} and kwds {pck[1]}, produced result {result}")
        #############
        # use varargs
        #############
        args, kwds = (0,1,1,1,1), {}
        pck = ad.package(args, kwds)
        expected = (0,1,1,1,1), {}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        expected = 4
        result = func_test(*pck[0], **pck[1])
        self.assertEqual(result, expected, msg=f"Expected result {expected} with args {pck[0]} and kwds {pck[1]}, produced result {result}")

        ###########################
        # Exact with contradiction
        ###########################
        def func_test(a, b = 1, c = 2):
            return a+b+c
        ad = ArgDefiner(func_test)
        args, kwds = (0,0,1,2,3), {'c': 3}
        pck = ad.package(args, kwds)
        expected = (0,0,1), {}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")

        ###################################################
        #
        # Keyword Only
        #
        ###################################################
        def func_test(*, a=0,b=0,c=0):
            return a+b+c
        ad = ArgDefiner(func_test)
        #################
        # rely on default
        #################
        args, kwds = (), {}
        pck = ad.package(args, kwds)
        expected = (), {'a': 0, 'b': 0, 'c': 0}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        expected = 0
        result = func_test(*pck[0], **pck[1])
        self.assertEqual(result, expected, msg=f"Expected result {expected} with args {pck[0]} and kwds {pck[1]}, produced result {result}")
        #########
        # keyword
        #########
        args, kwds = (), {'a': 1, 'b': 1, 'c': 1}
        pck = ad.package(args, kwds)
        expected = (), {'a': 1, 'b': 1, 'c': 1}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        expected = 3
        result = func_test(*pck[0], **pck[1])
        self.assertEqual(result, expected, msg=f"Expected result {expected} with args {pck[0]} and kwds {pck[1]}, produced result {result}")
        ###################
        # excessive keyword
        ###################
        args, kwds = (), {'a': 1, 'b': 1, 'c': 1, 'd': 10}
        pck = ad.package(args, kwds)
        expected = (), {'a': 1, 'b': 1, 'c': 1}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        expected = 3
        result = func_test(*pck[0], **pck[1])
        self.assertEqual(result, expected, msg=f"Expected result {expected} with args {pck[0]} and kwds {pck[1]}, produced result {result}")
        #######################
        # with variable keyword
        #######################
        def func_test(*, a=0,b=0,c=0, **kwds):
            return a+b+c + sum(kwds.values())
        ad = ArgDefiner(func_test)
        args, kwds = (), {'a': 1, 'd': 1, 'e': 0}
        pck = ad.package(args, kwds)
        expected = (), {'a': 1, 'b': 0, 'c': 0, 'd': 1, 'e': 0}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        expected = 2
        result = func_test(*pck[0], **pck[1])
        self.assertEqual(result, expected, msg=f"Expected result {expected} with args {pck[0]} and kwds {pck[1]}, produced result {result}")

        ###################################################
        #
        # Mix & Match
        #
        ###################################################
        def func_test(a,b=0,*,c=0):
            return a+b+c
        ad = ArgDefiner(func_test)
        ########################
        # positional and keyword
        ########################
        args, kwds = (1,), {'c': 2}
        pck = ad.package(args, kwds)
        expected = (1,), {'b': 0, 'c': 2}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        expected = 3
        result = func_test(*pck[0], **pck[1])
        self.assertEqual(result, expected, msg=f"Expected result {expected} with args {pck[0]} and kwds {pck[1]}, produced result {result}")
        ###################################
        # positional and keyword w/ varargs
        ###################################
        def func_test(a,b=0,*args,c=0):
            return a+b+c+sum(args)
        ad = ArgDefiner(func_test)
        args, kwds = (1,2,3), {'c': 2}
        pck = ad.package(args, kwds)
        expected = (1,2,3), {'c': 2}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        expected = 8
        result = func_test(*pck[0], **pck[1])
        self.assertEqual(result, expected, msg=f"Expected result {expected} with args {pck[0]} and kwds {pck[1]}, produced result {result}")
        #################################
        # positional and keyword w/ varkw
        #################################
        def func_test(a,b=0,*,c=0, **kwds):
            return a+b+c+sum(kwds.values())
        ad = ArgDefiner(func_test)
        args, kwds = (1,), {'c': 2, 'd': 1}
        pck = ad.package(args, kwds)
        expected = (1,), {'b': 0, 'c': 2, 'd': 1}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        expected = 4
        result = func_test(*pck[0], **pck[1])
        self.assertEqual(result, expected, msg=f"Expected result {expected} with args {pck[0]} and kwds {pck[1]}, produced result {result}")
        #########################################
        # positional & keyword w/ varargs & varkw
        #########################################
        def func_test(a,b=0,*args,c=0, **kwds):
            return a+b+c+sum(args)+sum(kwds.values())
        ad = ArgDefiner(func_test)
        args, kwds = (1,2,3), {'c': 2, 'd': 1}
        pck = ad.package(args, kwds)
        expected = (1,2,3), {'c': 2, 'd': 1}
        self.assertTupleEqual(pck[0], expected[0], msg=f"Expected arg tuple {expected[0]}, produced arg tuple {pck[0]}")
        self.assertDictEqual(pck[1], expected[1], msg=f"Expected kwd dict {expected[1]}, produced kwd dict {pck[1]}")
        expected = 9
        result = func_test(*pck[0], **pck[1])
        self.assertEqual(result, expected, msg=f"Expected result {expected} with args {pck[0]} and kwds {pck[1]}, produced result {result}")

