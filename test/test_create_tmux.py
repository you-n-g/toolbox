import unittest
from xytb.tmux import T

class TestCreateTmux(unittest.TestCase):

    def test_create_tmux(self):
        p = T("TEST-session.TEST-window", create_if_not_exists=True)

if __name__ == "__main__":
    unittest.main()
