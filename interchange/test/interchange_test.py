from unittest import TestCase
import test_helper
# import fuselage as fs
import interchange as intch

class NullImplementationTest(TestCase):

    def test_null_implementation_return_arguments_if_method_does_not_exist(self):
        ni = intch.NullImplementation()
        result = ni.this_method_does_not_exist(1,2,key=3)
        self.assertEqual(result, ((1,2),{"key":3}))


class StrategyTest(TestCase):

    def test_use_raise_an_error_if_unknown_implementation(self):
        class TestService(intch.Interchange):pass

        with self.assertRaises(intch.UnregisteredImplementationError):
            TestService.use("foo")

    def test_raises_an_error_if_method_not_implemented(self):
        class TestService(intch.Interchange):methods =('add',)

        class NewImplementation(object): pass
        TestService.register("test", NewImplementation )
        TestService.use("test")

        with self.assertRaises(intch.ImplementationMissingError):
            TestService.add(1,2)

    def test_delegates_work_to_selected_implementation(self):
        class TestService(intch.Interchange):methods =('add',)

        class NewImplementation(object):
            def add(self, *args):
                return sum(args)

        TestService.register('test', NewImplementation() )
        TestService.use('test')

        self.assertEqual(TestService.add(1,2),3)

    def test_defines_an_up_query_method(self):
        class TestService(intch.Interchange):methods =('add',)

        class NewImplementation(object):
            def is_up(self):
                return True

        TestService.register('test', NewImplementation() )
        TestService.use('test')

        self.assertTrue(TestService.is_up())
        self.assertFalse(TestService.is_down())

    def test_generates_a_null_implementation_that_returns_the_arguments_by_default(self):
        class TestService(intch.Interchange):methods=('add',)

        self.assertEqual( (1,2), TestService.add(1,2))

    def test_generates_a_down_implementation(self):
        class TestService(intch.Interchange):methods=('add',)
    
        TestService.use("down")
        self.assertTrue(TestService.is_down)

    def test_down_implementation_works_with_extend(self):
        raise NotImplementedError

    def test_can_check_to_see_if_services_are_up(self):
        class TestService(intch.Interchange):methods=('foo',)
        TestService.use("down")
        with self.assertRaises(intch.ImplementationNotAvailableError):
            TestService.check()

    def test_can_implement_multiple_methods_at_once(self):
        class TestService(intch.Interchange):methods=('foo','bar')

        class NewI(object):
            def foo(self): return 'foo'
            def bar(self): return 'bar'

        TestService.register('test', NewI())
        TestService.use('test')

        self.assertEqual('foo', TestService.foo() )
        self.assertEqual('bar', TestService.bar() )

    def test_null_implementation_works_with_extend(self):
        raise NotImplementedError

    def test_can_use_one_implementation_temporarily(self):
        class TestService(intch.Interchange):methods=('number',)

        class One(object):
            def number(self):
                return 1

        class Two(object):
            def number(self):
                return 2

        TestService.register("one", One())
        TestService.register("two", Two())

        TestService.use("one")

        self.assertEqual(1, TestService.number())

        with TestService.work_with("two") as service:
            newnumb = service.number()

        self.assertEqual(2, newnumb)
        self.assertEqual(1, TestService.number())














