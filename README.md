# AnyKrowd Onboarding QR Code Generator

Professional QR code generator for AnyKrowd onboarding processes with dual template support, WhatsApp integration, and comprehensive automation features.

**Version**: 1.0.0  
**Release Date**: August 2025  
**Status**: Production Ready ✅

---

## 🚀 Features

- **Dual Template Support**: Application and Guest user onboarding templates
- **Professional PDF Generation**: High-quality layouts with corporate branding
- **WhatsApp Integration**: Automatic WhatsApp group QR codes with professional styling
- **Smart User Search**: Email-based user matching with import file generation
- **Database Integration**: MySQL/AWS RDS connectivity with optimized queries
- **Email Validation**: Automatic email cleaning and validation
- **Cache Management**: Intelligent Python cache clearing for development
- **TOPUP Manual Integration**: Automatic second page with TOPUP manual when TOPUP role is detected
- **Comprehensive Logging**: Detailed logging and error tracking
- **Testing Suite**: Complete test coverage for all components
- **Deployment Ready**: Professional deployment scripts and packagingoarding QR Code Generator

Professional QR code generator for AnyKrowd onboarding processes with dual template support and WhatsApp integration.

## 🚀 Features

- **Dual Template Support**: Application and Guest user onboarding templates
- **Professional PDF Generation**: High-quality layouts with corporate branding
- **WhatsApp Integration**: Automatic WhatsApp group QR codes with professional styling
- **Smart User Search**: Email-based user matching with import file generation
- **Database Integration**: MySQL/AWS RDS connectivity with optimized queries
- **Email Validation**: Automatic email cleaning and validation
- **Cache Management**: Intelligent Python cache clearing for development
- **TOPUP Manual Integration**: Automatic second page with TOPUP manual when TOPUP role is detected

## 📋 Templates

