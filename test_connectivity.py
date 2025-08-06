#!/usr/bin/env python3
"""
Test script for database connectivity and error handling
"""

from database import DatabaseConnection

def test_database_connectivity():
    """Test database connectivity with improved error handling"""
    print("=== Database Connectivity Test ===\n")
    
    db = DatabaseConnection()
    
    # Test network connectivity
    print("1. Testing network connectivity...")
    if db.test_network_connectivity():
        print("✓ Network is reachable")
    else:
        print("✗ Network connectivity failed")
        return
    
    # Test central database connection
    print("\n2. Testing central database connection...")
    if db.connect("central-mc"):
        print("✓ Central database connection successful")
        db.disconnect()
    else:
        print("✗ Central database connection failed")
        return
    
    # Test tenant database connection
    print("\n3. Testing tenant database connection...")
    if db.connect("tenant-summercamp-2025"):
        print("✓ Tenant database connection successful")
        
        # Test a simple query
        print("\n4. Testing database query...")
        try:
            query = "SELECT COUNT(*) as count FROM currencies WHERE show_in_clientx = '1'"
            results = db.execute_query(query)
            if results:
                count = results[0]['count']
                print(f"✓ Query successful: Found {count} currencies")
            else:
                print("⚠ Query returned no results")
        except Exception as e:
            print(f"✗ Query failed: {e}")
        
        db.disconnect()
    else:
        print("✗ Tenant database connection failed")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_database_connectivity()
