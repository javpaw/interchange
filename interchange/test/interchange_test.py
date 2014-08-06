from unittest import TestCase
import test_helper
# import fuselage as fs
import interchange as intch

class NullImplementationTest(TestCase):

    def test_null_implementation_return_arguments_if_method_does_not_exist(self):
        ni = intch.NullImplementation()
        result = ni.this_method_does_not_exist(1,2,key=3)
        self.assertEqual(result, ((1,2),{"key":3}))


class InterchangeTest(TestCase):

    def test_use_raise_an_error_if_unknown_implementation(self):
        class TestService(intch.Interchange):pass

        with self.assertRaises(intch.UnregisteredImplementationError):
            ts = TestService()
            ts.use("foo")

    def test_raises_an_error_if_method_not_implemented(self):
        class TestService(intch.Interchange):methods =('add',)

        class NewImplementation(object): pass
        ts = TestService()
        ts.register("test", NewImplementation )
        ts.use("test")

        with self.assertRaises(intch.ImplementationMissingError):
            ts.add(1,2)

    def test_delegates_work_to_selected_implementation(self):
        class TestService(intch.Interchange):methods =('add',)

        class NewImplementation(object):
            def add(self, *args):
                return sum(args)

        ts = TestService()
        ts.register('test', NewImplementation() )
        ts.use('test')

        self.assertEqual(ts.add(1,2),3)

    def test_defines_an_up_query_method(self):
        class TestService(intch.Interchange):methods =('add',)

        class NewImplementation(object):
            def is_up(self):
                return True

        ts = TestService()
        ts.register('test', NewImplementation() )
        ts.use('test')

        self.assertTrue(ts.is_up())
        self.assertFalse(ts.is_down())

    def test_generates_a_null_implementation_that_returns_the_arguments_by_default(self):
        class TestService(intch.Interchange):methods=('add',)
        ts = TestService()
        self.assertEqual( (1,2), ts.add(1,2))

    def test_generates_a_down_implementation(self):
        class TestService(intch.Interchange):methods=('add',)
        ts = TestService()    
        ts.use("down")
        self.assertTrue(ts.is_down())

    def test_can_check_to_see_if_services_are_up(self):
        class TestService(intch.Interchange):methods=('foo',)
        ts = TestService()
        ts.use("down")
        with self.assertRaises(intch.ImplementationNotAvailableError):
            ts.check()

    def test_can_implement_multiple_methods_at_once(self):
        class TestService(intch.Interchange):methods=('foo','bar')

        class NewI(object):
            def foo(self): return 'foo'
            def bar(self): return 'bar'

        ts = TestService()
        ts.register('test', NewI())
        ts.use('test')

        self.assertEqual('foo', ts.foo() )
        self.assertEqual('bar', ts.bar() )


    def test_can_use_one_implementation_temporarily(self):
        class TestService(intch.Interchange):methods=('number',)

        class One(object):
            def number(self):
                return 1

        class Two(object):
            def number(self):
                return 2

        ts = TestService()

        ts.register("one", One())
        ts.register("two", Two())

        ts.use("one")

        self.assertEqual(1, ts.number())

        with ts.work_with("two") as service:
            newnumb = service.number()

        self.assertEqual(2, newnumb)
        self.assertEqual(1, ts.number())