### Application Template
- **Purpose**: Kassa/terminal configuration
- **QR Code**: Single onboarding QR code
- **Instructions**: 7-step process for staff setup
- **Branding**: Blue corporate theme (#1E3A8A)
- **TOPUP Support**: Automatic second page with manual when TOPUP role detected

### Guest Template  
- **Purpose**: User-specific configuration
- **QR Codes**: Dual QR codes (Onboarding + User)
- **Instructions**: 5-step simplified process
- **Branding**: Purple guest theme (#6A1B9A)
- **TOPUP Support**: Automatic second page with manual when TOPUP role detected

## 🛠️ Quick Start

### Automated Setup
```bash
# 1. Run the setup script
python setup.py

# 2. Configure your environment
cp .env.example .env
# Edit .env with your database credentials

# 3. Test the installation
python test_application.py

# 4. Run the application
python main.py
```

### Manual Installation

#### Prerequisites
- Python 3.8+
- MySQL database access (AWS RDS)
- Required Python packages (see requirements.txt)

#### Setup Steps
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Verify installation**
   ```bash
   python setup.py
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### Environment Variables (.env)
```env
DB_HOST=your-rds-endpoint.region.rds.amazonaws.com
DB_PORT=3306
DB_DATABASE=your_database_name
DB_USERNAME=your_username
DB_PASSWORD=your_password
OUTPUT_DIRECTORY=output
```

### Database Schema
The application expects these tables:
- `domains`: Tenant information (`tenant_id`, `domain`)
- `onboardings`: QR data with location/sales/event relationships
- `users`: User information for guest QR generation
- `roles`/`roleables`: Role and payment method data

## 🎯 Usage

### Basic Workflow
1. **Start Application**: `python main.py`
2. **Enter Tenant Slug**: Identify the target tenant
3. **Configure WhatsApp**: Optional WhatsApp group integration
4. **Select Template**: Choose Application or Guest template
5. **Generate PDF**: Professional multi-page PDF output

### Template Selection
- **Application (1)**: For terminal/kassa setup
- **Guest (2)**: For user-specific configurations

### WhatsApp Integration
- Optional WhatsApp group QR codes
- Professional green styling (#25D366)
- Conditional support text display

## 📁 Project Structure

```
OnboardingQR/
├── main.py                    # Main application entry point
├── qr_generator.py           # PDF generation and QR code creation
├── database.py               # MySQL database connectivity
├── config.py                 # Application configuration
├── utils.py                  # Utility functions
├── version.py                # Version information and history
├── logging_config.py         # Logging configuration
├── requirements.txt          # Python dependencies
├── setup.py                  # Automated setup script
├── test_application.py       # Comprehensive test suite
├── deploy.py                 # Deployment preparation script
├── .env.example             # Environment configuration template
├── .gitignore               # Git ignore rules
├── README.md                # This documentation
├── TOPUPMANUAL.png          # TOPUP manual image
└── .github/
    └── copilot-instructions.md  # Development guidelines
```

## 🔧 Core Components

### main.py
- Application orchestration
- User interaction handling
- Template selection logic
- Cache management

### qr_generator.py
- PDF generation using ReportLab
- QR code creation with qrcode library
- Professional layout rendering
- WhatsApp QR integration

### database.py
- MySQL connection management
- Optimized query execution
- User search functionality
- Tenant data retrieval

### config.py
- Centralized configuration
- Color schemes and fonts
- Template settings
- Error/success messages

### utils.py
- Email validation and cleaning
- Text processing utilities
- File system operations
- Date/time formatting

## 🎨 Design System

### Colors
- **Application**: Blue theme (#1E3A8A)
- **Guest**: Purple theme (#6A1B9A)  
- **WhatsApp**: Official green (#25D366)
- **Text**: Primary black, secondary gray

### Typography
- **Titles**: Helvetica-Bold 32pt
- **Headers**: Helvetica-Bold 18-20pt
- **Body**: Helvetica 14pt
- **Small**: Helvetica 10-12pt

### Layout
- **QR Codes**: 140x140px with 6px borders
- **WhatsApp QR**: 80x80px with green styling
- **Margins**: 70px standard margins
- **Spacing**: Mathematical proportional spacing

## 🔍 Features Detail

### Smart User Search
- Email pattern matching based on onboarding names
- Automatic email generation: `firstnamelastname@domain.com`
- Special character cleaning and validation
- Import file generation for missing users

### PDF Generation
- Professional A4 layouts (595.27 x 841.89 points)
- Multi-page support with consistent headers/footers
- High-quality QR code rendering
- Corporate branding integration

### WhatsApp Integration
- URL validation for WhatsApp links
- Professional QR styling with borders
- Conditional display logic
- Support text integration

### TOPUP Manual Integration
- Automatic detection of TOPUP role in onboarding data
- Dynamic page count calculation including TOPUP manual pages
- Professional layout with template-specific styling (blue for Application, purple for Guest)
- Image scaling and positioning for optimal display
- Error handling with fallback messages if image is not found
- Consistent footer and branding across all pages

## 📊 Output

### Generated Files
- **PDF Templates**: Multi-page professional layouts
- **Import Files**: CSV for missing user data (`missing_users_import.csv`)
- **Temporary Files**: Auto-cleaned QR code images

### File Structure
```
firstname,lastname,email
John,Doe,johndoe@example.com
Jane,Smith,janesmith@example.com
```

## 🛡️ Error Handling

- **Database Connection**: Graceful failure with clear messages
- **Missing Data**: Import file generation for incomplete records
- **Invalid Input**: Validation with user-friendly feedback
- **File Operations**: Automatic directory creation and cleanup

## 🔄 Development

### Code Quality
- Type hints throughout codebase
- Comprehensive error handling
- Modular architecture
- Professional documentation

### Maintenance
- Centralized configuration
- Utility function library
- Clean separation of concerns
- Version control ready

## 📝 License

Internal AnyKrowd Development Tool - Proprietary

## 👥 Support

For technical support or feature requests, contact the AnyKrowd Development Team.

---

**Version**: 1.0.0  
**Last Updated**: August 2025  
**Developed by**: AnyKrowd Development Team
- **Database Integration**: Connects to AWS RDS MySQL database
- **PDF Generation**: Creates professional PDF templates with QR codes
- **User Data Management**: Handles user lookup and creates import files for missing data

## Requirements

- Python 3.7+
- MySQL database access
- Required Python packages (see requirements.txt)

## Installation

1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables in `.env` file:
   - `DB_HOST`: Database host
   - `DB_USER`: Database username
   - `DB_PASS`: Database password
   - `DB_NAME`: Database name

## Usage

Run the main application:
```bash
python main.py
```

The application will guide you through:
1. Entering the tenant slug
2. Displaying available onboarding QRs
3. Selecting template type (Application or Guest User)
4. Generating QR code templates

## Output

- **PDF Templates**: Generated in the current directory
- **Import Files**: CSV files for missing user data (when applicable)

## Template Types

### 1. Application Onboarding QR
- Basic onboarding information
- QR code linking to signup page
- Suitable for general application access

### 2. Guest User Onboarding QR
- Includes user-specific information
- Searches for existing user data
- Creates import file for missing users
- More detailed template with user context

## Database Schema

The application works with these main tables:
- `domains`: Tenant and domain information
- `onboardings`: QR code data with relationships
- `locations`: Location information
- `sale_catalogues`: Sales catalog data
- `events`: Event information
- `users`: User data for guest templates

## QR Code Format

Generated QR codes create URLs in the format:
```
https://{domain}/?onboardingQrCode={qr_code}#/auth/signuphome
```

## Error Handling

- Database connection failures are handled gracefully
- Missing tenant data triggers fallback searches
- Missing user data creates import files for manual processing
- All errors are logged with descriptive messages

## Security

- Uses read-only database connection
- Environment variables for sensitive configuration
- No sensitive data stored in generated files

## Development

To extend the application:
1. Modify template designs in `qr_generator.py`
2. Add new database queries in `database.py`
3. Extend the main flow in `main.py`

## 🚀 Deployment

### Production Deployment
```bash
# Create deployment package
python deploy.py

# This creates:
# - Deployment directory with all necessary files
# - ZIP archive ready for distribution
# - Deployment instructions
```

### Testing
```bash
# Run comprehensive test suite
python test_application.py

# Verify all components are working
# Tests cover:
# - Environment and dependencies
# - Configuration loading
# - Utility functions
# - QR code generation
# - File operations
```

## Troubleshooting

### Common Issues
- **Database Connection**: Ensure `.env` file is configured correctly
- **Missing Dependencies**: Run `python setup.py` to install requirements
- **Permission Errors**: Check file system permissions for output directory
- **TOPUP Image**: Ensure `TOPUPMANUAL.png` exists in project root

### Logging
The application creates detailed logs that help with troubleshooting:
- Console output for user interaction
- File logs for detailed debugging (when configured)
- Error tracking with stack traces

### Support
For technical support or feature requests, contact the AnyKrowd Development Team.

---

## 📋 Version History

### v1.0.0 (August 2025)
**Features:**
- Initial release with dual template support
- WhatsApp QR code integration
- TOPUP manual automation
- Professional PDF generation
- Smart user search and import file generation
- Cache management system
- Comprehensive error handling

**Fixes:**
- Optimized positioning for instruction sections
- Enhanced template consistency
- Improved text localization

---

**Developed by**: AnyKrowd Development Team  
**License**: Internal AnyKrowd Development Tool - Proprietary  
**Status**: Production Ready ✅
