<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# AnyKrowd Onboarding QR Code Generator

This is a Python application for generating QR codes for onboarding processes in the AnyKrowd platform.

## Project Context

- **Database**: MySQL on AWS RDS (read-only connection)
- **Purpose**: Generate QR codes for tenant onboarding processes
- **Templates**: Two types - Application onboarding and Guest user onboarding
- **Output**: PDF files with QR codes and relevant information

## Key Components

1. **database.py** - Handles MySQL connection and queries for tenant data, onboarding QRs, and user lookup
2. **qr_generator.py** - Creates QR codes and generates PDF templates using ReportLab
3. **main.py** - Main application flow and user interaction

## Database Schema References

- `domains` table: Contains tenant information with `tenant_id` and `domain` fields
- `onboardings` table: Contains onboarding QR data with relationships to locations, sales, and events
- `users` table: Contains user information for guest QR generation

## QR Code Format

QR codes generate URLs in format: `https://{domain}/?onboardingQrCode={qr_code}#/auth/signuphome`

## Dependencies

- mysql-connector-python: Database connectivity
- qrcode[pil]: QR code generation
- reportlab: PDF template creation
- python-dotenv: Environment variable management

## Development Guidelines

- Always handle database connection errors gracefully
- Provide fallback search mechanisms for tenant lookup
- Generate import files for missing user data
- Use absolute paths for file operations
- Follow the tenant variable format: `tenant-{tenant_id}`
