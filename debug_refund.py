#!/usr/bin/env python3
"""
Debug script to test refund settings
"""

from database import DatabaseConnection

def debug_refund_settings():
    """Debug refund settings lookup"""
    print("=== Debug Refund Settings ===\n")
    
    db = DatabaseConnection()
    
    # Test connection to central database
    if not db.connect("central-mc"):
        print("✗ Could not connect to central database")
        return
    
    print("✓ Connected to central database")
    
    # Test different tenant ID formats
    tenant_variations = [
        "summercamp-2025",
        "summercamp",
        "tenant-summercamp-2025"
    ]
    
    for tenant_id in tenant_variations:
        print(f"\n--- Testing tenant ID: {tenant_id} ---")
        
        # Check if tenant exists in tenants table
        query = "SELECT id, data FROM tenants WHERE id = %s"
        results = db.execute_query(query, (tenant_id,))
        
        if results:
            for tenant in results:
                print(f"Found tenant: {tenant['id']}")
                data = tenant.get('data', {})
                if data:
                    print(f"Data type: {type(data)}")
                    if isinstance(data, str):
                        print(f"Data (first 200 chars): {data[:200]}...")
                        # Try to parse as JSON
                        try:
                            import json
                            parsed_data = json.loads(data)
                            print(f"Parsed data keys: {list(parsed_data.keys()) if isinstance(parsed_data, dict) else 'Not a dict'}")
                            if isinstance(parsed_data, dict):
                                enable_refund = parsed_data.get('enable_refund_scheduler', 'Not found')
                                refund_start = parsed_data.get('refund_start_datetime', 'Not found')
                                refund_end = parsed_data.get('refund_end_datetime', 'Not found')
                                print(f"Enable refund scheduler: {enable_refund}")
                                print(f"Refund start datetime: {refund_start}")
                                print(f"Refund end datetime: {refund_end}")
                        except Exception as e:
                            print(f"Error parsing JSON: {e}")
                    else:
                        print(f"Data: {data}")
                    
                    # Try to get refund settings for this tenant
                    refund_settings = db.get_refund_settings(tenant['id'])
                    print(f"Refund settings: {refund_settings}")
        else:
            print(f"No tenant found with ID: {tenant_id}")
    
    # Also check all tenants to see what's available
    print(f"\n--- All available tenants ---")
    query = "SELECT id FROM tenants LIMIT 10"
    results = db.execute_query(query)
    
    if results:
        for tenant in results:
            print(f"- {tenant['id']}")
    
    db.disconnect()
    print("\n=== Debug Complete ===")

if __name__ == "__main__":
    debug_refund_settings()
