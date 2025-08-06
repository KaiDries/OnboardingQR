import mysql.connector
import os
import socket
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.base_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'port': 3306,
            'ssl_disabled': False
        }
        self.connection = None
        self.central_db = "central-mc"  # Central database with domains table
        self.current_database = None
    
    def test_network_connectivity(self) -> bool:
        """Test if we can reach the database server"""
        try:
            host = self.base_config['host']
            port = self.base_config['port']
            
            print(f"Testing network connectivity to {host}:{port}...")
            
            # Create a socket and try to connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)  # 10 second timeout
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"✓ Network connectivity to {host}:{port} successful")
                return True
            else:
                print(f"✗ Cannot reach {host}:{port} (error code: {result})")
                print("This indicates a network connectivity issue.")
                return False
                
        except Exception as e:
            print(f"✗ Network connectivity test failed: {e}")
            return False
    
    def connect(self, database: str = None, retry_attempts: int = 3):
        """Establish database connection to specific database with retry logic"""
        config = self.base_config.copy()
        if database:
            config['database'] = database
            self.current_database = database
        
        # Add connection timeout settings
        config.update({
            'connection_timeout': 10,  # 10 seconds connection timeout
            'autocommit': True,
            'use_pure': True  # Use pure Python implementation for better compatibility
        })
        
        for attempt in range(retry_attempts):
            try:
                if self.connection and self.connection.is_connected():
                    self.connection.close()
                
                self.connection = mysql.connector.connect(**config)
                if database:
                    print(f"Database connection established to: {database}")
                else:
                    print("Database connection established successfully")
                return True
                
            except mysql.connector.Error as err:
                if attempt < retry_attempts - 1:
                    print(f"Connection attempt {attempt + 1} failed, retrying... ({err})")
                    import time
                    time.sleep(2)  # Wait 2 seconds before retry
                else:
                    print(f"Error connecting to database {database or 'server'} after {retry_attempts} attempts: {err}")
                    print("This might be due to:")
                    print("- Network connectivity issues")
                    print("- Database server maintenance")
                    print("- VPN/firewall blocking the connection")
                    print("- AWS RDS instance being unavailable")
                    return False
            except Exception as e:
                print(f"Unexpected connection error: {e}")
                return False
        
        return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
    
    def list_databases(self) -> List[str]:
        """List available databases"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            cursor.close()
            return databases
        except mysql.connector.Error as err:
            print(f"Error listing databases: {err}")
            return []
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict[str, Any]]]:
        """Execute a SELECT query and return results"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            return None
    
    def find_tenant_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Find tenant by slug in domains table"""
        # Connect to central database for domains lookup
        if not self.connect(self.central_db):
            return None

        query = "SELECT * FROM domains WHERE tenant_id = %s"
        results = self.execute_query(query, (slug,))

        if results:
            return results[0]

        return None
    
    def find_partial_tenants(self, slug: str) -> List[Dict[str, Any]]:
        """Find tenants by partial slug match"""
        if not self.connect(self.central_db):
            return []
        
        query = "SELECT * FROM domains WHERE tenant_id LIKE %s OR domain LIKE %s ORDER BY tenant_id"
        results = self.execute_query(query, (f"%{slug}%", f"%{slug}%"))
        
        return results if results else []
    
    def get_onboarding_qrs(self, tenant_id: str) -> List[Dict[str, Any]]:
        """Get all onboarding QRs for a tenant"""
        # Connect to tenant-specific database
        tenant_db = f"tenant-{tenant_id}"
        if not self.connect(tenant_db):
            return []
        
        query = """
        SELECT 
            o.name AS onboarding_name,
            l.name AS location_name,
            s.name AS sales_name,
            e.name AS event_name,
            o.qr_code,
            -- Rollen kolom
            TRIM(BOTH ', ' FROM CONCAT(
                CASE WHEN JSON_EXTRACT(r.rights, '$.top_up') = true THEN 'top_up, ' ELSE '' END,
                CASE WHEN JSON_EXTRACT(r.rights, '$.sales_manager') = true THEN 'sales, ' ELSE '' END,
                CASE WHEN JSON_EXTRACT(r.rights, '$.entrance') = true THEN 'entrance, ' ELSE '' END
            )) AS rollen,
            -- Betaalmethodes (voor alle rollen die transactie rechten hebben)
            CASE 
                WHEN JSON_EXTRACT(r.rights, '$.sales_manager') = true OR JSON_EXTRACT(r.rights, '$.top_up') = true THEN
                    TRIM(BOTH ', ' FROM CONCAT(
                        CASE WHEN JSON_EXTRACT(r.rights, '$.card_transactions') = true THEN 'CARD, ' ELSE '' END,
                        CASE WHEN JSON_EXTRACT(r.rights, '$.cash_transactions') = true THEN 'CASH, ' ELSE '' END,
                        CASE WHEN JSON_EXTRACT(r.rights, '$.qr_transactions') = true THEN 'QR, ' ELSE '' END,
                        CASE WHEN JSON_EXTRACT(r.rights, '$.rfid_transactions') = true THEN 'RFID, ' ELSE '' END
                    ))
                ELSE ''
            END AS betaalmethodes
        FROM onboardings o
        LEFT JOIN locations l ON o.location_id = l.id
        LEFT JOIN sale_catalogues s ON o.sale_catalogue_id = s.id
        LEFT JOIN events e ON o.event_id = e.id
        LEFT JOIN roleables rbl
          ON rbl.roleable_type = 'App\\\\Models\\\\Tenant\\\\Onboarding'
          AND rbl.roleable_id = o.id
        LEFT JOIN roles r
          ON rbl.role_id = r.id AND r.deleted_at IS NULL AND JSON_VALID(r.rights) = 1
        WHERE o.deleted_at IS NULL
        """
        
        results = self.execute_query(query)
        return results if results else []
    
    def find_user_by_onboarding_name(self, onboarding_name: str, tenant_id: str = None) -> List[Dict[str, Any]]:
        """Find users by onboarding name in email that have RFID tags with QR codes, excluding personal email domains"""
        # Use current database if already connected to tenant db, otherwise connect to tenant db
        if tenant_id and self.current_database != f"tenant-{tenant_id}":
            tenant_db = f"tenant-{tenant_id}"
            if not self.connect(tenant_db):
                return []
        
        # Only return users that have RFID tags with QR codes (INNER JOIN)
        query = """
        SELECT 
            u.firstname, 
            u.lastname, 
            u.email,
            rt.qr_code
        FROM users u
        INNER JOIN user_rfid_tags urt ON u.id = urt.user_id
        INNER JOIN rfid_tags rt ON urt.rfid_tag_id = rt.id
        WHERE u.email LIKE %s 
        AND u.email NOT LIKE '%@gmail.com' 
        AND u.email NOT LIKE '%@hotmail.com' 
        AND u.email NOT LIKE '%@outlook.com'
        AND u.email NOT LIKE '%@yahoo.com'
        AND u.email NOT LIKE '%@live.com'
        AND u.email NOT LIKE '%@msn.com'
        AND rt.qr_code IS NOT NULL
        AND rt.qr_code != ''
        ORDER BY u.email
        """
        results = self.execute_query(query, (f"%{onboarding_name}%",))
        return results if results else []
    
    def get_event_details(self, event_name: str, tenant_id: str = None) -> Optional[Dict[str, Any]]:
        """Get event details including start and end times"""
        # Use current database if already connected to tenant db, otherwise connect to tenant db
        if tenant_id and self.current_database != f"tenant-{tenant_id}":
            tenant_db = f"tenant-{tenant_id}"
            if not self.connect(tenant_db):
                return None
        
        query = "SELECT * FROM events WHERE name = %s"
        results = self.execute_query(query, (event_name,))
        return results[0] if results else None

    def get_currencies(self, tenant_id: str = None) -> List[Dict[str, Any]]:
        """Get currencies information for the tenant"""
        # Use current database if already connected to tenant db, otherwise connect to tenant db
        if tenant_id and self.current_database != f"tenant-{tenant_id}":
            tenant_db = f"tenant-{tenant_id}"
            if not self.connect(tenant_db):
                return []
        
        query = """
        SELECT *
        FROM currencies 
        WHERE show_in_clientx = '1'
        ORDER BY burning_weight ASC
        """
        results = self.execute_query(query)
        return results if results else []

    def get_refund_settings(self, tenant_id: str) -> Dict[str, Any]:
        """Get refund scheduler settings for tenant"""
        # Connect to central database
        if not self.connect(self.central_db):
            return {}
        
        # Get the property_app_settings value (should be tenant ID)
        property_app_settings = tenant_id
        
        query = """
        SELECT 
          'REFUND SCHEDULER ENABLED' AS INSTELLING,
          CASE 
            WHEN JSON_UNQUOTE(JSON_EXTRACT(data, '$.enable_refund_scheduler')) = 'true' THEN '[X]'
            ELSE '[ ]'
          END AS STATE
        FROM
          tenants
        WHERE id = %s

        UNION ALL

        SELECT 
          'REFUND START DATETIME' AS INSTELLING,
          JSON_UNQUOTE(JSON_EXTRACT(data, '$.refund_start_datetime')) AS STATE
        FROM
          tenants
        WHERE id = %s

        UNION ALL

        SELECT 
          'REFUND END DATETIME' AS INSTELLING,
          JSON_UNQUOTE(JSON_EXTRACT(data, '$.refund_end_datetime')) AS STATE
        FROM
          tenants
        WHERE id = %s
        """
        
        results = self.execute_query(query, (property_app_settings, property_app_settings, property_app_settings))
        
        # Convert results to dictionary
        refund_info = {}
        if results:
            for row in results:
                instelling = row.get('INSTELLING', '')
                state = row.get('STATE', '')
                
                # Format datetime if it's a date field
                if 'DATETIME' in instelling and state:
                    try:
                        # Parse ISO datetime and format to DD-MM-YYYY HH:MM
                        from datetime import datetime
                        if 'T' in str(state):
                            dt = datetime.fromisoformat(str(state).replace('Z', '+00:00'))
                            # Add 2 hours (timezone adjustment)
                            from datetime import timedelta
                            dt = dt + timedelta(hours=2)
                            state = dt.strftime('%d-%m-%Y %H:%M')
                    except:
                        pass  # Keep original value if parsing fails
                
                refund_info[instelling] = state
        
        return refund_info
