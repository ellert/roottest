# File: roottest/python/cpp11/PyROOT_cpptests.py
# Author: Wim Lavrijsen (LBNL, WLavrijsen@lbl.gov)
# Created: 11/25/13
# Last: 11/26/13

"""C++11 language interface unit tests for PyROOT package."""

import sys, os, unittest
sys.path.append( os.path.join( os.getcwd(), os.pardir ) )

from ROOT import *
from common import *

__all__ = [
   'Cpp1Cpp11StandardClassesTestCase',
   'Cpp2Cpp11LanguageConstructsTestCase'
]

gROOT.LoadMacro( "Cpp11Features.C+" )


### C++11 standard library classes ===========================================
class Cpp1Cpp11StandardClassesTestCase( MyTestCase ):
   def test01SharedPtr( self ):
      """Test usage and access of std::shared_ptr<>"""

      if not USECPP11:
         return

    # proper memory accounting
      self.assertEqual( MyCounterClass.counter, 0 )

      ptr1 = CreateMyCounterClass()
      self.assert_( not not ptr1 )
      self.assertEqual( MyCounterClass.counter, 1 )

      ptr2 = CreateMyCounterClass()
      self.assert_( not not ptr2 )
      self.assertEqual( MyCounterClass.counter, 2 )

      del ptr2, ptr1
      import gc; gc.collect()
      self.assertEqual( MyCounterClass.counter, 0 )


### C++11 language constructs test cases =====================================
class Cpp2Cpp11LanguageConstructsTestCase( MyTestCase ):
   def test01StaticEnum( self ):
      """Test usage and access of a const static enum defined in header"""

      if not USECPP11:
         return

      # TODO: this will fail
      # self.assert_( hasattr( PyTest, '_Lock_policy' ) )
      if not FIXCLING:
         self.assert_( hasattr( PyTest, '_S_single' ) )
         self.assert_( hasattr( PyTest, '__default_lock_policy' ) )

   def test02NULLPtrPassing( self ):
      """Allow the programmer to pass NULL in certain cases"""


      # note that this test is not protected with USECPP11, as nullptr is
      # defined explicitly in the ROOT module, not taken from C++

      self.assertNotEqual( nullptr, 0 )
      self.assertRaises( TypeError, TGraphErrors, 0, 0, 0 )

      g = TGraphErrors( 0, nullptr, nullptr )
      self.assertEqual( round( g.GetMean(), 8 ), 0.0 )

 
## actual test run
if __name__ == '__main__':
   from MyTextTestRunner import MyTextTestRunner

   loader = unittest.TestLoader()
   testSuite = loader.loadTestsFromModule( sys.modules[ __name__ ] )

   runner = MyTextTestRunner( verbosity = 2 )
   result = not runner.run( testSuite ).wasSuccessful()

   sys.exit( result )
