# unittest.TestCase or django.test.SimpleTestCase == No database needed.
# django.test.TestCase == Database needed.

# It also provides an additional method:
# >> classmethod TestCase.setUpTestData()
# The class-level atomic block described above allows the creation of initial data at the class level,
# once for the whole TestCase.
# This technique allows for faster tests as compared to using setUp().
