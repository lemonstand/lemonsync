#!/usr/bin/env python

import unittest
import sys
import LemonSync
from unit.utils import TestUtils

def main ():
    # Run the test suites
    utils= unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    unittest.TestSuite([utils])
    unittest.main(verbosity=2)
    
if __name__ == '__main__':
    main()