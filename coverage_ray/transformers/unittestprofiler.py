import unittest
import cProfile
import pstats
import io

def profile(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return result
    return wrapper

class TestMyModule(unittest.TestCase):
    @profile
    def test_add(self):
        self.assertEqual(2+3, 5)

    @profile
    def test_subtract(self):
        self.assertEqual(5-2, 2)

if __name__ == '__main__':
    unittest.main()