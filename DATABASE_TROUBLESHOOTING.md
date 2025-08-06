# Database Connectivity Troubleshooting Guide

## Issues Fixed

### 1. Connection Timeout Handling
- **Problem**: MySQL connection timeout errors (10060)
- **Solution**: Added retry logic with 3 attempts and 2-second delays
- **Improvement**: Added specific timeout settings and better error messages

### 2. Network Connectivity Testing
- **Added**: `test_network_connectivity()` method to check if database server is reachable
- **Benefit**: Diagnoses network issues before attempting database operations

### 3. Graceful Error Handling
- **Currencies Section**: Shows "Database connection unavailable" message instead of crashing
- **Refund Settings**: Silently skips if database is unavailable
- **PDF Generation**: Continues with placeholder content when database is unreachable

## Connection Configuration Improvements

### Database Connection Settings
```python
config.update({
    'connection_timeout': 10,  # 10 seconds connection timeout
    'autocommit': True,
    'use_pure': True  # Use pure Python implementation for better compatibility
})
```

### Retry Logic
- **Attempts**: 3 connection attempts with 2-second delays
- **Error Messages**: Clear explanations of potential causes
- **Fallback**: Application continues with limited functionality

## Troubleshooting Steps

### If You Encounter Connection Issues:

1. **Check Network Connectivity**
   ```bash
   python test_connectivity.py
   ```

2. **Common Causes and Solutions**:
   - **VPN Connection**: Ensure you're connected to the required VPN
   - **Firewall**: Check if Windows Firewall or company firewall is blocking port 3306
   - **Internet Connection**: Verify general internet connectivity
   - **AWS RDS Status**: Check if the RDS instance is running and accessible

3. **Error Codes**:
   - **10060**: Connection timeout - usually network/firewall issue
   - **2003**: Cannot connect to MySQL server - server may be down
   - **1045**: Access denied - credentials issue

### Manual Diagnostics

1. **Test Network Connection**:
   ```powershell
   Test-NetConnection anykrowd-production-readonly-2.cy6qqnb1m0nj.eu-west-1.rds.amazonaws.com -Port 3306
   ```

2. **Check DNS Resolution**:
   ```powershell
   nslookup anykrowd-production-readonly-2.cy6qqnb1m0nj.eu-west-1.rds.amazonaws.com
   ```

3. **Test with MySQL Client** (if available):
   ```bash
   mysql -h anykrowd-production-readonly-2.cy6qqnb1m0nj.eu-west-1.rds.amazonaws.com -u [username] -p
   ```

## Application Behavior

### When Database is Available
- ✅ Full functionality with currencies and refund information
- ✅ User lookup and onboarding QR generation
- ✅ Complete PDF generation with all data

### When Database is Unavailable
- ⚠️ PDF generation continues with placeholder messages
- ⚠️ Currencies section shows "Database connection unavailable"
- ⚠️ Refund settings are skipped
- ✅ QR codes are still generated correctly
- ✅ Basic PDF structure is maintained

## Environment Check

Ensure your `.env` file contains:
```
DB_HOST=anykrowd-production-readonly-2.cy6qqnb1m0nj.eu-west-1.rds.amazonaws.com
DB_USER=[your_username]
DB_PASS=[your_password]
```

## Testing Your Setup

Run the connectivity test before using the main application:
```bash
python test_connectivity.py
```

This will verify:
1. Network connectivity to database server
2. Database authentication
3. Query execution capability
4. Tenant database accessibility
