#!/bin/bash
set -euo pipefail

# Twingate Connector Setup Script for Valargen Staging VM
# This script installs and configures Twingate connector as a systemd service
# For Docker Compose integration, see docker-compose.staging.yml

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   log_error "This script must be run as root (use sudo)"
   exit 1
fi

# Check for required environment variables
if [[ -z "${TWINGATE_ACCESS_TOKEN:-}" ]]; then
    log_error "TWINGATE_ACCESS_TOKEN environment variable is not set"
    log_info "Export it before running this script:"
    log_info "  export TWINGATE_ACCESS_TOKEN='your-token-here'"
    log_info ""
    log_info "To obtain the token:"
    log_info "  1. Log in to Twingate Admin Console: https://app.twingate.com"
    log_info "  2. Navigate to: Networks → Your Network → Connectors → Add Connector"
    log_info "  3. Generate and copy the Access Token"
    exit 1
fi

if [[ -z "${TWINGATE_NETWORK:-}" ]]; then
    log_error "TWINGATE_NETWORK environment variable is not set"
    log_info "Export it before running this script:"
    log_info "  export TWINGATE_NETWORK='your-network-name'"
    log_info ""
    log_info "To find your network name:"
    log_info "  1. Log in to Twingate Admin Console: https://app.twingate.com"
    log_info "  2. Navigate to: Networks"
    log_info "  3. Your network name is displayed (e.g., 'valargen-staging')"
    exit 1
fi

# Optional: Connector label
TWINGATE_LABEL="${TWINGATE_LABEL:-valargen-staging}"

log_info "Starting Twingate connector setup..."
log_info "Network: ${TWINGATE_NETWORK}"
log_info "Label: ${TWINGATE_LABEL}"

# Check if Docker is installed
if command -v docker &> /dev/null; then
    log_info "Docker is installed. You can use Docker Compose for connector deployment."
    log_info "See docker-compose.staging.yml for Docker-based deployment."
    read -p "Continue with systemd installation anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Setup cancelled. Use Docker Compose for easier management:"
        log_info "  docker compose -f docker-compose.yml -f docker-compose.staging.yml up -d valargen-twingate-connector"
        exit 0
    fi
fi

# Detect OS and architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

log_info "Detected OS: ${OS}"
log_info "Detected Architecture: ${ARCH}"

# Map architecture to Twingate's naming
case ${ARCH} in
    x86_64)
        TWINGATE_ARCH="amd64"
        ;;
    aarch64|arm64)
        TWINGATE_ARCH="arm64"
        ;;
    armv7l)
        TWINGATE_ARCH="armv7"
        ;;
    *)
        log_error "Unsupported architecture: ${ARCH}"
        exit 1
        ;;
esac

# Install based on OS
case ${OS} in
    linux)
        log_info "Installing Twingate connector for Linux..."

        # Check Linux distribution
        if [[ -f /etc/os-release ]]; then
            . /etc/os-release
            DISTRO=$ID
        else
            log_error "Cannot detect Linux distribution"
            exit 1
        fi

        case ${DISTRO} in
            ubuntu|debian)
                log_info "Installing on Debian/Ubuntu..."

                # Add Twingate repository
                log_info "Adding Twingate repository..."
                curl -fsSL https://binaries.twingate.com/client/linux/install.sh | bash

                # Install connector package
                log_info "Installing twingate-connector package..."
                apt-get update
                apt-get install -y twingate-connector
                ;;

            centos|rhel|fedora)
                log_info "Installing on RHEL/CentOS/Fedora..."

                # Add Twingate repository
                log_info "Adding Twingate repository..."
                curl -fsSL https://binaries.twingate.com/client/linux/install.sh | bash

                # Install connector package
                log_info "Installing twingate-connector package..."
                yum install -y twingate-connector || dnf install -y twingate-connector
                ;;

            *)
                log_warn "Unsupported distribution: ${DISTRO}"
                log_info "Attempting generic installation..."
                curl -fsSL https://binaries.twingate.com/client/linux/install.sh | bash
                ;;
        esac
        ;;

    *)
        log_error "Unsupported OS: ${OS}"
        log_error "This script supports Linux only."
        log_info "For other platforms, use Docker Compose:"
        log_info "  docker compose -f docker-compose.yml -f docker-compose.staging.yml up -d valargen-twingate-connector"
        exit 1
        ;;
esac

# Configure connector
log_info "Configuring Twingate connector..."

# Create configuration directory if it doesn't exist
mkdir -p /etc/twingate

# Write configuration file
cat > /etc/twingate/connector.conf <<EOF
TWINGATE_ACCESS_TOKEN=${TWINGATE_ACCESS_TOKEN}
TWINGATE_NETWORK=${TWINGATE_NETWORK}
TWINGATE_LABEL=${TWINGATE_LABEL}
EOF

# Secure the configuration file
chmod 600 /etc/twingate/connector.conf
chown root:root /etc/twingate/connector.conf

log_info "Configuration written to /etc/twingate/connector.conf"

# Create systemd service file
log_info "Creating systemd service..."

cat > /etc/systemd/system/twingate-connector.service <<EOF
[Unit]
Description=Twingate Connector
Documentation=https://docs.twingate.com
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
EnvironmentFile=/etc/twingate/connector.conf
ExecStart=/usr/bin/twingate-connector start
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits
MemoryLimit=128M
CPUQuota=25%

# Security
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
log_info "Reloading systemd daemon..."
systemctl daemon-reload

# Enable service to start on boot
log_info "Enabling twingate-connector service..."
systemctl enable twingate-connector

# Start service
log_info "Starting twingate-connector service..."
systemctl start twingate-connector

# Wait a few seconds for service to initialize
sleep 5

# Check service status
log_info "Checking connector status..."
if systemctl is-active --quiet twingate-connector; then
    log_info "✓ Twingate connector is running!"

    # Display service status
    systemctl status twingate-connector --no-pager | head -20

    log_info ""
    log_info "✓ Setup complete!"
    log_info ""
    log_info "Next steps:"
    log_info "  1. Verify connector is online in Twingate Admin Console:"
    log_info "     https://app.twingate.com → Networks → ${TWINGATE_NETWORK} → Connectors"
    log_info ""
    log_info "  2. Configure resources (SSH, web app) in Twingate Admin Console"
    log_info ""
    log_info "  3. Assign access policies to users/groups"
    log_info ""
    log_info "  4. Update Azure NSG rules to restrict SSH access"
    log_info ""
    log_info "Useful commands:"
    log_info "  - Check status: sudo systemctl status twingate-connector"
    log_info "  - View logs:    sudo journalctl -u twingate-connector -f"
    log_info "  - Restart:      sudo systemctl restart twingate-connector"
    log_info "  - Stop:         sudo systemctl stop twingate-connector"
    log_info ""
    log_info "See docs/TWINGATE.md for complete documentation."
else
    log_error "✗ Twingate connector failed to start"
    log_error "Check logs for details:"
    log_error "  sudo journalctl -u twingate-connector -n 50"
    exit 1
fi
