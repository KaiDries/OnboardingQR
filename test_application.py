#!/usr/bin/env python3
"""
Test script for AnyKrowd Onboarding QR Generator
Version: 1.0.0

This script performs comprehensive testing of the application components.
"""

import sys
import os
import unittest
from pathlib import Path
from typing import Dict, Any, List
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class TestEnvironment(unittest.TestCase):
    """Test environment and dependencies"""
    
    def test_python_version(self):
        """Test Python version compatibility"""
        version = sys.version_info
        self.assertGreaterEqual(version.major, 3, "Python 3.x required")
        self.assertGreaterEqual(version.minor, 8, "Python 3.8+ required")
    
    def test_dependencies(self):
        """Test all required dependencies are available"""
        dependencies = [
            'mysql.connector',
            'qrcode',
            'PIL',
            'reportlab.pdfgen',
            'dotenv'
        ]
        
        for dep in dependencies:
            try:
                __import__(dep)
            except ImportError:
                self.fail(f"Missing dependency: {dep}")

class TestConfiguration(unittest.TestCase):
    """Test configuration and setup"""
    
    def test_config_import(self):
        """Test configuration can be imported"""
        try:
            import config
            self.assertTrue(hasattr(config, 'APP_NAME'))
            self.assertTrue(hasattr(config, 'COLORS'))
            self.assertTrue(hasattr(config, 'FONTS'))
        except ImportError:
            self.fail("Cannot import config module")
    
    def test_version_info(self):
        """Test version information"""
        try:
            from version import __version__, get_version_info
            self.assertIsInstance(__version__, str)
            version_info = get_version_info()
            self.assertIsInstance(version_info, dict)
            self.assertIn('version', version_info)
        except ImportError:
            self.skipTest("Version module not available")

class TestUtilities(unittest.TestCase):
    """Test utility functions"""
    
    def test_utils_import(self):
        """Test utils module can be imported"""
        try:
            import utils
            self.assertTrue(hasattr(utils, 'parse_onboarding_name'))
            self.assertTrue(hasattr(utils, 'generate_expected_email'))
        except ImportError:
            self.fail("Cannot import utils module")
    
    def test_email_generation(self):
        """Test email generation functionality"""
        try:
            from utils import generate_expected_email
            email = generate_expected_email("John", "Doe", "example.com")
            self.assertEqual(email, "johndoe@example.com")
        except ImportError:
            self.skipTest("Utils module not available")

class TestQRGenerator(unittest.TestCase):
    """Test QR code generation functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        os.chdir(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(project_root)
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_qr_generator_import(self):
        """Test QR generator can be imported"""
        try:
            from qr_generator import QRCodeGenerator
            generator = QRCodeGenerator()
            self.assertIsInstance(generator, QRCodeGenerator)
        except ImportError:
            self.fail("Cannot import QRCodeGenerator")
    
    def test_qr_code_creation(self):
        """Test basic QR code creation"""
        try:
            from qr_generator import QRCodeGenerator
            generator = QRCodeGenerator()
            
            # Test QR code creation
            qr_img = generator.create_qr_code("https://example.com", 140)
            self.assertIsNotNone(qr_img)
            
        except ImportError:
            self.skipTest("QR generator not available")
        except Exception as e:
            self.fail(f"QR code creation failed: {e}")

class TestFileOperations(unittest.TestCase):
    """Test file and directory operations"""
    
    def test_directory_creation(self):
        """Test directory creation utilities"""
        try:
            from utils import ensure_directory_exists
            test_dir = "test_output"
            ensure_directory_exists(test_dir)
            self.assertTrue(Path(test_dir).exists())
            # Cleanup
            shutil.rmtree(test_dir, ignore_errors=True)
        except ImportError:
            self.skipTest("Utils module not available")

def run_comprehensive_test():
    """Run all tests and provide detailed report"""
    print("=" * 60)
    print("AnyKrowd Onboarding QR Generator - Comprehensive Test")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestEnvironment,
        TestConfiguration,
        TestUtilities,
        TestQRGenerator,
        TestFileOperations
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError: ')[-1].split('\n')[0]}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('\n')[-2]}")
    
    # Overall status
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED - Application is ready for deployment!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED - Please address issues before deployment")
        return 1

if __name__ == "__main__":
    sys.exit(run_comprehensive_test())
