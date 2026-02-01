#!/bin/bash
#
# Valargen SSH Setup & Tunnel
#

set -e

KEY_PATH="$HOME/.ssh/id_ed25519_valargen"
SSH_CONFIG="$HOME/.ssh/config"
PREF_FILE="$HOME/.ssh/.valargen_pref"
ROLE_FILE="$HOME/.ssh/.valargen_role"
HOST_ALIAS="valargen-staging-tunnel"
IPV6_ADDRESS="2603:1030:20e:1::5"
STATIC_IP="4.227.184.143"
SSH_TIMEOUT=15
PROXY_PORT=1080
DB_LOCAL_PORT=5433
DB_REMOTE_HOST="10.0.0.4"
DB_REMOTE_PORT=5432
# Bind address for SOCKS proxy:
# - 127.0.0.1 (localhost only) - Secure, Postman/local apps work
# - 0.0.0.0 (all interfaces) - Docker containers can access
BIND_ADDRESS="0.0.0.0"
CONNECTION_METHOD=""
USER_ROLE=""

# Role-based usernames
ROLE_TUNNEL="vg-tunnel"
ROLE_ADMIN="vg-admin"
ROLE_SUPER="vg-super"
SSH_USER=""

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
BLINK='\033[5m'; BOLD='\033[1m'; REVERSE='\033[7m'; UNDERLINE='\033[4m'

info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
err()   { echo -e "${RED}[ERROR]${NC} $1"; }
attention() { echo -e "${BLINK}${BOLD}${REVERSE}${YELLOW} $1 ${NC}"; }

# Auto-detect IPv6 connectivity
detect_ipv6_support() {
    # Check if system has IPv6 enabled
    if [[ ! -f /proc/net/if_inet6 ]] && [[ "$(uname -s)" != "Darwin" ]]; then
        return 1
    fi

    # Try to reach the IPv6 address via ping
    if command -v ping6 &>/dev/null; then
        ping6 -c 1 -W 3 "$IPV6_ADDRESS" &>/dev/null && return 0
    elif ping -6 -c 1 -W 3 "$IPV6_ADDRESS" &>/dev/null 2>&1; then
        return 0
    fi

    # Alternative: try SSH connection test using -N (works for tunnel-only accounts)
    # Tunnel-only accounts return "This account is currently not available" but connection succeeds
    timeout 5 ssh -o ConnectTimeout=3 -o BatchMode=yes -o HostName="$IPV6_ADDRESS" -N "$HOST_ALIAS" &
    local pid=$!
    sleep 2
    if kill -0 $pid 2>/dev/null; then
        kill $pid 2>/dev/null
        wait $pid 2>/dev/null
        return 0
    fi
    wait $pid 2>/dev/null
    # Check if it failed due to "not available" (which means auth succeeded)
    local result=$(timeout 5 ssh -o ConnectTimeout=3 -o BatchMode=yes -o HostName="$IPV6_ADDRESS" "$HOST_ALIAS" exit 2>&1)
    if [[ "$result" == *"not available"* ]]; then
        return 0  # Auth succeeded, account is just restricted
    fi

    return 1
}

# Auto-detect IPv4 connectivity
detect_ipv4_support() {
    # Try to reach the static IP via ping
    if ping -c 1 -W 3 "$STATIC_IP" &>/dev/null 2>&1; then
        return 0
    fi

    # Alternative: try SSH connection test using -N (works for tunnel-only accounts)
    # Tunnel-only accounts return "This account is currently not available" but connection succeeds
    timeout 5 ssh -o ConnectTimeout=3 -o BatchMode=yes -o HostName="$STATIC_IP" -N "$HOST_ALIAS" &
    local pid=$!
    sleep 2
    if kill -0 $pid 2>/dev/null; then
        kill $pid 2>/dev/null
        wait $pid 2>/dev/null
        return 0
    fi
    wait $pid 2>/dev/null
    # Check if it failed due to "not available" (which means auth succeeded)
    local result=$(timeout 5 ssh -o ConnectTimeout=3 -o BatchMode=yes -o HostName="$STATIC_IP" "$HOST_ALIAS" exit 2>&1)
    if [[ "$result" == *"not available"* ]]; then
        return 0  # Auth succeeded, account is just restricted
    fi

    return 1
}

# Auto-detect best connection method
auto_detect_connection() {
    info "Auto-detecting network connectivity..."

    local ipv6_ok=false
    local ipv4_ok=false

    # Test IPv6 first (preferred)
    info "Testing IPv6 connectivity to $IPV6_ADDRESS..."
    if detect_ipv6_support; then
        ok "IPv6 connectivity available"
        ipv6_ok=true
    else
        warn "IPv6 not available"
    fi

    # Test IPv4
    info "Testing IPv4 connectivity to $STATIC_IP..."
    if detect_ipv4_support; then
        ok "IPv4 connectivity available"
        ipv4_ok=true
    else
        warn "IPv4 not available"
    fi

    # Determine best method
    if $ipv6_ok; then
        CONNECTION_METHOD="ipv6"
        echo "ipv6" > "$PREF_FILE"
        ok "Auto-selected: IPv6 (Direct)"
        return 0
    elif $ipv4_ok; then
        CONNECTION_METHOD="direct"
        echo "direct" > "$PREF_FILE"
        ok "Auto-selected: IPv4 (Direct)"
        return 0
    else
        err "No connectivity available to server"
        return 1
    fi
}

# Resolve and verify hostname (quiet mode by default)
resolve_hostname() {
    local hostname=$1
    local verbose=${2:-false}

    [[ "$verbose" == "true" ]] && info "Resolving hostname: $hostname"

    # If using IP address directly, just verify it's valid
    if [[ "$hostname" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] || [[ "$hostname" =~ : ]]; then
        [[ "$verbose" == "true" ]] && ok "Using IP address directly"
        return 0
    fi

    # Try nslookup
    if command -v nslookup &>/dev/null; then
        if nslookup "$hostname" &>/dev/null; then
            [[ "$verbose" == "true" ]] && ok "Hostname resolved successfully"
            return 0
        fi
    fi

    # Try host command
    if command -v host &>/dev/null; then
        if host "$hostname" &>/dev/null; then
            [[ "$verbose" == "true" ]] && ok "Hostname resolved successfully"
            return 0
        fi
    fi

    # Try getent
    if command -v getent &>/dev/null; then
        if getent hosts "$hostname" &>/dev/null; then
            [[ "$verbose" == "true" ]] && ok "Hostname resolved successfully"
            return 0
        fi
    fi

    # Try ping as last resort (will resolve hostname)
    if ping -c 1 -W 2 "$hostname" &>/dev/null 2>&1; then
        [[ "$verbose" == "true" ]] && ok "Hostname resolved via ping"
        return 0
    fi

    [[ "$verbose" == "true" ]] && warn "Could not resolve hostname: $hostname"
    return 1
}

# Check if SSH config has active (non-commented) entry for host
has_active_ssh_config() {
    if [[ -f "$SSH_CONFIG" ]]; then
        # Match non-commented "Host <alias>" line
        grep -q "^Host $HOST_ALIAS$" "$SSH_CONFIG" 2>/dev/null && return 0
        grep -q "^Host $HOST_ALIAS " "$SSH_CONFIG" 2>/dev/null && return 0
    fi
    return 1
}

# Check and fix SSH key permissions
check_key_permissions() {
    if [[ ! -f "$KEY_PATH" ]]; then
        return 1
    fi

    local perms=$(stat -c "%a" "$KEY_PATH" 2>/dev/null || stat -f "%Lp" "$KEY_PATH" 2>/dev/null)

    if [[ "$perms" != "600" ]]; then
        warn "SSH key has incorrect permissions: $perms (should be 600)"
        info "Fixing permissions..."
        chmod 600 "$KEY_PATH"
        if [[ $? -eq 0 ]]; then
            ok "Fixed SSH key permissions to 600"
        else
            err "Failed to fix permissions. Run: chmod 600 $KEY_PATH"
            return 1
        fi
    fi

    # Also check public key permissions (should be 644 or 600)
    if [[ -f "${KEY_PATH}.pub" ]]; then
        local pub_perms=$(stat -c "%a" "${KEY_PATH}.pub" 2>/dev/null || stat -f "%Lp" "${KEY_PATH}.pub" 2>/dev/null)
        if [[ "$pub_perms" != "644" ]] && [[ "$pub_perms" != "600" ]]; then
            chmod 644 "${KEY_PATH}.pub" 2>/dev/null
        fi
    fi

    return 0
}

# Display key with attention-grabbing formatting
display_key_attention() {
    local key_content=$(cat "${KEY_PATH}.pub" 2>/dev/null)

    echo ""
    echo ""
    echo -e "${BLINK}${BOLD}${RED}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLINK}${BOLD}${RED}║                                                                  ║${NC}"
    echo -e "${BLINK}${BOLD}${RED}║   ⚠️  ATTENTION: COPY THIS KEY AND SEND TO ADMINISTRATOR  ⚠️     ║${NC}"
    echo -e "${BLINK}${BOLD}${RED}║                                                                  ║${NC}"
    echo -e "${BLINK}${BOLD}${RED}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BOLD}${GREEN}Your SSH Public Key:${NC}"
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}$key_content${NC}"
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════════${NC}"
    echo ""

    # Auto-copy to clipboard
    local copied=false
    if command -v pbcopy &>/dev/null; then
        echo "$key_content" | pbcopy && copied=true
    elif command -v xclip &>/dev/null; then
        echo "$key_content" | xclip -selection clipboard && copied=true
    elif command -v xsel &>/dev/null; then
        echo "$key_content" | xsel --clipboard && copied=true
    fi

    if $copied; then
        echo -e "${GREEN}${BOLD}✓ KEY AUTOMATICALLY COPIED TO CLIPBOARD${NC}"
    else
        attention "⚠️  MANUALLY COPY THE KEY ABOVE ⚠️"
    fi

    echo ""
    echo -e "${BOLD}${YELLOW}Next Steps:${NC}"
    echo -e "  1. ${BOLD}Send this key to your administrator${NC}"
    echo -e "  2. Wait for confirmation that your key has been added"
    echo -e "  3. Run this script again to connect"
    echo ""
    echo -e "${RED}${BOLD}⚠️  NEVER share your private key (without .pub)!${NC}"
    echo ""
}

# Help
show_help() {
    local script=$(basename "$0")
    cat << EOF
Valargen SSH Setup & Tunnel

Usage: $script [COMMAND]

Commands:
  (none)                                  Auto-setup + auto-detect IPv6/IPv4 + start tunnel
      Example: $script
      - Generates SSH key if missing (displays for admin)
      - Auto-detects best connection (IPv6 preferred, IPv4 fallback)
      - Configures SSH and starts tunnel automatically

  tunnel                                  Start SOCKS proxy tunnel for Postman (port $PROXY_PORT)
      Example: $script tunnel

  kill                                    Stop existing tunnel on port $PROXY_PORT
      Example: $script kill

  restart                                 Stop existing tunnel and start new one
      Example: $script restart

  setup                                   Interactive setup wizard (prompts for choices)
      Example: $script setup

  auto                                    Force automated setup (no prompts where possible)
      Example: $script auto

  switch                                  Switch connection method (IPv6/IPv4)
      Example: $script switch

  reset                                   Reset account - remove all configuration
      Example: $script reset

  showkey                                 Display your public SSH key (attention-grabbing format)
      Example: $script showkey

  showip                                  Display configured server IPs and current mode
      Example: $script showip

  updateip                                Update configured server IP address
      Example: $script updateip

  status                                  Check connection status and requirements
      Example: $script status

  diagnose                                Run client machine diagnostics before setup
      Example: $script diagnose

  db                                      Start PostgreSQL tunnel for DBeaver/pgAdmin (port $DB_LOCAL_PORT)
      Example: $script db

  db-kill                                 Stop PostgreSQL database tunnel
      Example: $script db-kill

  help                                    Show this help message
      Example: $script help

First-Time Client Setup:
  1. Run: $script
  2. Copy the displayed SSH public key (auto-copied to clipboard)
  3. Send the key to your administrator
  4. Wait for admin to confirm key is added
  5. Run the script again to connect automatically

Postman Proxy Setup:
  1. Run: $script tunnel
  2. Postman > Settings > Proxy > SOCKS5 > 127.0.0.1:$PROXY_PORT

Docker Access:
  By default, tunnel binds to localhost only (secure).
  To allow Docker containers access, edit this script and set:
    BIND_ADDRESS="0.0.0.0"
  Then ensure firewall blocks external access to port $PROXY_PORT.

Files:
  SSH Key:    $KEY_PATH
  SSH Config: $SSH_CONFIG

EOF
    exit 0
}

# Check if port is in use
check_port() {
    if lsof -i :$PROXY_PORT &>/dev/null || ss -tuln 2>/dev/null | grep -q ":$PROXY_PORT "; then
        err "Port $PROXY_PORT is already in use"
        info "Run '$(basename "$0") kill' to stop existing tunnel"
        exit 1
    fi
}

# Kill existing tunnel
kill_tunnel() {
    info "Stopping tunnel on port $PROXY_PORT..."

    local pid=""
    if command -v lsof &>/dev/null; then
        pid=$(lsof -ti :$PROXY_PORT 2>/dev/null)
    elif command -v ss &>/dev/null; then
        pid=$(ss -tlnp 2>/dev/null | grep ":$PROXY_PORT " | grep -oP 'pid=\K\d+')
    fi

    if [[ -n "$pid" ]]; then
        kill $pid 2>/dev/null && ok "Tunnel stopped (PID: $pid)" || err "Failed to stop tunnel"
    else
        warn "No tunnel running on port $PROXY_PORT"
    fi
}

# Reset account - remove all configuration
reset_account() {
    echo -e "${RED}=== RESET ACCOUNT ===${NC}\n"
    warn "This will remove all Valargen SSH configuration"
    echo ""

    echo -en "${RED}Are you sure? This cannot be undone (y/n): ${NC}"
    read confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        info "Reset cancelled"
        exit 0
    fi

    echo ""
    info "Resetting account..."

    # Kill tunnel
    local pid=""
    if command -v lsof &>/dev/null; then
        pid=$(lsof -ti :$PROXY_PORT 2>/dev/null) || true
    elif command -v ss &>/dev/null; then
        pid=$(ss -tlnp 2>/dev/null | grep ":$PROXY_PORT " | grep -oP 'pid=\K\d+') || true
    fi

    if [[ -n "$pid" ]]; then
        kill $pid 2>/dev/null && ok "Tunnel stopped" || true
    fi

    # Remove SSH key
    if [[ -f "$KEY_PATH" ]]; then
        rm -f "$KEY_PATH" "${KEY_PATH}.pub"
        ok "Removed SSH key: $KEY_PATH"
    fi

    # Remove preference file
    if [[ -f "$PREF_FILE" ]]; then
        rm -f "$PREF_FILE"
        ok "Removed connection preference"
    fi

    # Remove role file
    if [[ -f "$ROLE_FILE" ]]; then
        rm -f "$ROLE_FILE"
        ok "Removed role preference"
    fi

    # Remove SSH config entry
    if [[ -f "$SSH_CONFIG" ]]; then
        if grep -q "Host $HOST_ALIAS" "$SSH_CONFIG" 2>/dev/null; then
            sed -i.bak "/Host $HOST_ALIAS/,/ServerAliveCountMax/d" "$SSH_CONFIG"
            ok "Removed SSH config entry for $HOST_ALIAS"
            [[ -f "${SSH_CONFIG}.bak" ]] && rm "${SSH_CONFIG}.bak"
        fi
    fi

    # Remove known_hosts entries
    local known_hosts="$HOME/.ssh/known_hosts"
    if [[ -f "$known_hosts" ]]; then
        ssh-keygen -R "$STATIC_IP" &>/dev/null && ok "Removed known_hosts entry for $STATIC_IP" || true
        ssh-keygen -R "$IPV6_ADDRESS" &>/dev/null && ok "Removed known_hosts entry for $IPV6_ADDRESS" || true
    fi

    # Remove Twingate
    if [[ "$(uname -s)" == "Linux" ]]; then
        if command -v twingate &>/dev/null; then
            echo ""
            read -p "Remove Twingate? (y/n): " remove_twingate
            if [[ "$remove_twingate" =~ ^[Yy]$ ]]; then
                info "Removing Twingate..."
                if command -v apt &>/dev/null; then
                    sudo apt remove -y twingate 2>/dev/null && ok "Twingate removed" || warn "Failed to remove Twingate"
                elif command -v dnf &>/dev/null; then
                    sudo dnf remove -y twingate 2>/dev/null && ok "Twingate removed" || warn "Failed to remove Twingate"
                elif command -v yum &>/dev/null; then
                    sudo yum remove -y twingate 2>/dev/null && ok "Twingate removed" || warn "Failed to remove Twingate"
                else
                    warn "Could not detect package manager. Remove Twingate manually."
                fi
            fi
        fi
    elif [[ "$(uname -s)" == "Darwin" ]]; then
        if [[ -d "/Applications/Twingate.app" ]] || pgrep -x "Twingate" &>/dev/null; then
            echo ""
            read -p "Remove Twingate? (y/n): " remove_twingate
            if [[ "$remove_twingate" =~ ^[Yy]$ ]]; then
                info "Stopping Twingate..."
                pkill -x "Twingate" 2>/dev/null || true
                if [[ -d "/Applications/Twingate.app" ]]; then
                    rm -rf "/Applications/Twingate.app" 2>/dev/null && ok "Twingate removed from Applications" || warn "Failed to remove. Try: sudo rm -rf /Applications/Twingate.app"
                fi
                # Remove Twingate user data
                rm -rf "$HOME/Library/Application Support/Twingate" 2>/dev/null
                rm -rf "$HOME/Library/Caches/com.twingate.macos" 2>/dev/null
                ok "Twingate data cleaned"
            fi
        fi
    fi

    echo ""
    ok "Account reset complete"
    info "Run '$(basename "$0")' to setup again"
}

# Check if all requirements are met
check_requirements() {
    local missing=0

    [[ ! -f "$KEY_PATH" ]] && { warn "SSH key not found"; missing=1; }

    if has_active_ssh_config; then
        : # Config exists
    else
        warn "SSH config not found for $HOST_ALIAS"
        missing=1
    fi

    if [[ "$(uname -s)" == "Linux" ]]; then
        command -v twingate &>/dev/null || { warn "Twingate not installed"; missing=1; }
    fi

    return $missing
}

# Generate SSH key (auto-generates with hostname-based email if not provided)
setup_key() {
    mkdir -p "$HOME/.ssh" && chmod 700 "$HOME/.ssh"

    # Auto-generate email from username and hostname
    local auto_email="${USER:-$(whoami)}@$(hostname -f 2>/dev/null || hostname)"
    local email="$auto_email"

    # Only ask for email in interactive mode
    if [[ -t 0 ]]; then
        echo ""
        echo -en "${BLUE}Enter your email (for key comment) [${auto_email}]: ${NC}"
        read user_email
        [[ -n "$user_email" ]] && email="$user_email"
    fi

    echo ""
    info "Generating SSH key..."
    ssh-keygen -t ed25519 -C "$email" -f "$KEY_PATH" -N "" -q
    chmod 600 "$KEY_PATH"

    echo ""
    ok "SSH key generated!"

    # Display key with attention-grabbing format
    display_key_attention

    # In non-interactive mode, just exit after showing key
    if [[ ! -t 0 ]]; then
        info "Non-interactive mode: Key generated. Share with admin and re-run."
        exit 0
    fi

    read -p "Press Enter after admin confirms your key is added..."
}

# Install Twingate
setup_twingate() {
    if [[ "$(uname -s)" == "Darwin" ]]; then
        info "Install Twingate from App Store: https://apps.apple.com/app/twingate/id1501592214"
        read -p "Press Enter after installing..."
    else
        read -p "Install Twingate? (y/n): " install
        [[ "$install" =~ ^[Yy]$ ]] && curl -s https://binaries.twingate.com/client/linux/install.sh | sudo bash
    fi

    echo ""
    info "Connect Twingate to network: valargen-staging-internal"
    read -p "Press Enter after connected..."
}

# Configure SSH
setup_config() {
    info "Configuring SSH..."
    mkdir -p "$HOME/.ssh"

    # Remove existing entry (including commented ones) to avoid duplicates
    if [[ -f "$SSH_CONFIG" ]]; then
        # Remove commented entries
        sed -i.bak "/^#.*Host $HOST_ALIAS/,/^#.*ServerAliveCountMax/d" "$SSH_CONFIG" 2>/dev/null
        # Remove non-commented entries
        sed -i.bak "/^Host $HOST_ALIAS/,/ServerAliveCountMax/d" "$SSH_CONFIG" 2>/dev/null
        [[ -f "${SSH_CONFIG}.bak" ]] && rm -f "${SSH_CONFIG}.bak"
    fi

    cat >> "$SSH_CONFIG" << EOF

Host $HOST_ALIAS
    HostName $STATIC_IP
    User $SSH_USER
    IdentityFile $KEY_PATH
    ConnectTimeout $SSH_TIMEOUT
    ServerAliveInterval 60
    ServerAliveCountMax 3
EOF

    chmod 600 "$SSH_CONFIG"
    ok "SSH config added"

    # Add host keys to known_hosts
    info "Adding server host keys..."
    ssh-keyscan -H "$STATIC_IP" >> "$HOME/.ssh/known_hosts" 2>/dev/null && ok "Host key added for $STATIC_IP"
    ssh-keyscan -H "$IPV6_ADDRESS" >> "$HOME/.ssh/known_hosts" 2>/dev/null && ok "Host key added for $IPV6_ADDRESS"
}

# Ask connection method
ask_connection_method() {
    echo -e "${GREEN}=== Connection Method ===${NC}\n"
    echo "How do you want to connect to Valargen?"
    echo ""
    echo "1) IPv6 - Direct IPv6 connection (recommended)"
    echo "   Uses IPv6: $IPV6_ADDRESS"
    echo ""
    echo "2) Direct SSH - No VPN required"
    echo "   Uses static IP: $STATIC_IP"
    echo ""
    read -p "Select [1/2]: " choice

    case "$choice" in
        1)
            CONNECTION_METHOD="ipv6"
            echo "ipv6" > "$PREF_FILE"
            ok "Selected: IPv6 (Direct)"
            ;;
        2)
            CONNECTION_METHOD="direct"
            echo "direct" > "$PREF_FILE"
            ok "Selected: Direct SSH"
            ;;
        *)
            err "Invalid choice"
            exit 1
            ;;
    esac
    echo ""
}

# Load saved preference
load_preference() {
    if [[ -f "$PREF_FILE" ]]; then
        CONNECTION_METHOD=$(cat "$PREF_FILE")
    fi
}

# Load saved role
load_role() {
    if [[ -f "$ROLE_FILE" ]]; then
        USER_ROLE=$(cat "$ROLE_FILE")
        case "$USER_ROLE" in
            tunnel) SSH_USER="$ROLE_TUNNEL" ;;
            admin)  SSH_USER="$ROLE_ADMIN" ;;
            super)  SSH_USER="$ROLE_SUPER" ;;
            *)      SSH_USER="$ROLE_TUNNEL" ;;
        esac
    fi
}

# Ask for role selection (used in interactive setup)
ask_role() {
    echo -e "${GREEN}=== Select Access Level ===${NC}\n"
    echo "1) tunnel  - API/Postman access only (recommended)"
    echo "   User: $ROLE_TUNNEL | No shell access"
    echo ""
    echo "2) admin   - Developer access"
    echo "   User: $ROLE_ADMIN | Limited shell access"
    echo ""
    echo "3) super   - Full admin access"
    echo "   User: $ROLE_SUPER | Full shell access"
    echo ""
    read -p "Select [1/2/3]: " choice

    case "$choice" in
        1)
            USER_ROLE="tunnel"
            SSH_USER="$ROLE_TUNNEL"
            echo "tunnel" > "$ROLE_FILE"
            ok "Selected: Tunnel (API access only)"
            ;;
        2)
            USER_ROLE="admin"
            SSH_USER="$ROLE_ADMIN"
            echo "admin" > "$ROLE_FILE"
            ok "Selected: Admin (Developer access)"
            ;;
        3)
            USER_ROLE="super"
            SSH_USER="$ROLE_SUPER"
            echo "super" > "$ROLE_FILE"
            ok "Selected: Super (Full admin access)"
            ;;
        *)
            err "Invalid choice"
            exit 1
            ;;
    esac
    echo ""
}

# Switch connection method
switch_method() {
    load_preference

    echo -e "${GREEN}=== Switch Connection Method ===${NC}\n"

    if [[ -n "$CONNECTION_METHOD" ]]; then
        info "Current method: $CONNECTION_METHOD"
    else
        info "Current method: not set"
    fi
    echo ""

    echo "1) IPv6 - Direct IPv6 connection: $IPV6_ADDRESS"
    echo "2) IPv4 - Static IP: $STATIC_IP"
    echo ""
    read -p "Select [1/2]: " choice

    case "$choice" in
        1)
            echo "ipv6" > "$PREF_FILE"
            # Update SSH config to use IPv6
            if [[ -f "$SSH_CONFIG" ]] && grep -q "Host $HOST_ALIAS" "$SSH_CONFIG" 2>/dev/null; then
                sed -i.bak "s/HostName .*/HostName $IPV6_ADDRESS/" "$SSH_CONFIG" 2>/dev/null || \
                sed -i '' "s/HostName .*/HostName $IPV6_ADDRESS/" "$SSH_CONFIG"
                [[ -f "${SSH_CONFIG}.bak" ]] && rm "${SSH_CONFIG}.bak"
                ok "Updated SSH config to use: $IPV6_ADDRESS"
            fi
            ok "Switched to: IPv6 (Direct)"
            ;;
        2)
            echo "direct" > "$PREF_FILE"
            # Update SSH config to use static IP
            if [[ -f "$SSH_CONFIG" ]] && grep -q "Host $HOST_ALIAS" "$SSH_CONFIG" 2>/dev/null; then
                sed -i.bak "s/HostName .*/HostName $STATIC_IP/" "$SSH_CONFIG" 2>/dev/null || \
                sed -i '' "s/HostName .*/HostName $STATIC_IP/" "$SSH_CONFIG"
                [[ -f "${SSH_CONFIG}.bak" ]] && rm "${SSH_CONFIG}.bak"
                ok "Updated SSH config to use: $STATIC_IP"
            fi
            ok "Switched to: Direct SSH"
            ;;
        *)
            err "Invalid choice"
            exit 1
            ;;
    esac
}

# Show public key
show_key() {
    if [[ ! -f "${KEY_PATH}.pub" ]]; then
        err "Public key not found: ${KEY_PATH}.pub"
        info "Run '$(basename "$0") setup' to generate a new key"
        exit 1
    fi

    # Use the attention-grabbing display
    display_key_attention
}

# Show configured server IPs
show_ip() {
    echo -e "${GREEN}=== Configured Server IPs ===${NC}\n"

    load_preference
    load_role

    echo "Static IP (Direct SSH):     $STATIC_IP"
    echo "IPv6 Address:               $IPV6_ADDRESS"
    echo ""

    if [[ "$CONNECTION_METHOD" == "direct" ]]; then
        ok "Current mode: IPv4 Direct (using $STATIC_IP)"
    elif [[ "$CONNECTION_METHOD" == "ipv6" ]]; then
        ok "Current mode: IPv6 (using $IPV6_ADDRESS)"
    else
        info "Current mode: Not set"
    fi

    # Show current role
    if [[ -n "$USER_ROLE" ]]; then
        ok "Current role: $USER_ROLE (user: $SSH_USER)"
    else
        info "Current role: Not set"
    fi

    # Show what's in SSH config
    if [[ -f "$SSH_CONFIG" ]] && grep -q "Host $HOST_ALIAS" "$SSH_CONFIG" 2>/dev/null; then
        local config_ip=$(grep -A1 "Host $HOST_ALIAS" "$SSH_CONFIG" | grep "HostName" | awk '{print $2}')
        local config_user=$(grep -A2 "Host $HOST_ALIAS" "$SSH_CONFIG" | grep "User" | awk '{print $2}')
        if [[ -n "$config_ip" ]]; then
            echo ""
            info "SSH config HostName: $config_ip"
            info "SSH config User: $config_user"
        fi
    fi
}

# Update configured IP address
update_ip() {
    echo -e "${GREEN}=== Update Server IP ===${NC}\n"

    info "Current Configuration:"
    info "  Static IP (Direct):     $STATIC_IP"
    info "  IPv6 Address: $IPV6_ADDRESS"
    echo ""

    echo "Which IP do you want to update?"
    echo "1) Static IP (IPv4)"
    echo "2) IPv6 Address"
    echo ""
    read -p "Select [1/2]: " choice

    case "$choice" in
        1)
            read -p "Enter new Static IP: " new_ip
            if [[ -z "$new_ip" ]]; then
                err "IP address cannot be empty"
                exit 1
            fi

            # Update SSH config if it exists
            if [[ -f "$SSH_CONFIG" ]] && grep -q "Host $HOST_ALIAS" "$SSH_CONFIG" 2>/dev/null; then
                # Get current connection method
                load_preference
                if [[ "$CONNECTION_METHOD" == "direct" ]]; then
                    sed -i.bak "s/HostName $STATIC_IP/HostName $new_ip/" "$SSH_CONFIG" 2>/dev/null || \
                    sed -i '' "s/HostName $STATIC_IP/HostName $new_ip/" "$SSH_CONFIG"
                    [[ -f "${SSH_CONFIG}.bak" ]] && rm "${SSH_CONFIG}.bak"
                    ok "Updated SSH config with new Static IP: $new_ip"
                else
                    ok "Static IP updated to: $new_ip"
                    info "SSH config uses IPv6 address"
                    info "Switch to IPv4 mode to use this IP"
                fi
            fi

            # Update script variable for this session
            STATIC_IP="$new_ip"
            ok "Static IP set to: $new_ip"
            warn "Note: To make this permanent, update STATIC_IP in the script"
            ;;
        2)
            read -p "Enter new Internal IP: " new_ip
            if [[ -z "$new_ip" ]]; then
                err "IP address cannot be empty"
                exit 1
            fi

            # Update SSH config if it exists
            if [[ -f "$SSH_CONFIG" ]] && grep -q "Host $HOST_ALIAS" "$SSH_CONFIG" 2>/dev/null; then
                load_preference
                if [[ "$CONNECTION_METHOD" == "ipv6" ]] || [[ -z "$CONNECTION_METHOD" ]]; then
                    sed -i.bak "s/HostName $IPV6_ADDRESS/HostName $new_ip/" "$SSH_CONFIG" 2>/dev/null || \
                    sed -i '' "s/HostName $IPV6_ADDRESS/HostName $new_ip/" "$SSH_CONFIG"
                    [[ -f "${SSH_CONFIG}.bak" ]] && rm "${SSH_CONFIG}.bak"
                    ok "Updated SSH config with new IPv6: $new_ip"
                else
                    ok "IPv6 updated to: $new_ip"
                    info "SSH config uses Static IP (IPv4 mode)"
                    info "Switch to IPv6 mode to use this IP"
                fi
            fi

            IPV6_ADDRESS="$new_ip"
            ok "Internal IP set to: $new_ip"
            warn "Note: To make this permanent, update IPV6_ADDRESS in the script"
            ;;
        *)
            err "Invalid choice"
            exit 1
            ;;
    esac
}

# Run full setup (automated mode)
run_setup() {
    echo -e "${GREEN}=== Valargen SSH Setup ===${NC}\n"

    # Pre-flight check - verify dependencies
    if ! preflight_check; then
        err "Pre-flight check failed. Install missing dependencies and try again."
        exit 1
    fi

    # Ensure .ssh directory exists first
    mkdir -p "$HOME/.ssh" && chmod 700 "$HOME/.ssh"

    # Step 1: Set default role (tunnel for API access)
    if [[ ! -f "$ROLE_FILE" ]]; then
        USER_ROLE="tunnel"
        SSH_USER="$ROLE_TUNNEL"
        echo "tunnel" > "$ROLE_FILE"
        ok "Auto-selected role: tunnel (API access only)"
    else
        load_role
        ok "Using saved role: $USER_ROLE (user: $SSH_USER)"
    fi

    # Step 2: Generate SSH Key if needed
    local key_is_new=false
    if [[ ! -f "$KEY_PATH" ]]; then
        info "No SSH key found. Generating new key..."
        key_is_new=true
        setup_key

        # After key generation, user needs to share with admin
        echo ""
        echo -e "${YELLOW}=== Waiting for Admin Key Setup ===${NC}"
        info "Your SSH key has been generated and displayed above."
        info "Share this key with your administrator."
        echo ""

        if [[ -t 0 ]]; then
            read -p "Has admin confirmed your key is added? (y/n): " key_confirmed
            if [[ ! "$key_confirmed" =~ ^[Yy]$ ]]; then
                echo ""
                warn "Setup paused - waiting for admin to add your key"
                info "After admin confirms, run this script again to continue"
                exit 0
            fi
        else
            info "Non-interactive mode: Share key with admin, then re-run"
            exit 0
        fi
    else
        ok "SSH key already exists"
        check_key_permissions

        # Only ask about key if SSH config is missing (first-time setup)
        if ! has_active_ssh_config && [[ -t 0 ]]; then
            echo ""
            echo -e "${YELLOW}An SSH key already exists:${NC}"
            echo "  $KEY_PATH"
            echo ""
            echo "1) Use existing key (recommended)"
            echo "2) Generate new key (will overwrite)"
            echo ""
            read -p "Select [1/2]: " key_choice

            if [[ "$key_choice" == "2" ]]; then
                warn "Generating new key will require admin to update server"
                read -p "Are you sure? (y/n): " confirm_new
                if [[ "$confirm_new" =~ ^[Yy]$ ]]; then
                    rm -f "$KEY_PATH" "${KEY_PATH}.pub"
                    setup_key
                fi
            else
                ok "Using existing key"
                display_key_attention
            fi
        fi
    fi

    # Step 3: Setup SSH Config first (needed for connection test)
    if has_active_ssh_config; then
        ok "SSH config already exists"
    else
        setup_config
    fi

    # Step 4: Auto-detect connection method
    echo ""
    if ! auto_detect_connection; then
        err "Could not establish connectivity to server"
        echo ""
        warn "Possible issues:"
        warn "  1. Admin has not added your SSH key yet"
        warn "  2. Your IP address is not whitelisted"
        warn "  3. Network connectivity issue"
        echo ""

        # Show user's public IP for whitelisting
        local public_ip=""
        if command -v curl &>/dev/null; then
            public_ip=$(curl -s --connect-timeout 5 ifconfig.me 2>/dev/null || curl -s --connect-timeout 5 api.ipify.org 2>/dev/null)
        fi

        if [[ -n "$public_ip" ]]; then
            echo -e "${YELLOW}Your public IP for whitelisting: ${BOLD}$public_ip${NC}"
        fi

        echo ""
        info "Share your public key and IP with admin, then try again"
        exit 1
    fi

    # Step 5: Update SSH config with detected connection method
    if [[ "$CONNECTION_METHOD" == "ipv6" ]]; then
        sed -i.bak "s/HostName .*/HostName $IPV6_ADDRESS/" "$SSH_CONFIG" 2>/dev/null || \
        sed -i '' "s/HostName .*/HostName $IPV6_ADDRESS/" "$SSH_CONFIG"
    else
        sed -i.bak "s/HostName .*/HostName $STATIC_IP/" "$SSH_CONFIG" 2>/dev/null || \
        sed -i '' "s/HostName .*/HostName $STATIC_IP/" "$SSH_CONFIG"
    fi
    [[ -f "${SSH_CONFIG}.bak" ]] && rm "${SSH_CONFIG}.bak"
    ok "Updated SSH config for $CONNECTION_METHOD connection"

    # Step 6: Test final connection
    echo ""
    local test_ip="$STATIC_IP"
    [[ "$CONNECTION_METHOD" == "ipv6" ]] && test_ip="$IPV6_ADDRESS"

    info "Testing SSH connection to $test_ip..."
    if test_connection "$test_ip"; then
        ok "Connection successful!"
    else
        err "Connection test failed"
        warn "The server may not have your key yet. Contact admin."
        exit 1
    fi

    echo ""
    ok "Setup complete!"
    echo ""

    if [[ -t 0 ]]; then
        read -p "Start tunnel now? (y/n): " start_now
        if [[ ! "$start_now" =~ ^[Yy]$ ]]; then
            info "Run '$(basename "$0") tunnel' to start tunnel later"
            exit 0
        fi
    else
        info "Starting tunnel automatically..."
    fi
    echo ""
}

# Interactive setup with prompts
run_setup_interactive() {
    echo -e "${GREEN}=== Valargen SSH Setup ===${NC}\n"

    # Step 1: Ask access level/role
    ask_role

    # Step 2: Ask connection method
    ask_connection_method

    if [[ "$CONNECTION_METHOD" == "direct" ]]; then
        # Direct SSH flow
        echo -e "${GREEN}=== Direct SSH Setup ===${NC}\n"

        # Step 2: SSH Key
        if [[ ! -f "$KEY_PATH" ]]; then
            setup_key
        else
            ok "SSH key already exists"
            display_key_attention
        fi

        # Step 3: Ask user to confirm admin has added the key
        echo -e "${YELLOW}=== Admin Key Setup ===${NC}"
        info "Share your public key with admin and ask them to:"
        info "  1. Add your SSH key to the server"
        info "  2. Whitelist your IP address if required"
        echo ""
        read -p "Has admin confirmed your key is added? (y/n): " key_confirmed

        if [[ ! "$key_confirmed" =~ ^[Yy]$ ]]; then
            warn "Please contact admin to add your key before proceeding"
            info "Run '$(basename "$0") showkey' to view your public key"
            exit 0
        fi

        # Step 4: SSH Config
        if [[ -f "$SSH_CONFIG" ]] && grep -q "Host $HOST_ALIAS" "$SSH_CONFIG" 2>/dev/null; then
            ok "SSH config already exists"
        else
            setup_config
        fi

        # Step 5: Test connection
        echo ""
        info "Testing SSH connection to $STATIC_IP..."
        if test_connection "$STATIC_IP"; then
            ok "Connection successful!"
        else
            err "Connection failed"
            echo ""
            warn "Possible issues:"
            warn "  1. Admin has not added your key yet"
            warn "  2. Your IP is not whitelisted"
            warn "  3. Server is not reachable"
            echo ""
            info "Contact admin with your public key and IP address"
            info "Run '$(basename "$0") showip' to see your IP"
            exit 1
        fi

    else
        # IPv6 flow
        echo -e "${GREEN}=== IPv6 Setup ===${NC}\n"

        # Step 2: SSH Key
        [[ ! -f "$KEY_PATH" ]] && setup_key

        # Step 3: SSH Config
        if [[ -f "$SSH_CONFIG" ]] && grep -q "Host $HOST_ALIAS" "$SSH_CONFIG" 2>/dev/null; then
            ok "SSH config already exists"
        else
            setup_config
        fi

        # Test IPv6 connection
        echo ""
        info "Testing IPv6 connection to $IPV6_ADDRESS..."
        if test_connection "$IPV6_ADDRESS"; then
            ok "IPv6 connection successful!"
        else
            warn "IPv6 connection failed. Your network may not support IPv6."
            info "Try switching to IPv4 mode: $(basename "$0") switch"
        fi
    fi

    echo ""
    ok "Setup complete!"
    echo ""
    read -p "Start tunnel now? (y/n): " start_now
    if [[ ! "$start_now" =~ ^[Yy]$ ]]; then
        info "Run '$(basename "$0") tunnel' to start tunnel later"
        exit 0
    fi
    echo ""
}

# Quick pre-flight check (silent unless issues found)
preflight_check() {
    local issues=0
    local warnings=""

    # Check required: ssh
    if ! command -v ssh &>/dev/null; then
        err "ssh NOT installed"
        info "Install: sudo apt install openssh-client (Ubuntu) or sudo yum install openssh-clients (CentOS)"
        issues=$((issues + 1))
    fi

    # Check required: ssh-keygen
    if ! command -v ssh-keygen &>/dev/null; then
        err "ssh-keygen NOT installed"
        issues=$((issues + 1))
    fi

    # Check DNS resolution
    if ! resolve_hostname "google.com" &>/dev/null; then
        warnings="${warnings}\n  - DNS resolution not working - check network settings"
    fi

    # Check clipboard (warn only)
    if ! command -v pbcopy &>/dev/null && ! command -v xclip &>/dev/null && ! command -v xsel &>/dev/null; then
        warnings="${warnings}\n  - No clipboard tool (xclip/xsel) - copy SSH key manually"
    fi

    # Show warnings if any
    if [[ -n "$warnings" ]]; then
        warn "Minor issues (non-blocking):$warnings"
        echo ""
    fi

    return $issues
}

# Full diagnose client machine - check dependencies and network
diagnose() {
    echo -e "${GREEN}=== Client Machine Diagnostics ===${NC}\n"
    local issues=0

    # Check required dependencies
    echo -e "${BLUE}[1/5] Checking dependencies...${NC}"

    if command -v ssh &>/dev/null; then
        ok "ssh installed: $(ssh -V 2>&1 | head -1)"
    else
        err "ssh NOT installed - required"
        issues=$((issues + 1))
    fi

    if command -v ssh-keygen &>/dev/null; then
        ok "ssh-keygen installed"
    else
        err "ssh-keygen NOT installed - required"
        issues=$((issues + 1))
    fi

    if command -v curl &>/dev/null; then
        ok "curl installed"
    else
        warn "curl not installed - optional (for IP detection)"
    fi

    if command -v ping &>/dev/null; then
        ok "ping installed"
    else
        warn "ping not installed - optional (for connectivity test)"
    fi

    # Check clipboard tools
    echo ""
    echo -e "${BLUE}[2/5] Checking clipboard tools...${NC}"
    if command -v pbcopy &>/dev/null; then
        ok "pbcopy available (macOS)"
    elif command -v xclip &>/dev/null; then
        ok "xclip available"
    elif command -v xsel &>/dev/null; then
        ok "xsel available"
    else
        warn "No clipboard tool - you'll need to copy SSH key manually"
    fi

    # Check network connectivity
    echo ""
    echo -e "${BLUE}[3/5] Checking network connectivity...${NC}"

    # Test internet
    if curl -s --connect-timeout 5 https://api.ipify.org &>/dev/null; then
        local public_ip=$(curl -s --connect-timeout 5 https://api.ipify.org)
        ok "Internet connectivity OK"
        info "Your public IP: $public_ip"
    else
        warn "Cannot reach internet - check network"
    fi

    # Test IPv6 support
    echo ""
    echo -e "${BLUE}[4/5] Checking IPv6/IPv4 support...${NC}"

    local ipv6_supported=false
    local ipv4_supported=false

    # Check IPv6
    if [[ -f /proc/net/if_inet6 ]] || [[ "$(uname -s)" == "Darwin" ]]; then
        if ping -6 -c 1 -W 3 2001:4860:4860::8888 &>/dev/null 2>&1 || ping6 -c 1 -W 3 2001:4860:4860::8888 &>/dev/null 2>&1; then
            ok "IPv6 supported on this network"
            ipv6_supported=true
        else
            warn "IPv6 not working (will use IPv4)"
        fi
    else
        warn "IPv6 not enabled on this system"
    fi

    # Check IPv4
    if ping -c 1 -W 3 8.8.8.8 &>/dev/null 2>&1; then
        ok "IPv4 supported"
        ipv4_supported=true
    else
        err "IPv4 not working"
        issues=$((issues + 1))
    fi

    # Test SSH port (outbound)
    echo ""
    echo -e "${BLUE}[5/5] Checking SSH port access...${NC}"

    if timeout 5 bash -c "echo >/dev/tcp/$STATIC_IP/22" 2>/dev/null; then
        ok "SSH port 22 reachable on $STATIC_IP"
    else
        if timeout 5 bash -c "echo >/dev/tcp/github.com/22" 2>/dev/null; then
            ok "SSH port 22 open (tested via github.com)"
            warn "Server $STATIC_IP not reachable - may need IP whitelist"
        else
            err "SSH port 22 blocked - check firewall/network"
            issues=$((issues + 1))
        fi
    fi

    # Summary
    echo ""
    echo -e "${GREEN}=== Diagnosis Summary ===${NC}"

    if [[ $issues -eq 0 ]]; then
        ok "All checks passed! Ready to run: $(basename "$0")"
        echo ""
        if $ipv6_supported; then
            info "Recommended: IPv6 connection"
        else
            info "Will use: IPv4 connection"
        fi
    else
        err "$issues issue(s) found"
        echo ""
        warn "Fix the issues above before running setup"

        if ! command -v ssh &>/dev/null; then
            echo ""
            info "Install SSH:"
            info "  Ubuntu/Debian: sudo apt install openssh-client"
            info "  CentOS/RHEL:   sudo yum install openssh-clients"
            info "  macOS:         Already installed"
        fi
    fi

    echo ""
    return $issues
}

# Check status
status() {
    echo -e "${GREEN}=== Connection Status ===${NC}\n"
    local all_ok=true

    # SSH Key
    if [[ -f "$KEY_PATH" ]]; then
        ok "SSH key exists: $KEY_PATH"
    else
        err "SSH key not found: $KEY_PATH"
        all_ok=false
    fi

    # SSH Config
    if has_active_ssh_config; then
        ok "SSH config exists for $HOST_ALIAS"
    else
        err "SSH config not found for $HOST_ALIAS"
        all_ok=false
    fi

    # Twingate
    if [[ "$(uname -s)" == "Linux" ]]; then
        if command -v twingate &>/dev/null; then
            ok "Twingate installed"
            if pgrep -x "twingate" &>/dev/null || systemctl is-active --quiet twingate 2>/dev/null; then
                ok "Twingate running"
            else
                warn "Twingate not running"
            fi
        else
            err "Twingate not installed"
            all_ok=false
        fi
    elif [[ "$(uname -s)" == "Darwin" ]]; then
        if pgrep -x "Twingate" &>/dev/null; then
            ok "Twingate running"
        else
            warn "Twingate not running (or not detected)"
        fi
    fi

    # Port check
    if lsof -i :$PROXY_PORT &>/dev/null || ss -tuln 2>/dev/null | grep -q ":$PROXY_PORT "; then
        warn "Port $PROXY_PORT is in use"
    else
        ok "Port $PROXY_PORT is available"
    fi

    # Test connections
    echo ""
    info "Testing SSH connections..."

    # Test IPv6 - check for "not available" which means auth succeeded (tunnel-only account)
    local ipv6_result=$(ssh -o ConnectTimeout=5 -o BatchMode=yes "$HOST_ALIAS" exit 2>&1)
    if [[ $? -eq 0 ]] || [[ "$ipv6_result" == *"not available"* ]]; then
        ok "IPv6 ($IPV6_ADDRESS) - reachable"
    else
        warn "IPv6 ($IPV6_ADDRESS) - not reachable"
    fi

    # Test IPv4 - check for "not available" which means auth succeeded (tunnel-only account)
    local ipv4_result=$(ssh -o ConnectTimeout=5 -o BatchMode=yes -o HostName=$STATIC_IP "$HOST_ALIAS" exit 2>&1)
    if [[ $? -eq 0 ]] || [[ "$ipv4_result" == *"not available"* ]]; then
        ok "Direct (static IP: $STATIC_IP) - reachable"
    else
        warn "Direct (static IP: $STATIC_IP) - not reachable"
    fi

    echo ""
    if $all_ok; then
        ok "Ready to start tunnel"
        echo ""
        info "Test with: curl --socks5-hostname 127.0.0.1:$PROXY_PORT https://api.ipify.org"
    else
        warn "Some checks failed - run 'setup' to fix"
    fi
}

# Test SSH connection
test_connection() {
    local ip=$1
    # Use -N flag for tunnel role (no shell required)
    # Timeout after 5 seconds with exit on success
    timeout 5 ssh -o ConnectTimeout=$SSH_TIMEOUT -o BatchMode=yes -o HostName=$ip -N "$HOST_ALIAS" &
    local pid=$!
    sleep 2
    if kill -0 $pid 2>/dev/null; then
        kill $pid 2>/dev/null
        wait $pid 2>/dev/null
        return 0
    else
        wait $pid 2>/dev/null
        return 1
    fi
}

# Start tunnel with specified IP
start_tunnel_with_ip() {
    local ip=$1
    local method=$2

    info "Starting tunnel via $method ($ip)..."
    info "Postman: Settings > Proxy > SOCKS5 > 127.0.0.1:$PROXY_PORT"

    if [[ "$BIND_ADDRESS" == "0.0.0.0" ]]; then
        info "Docker: Proxy accessible at 172.17.0.1:$PROXY_PORT"
        warn "Binding to all interfaces - ensure firewall is configured!"
    else
        info "Binding to localhost only (change BIND_ADDRESS for Docker access)"
    fi

    info "Press Ctrl+C to stop"
    echo ""
    ssh -o ConnectTimeout=$SSH_TIMEOUT -o HostName=$ip -D $BIND_ADDRESS:$PROXY_PORT -N -C "$HOST_ALIAS"
}

# Start tunnel using saved preference or auto-detect
tunnel() {
    check_port
    load_preference
    load_role

    # Ensure .ssh directory exists
    mkdir -p "$HOME/.ssh" && chmod 700 "$HOME/.ssh"

    # Check SSH key exists and has correct permissions
    if [[ ! -f "$KEY_PATH" ]]; then
        err "SSH key not found: $KEY_PATH"
        info "Run '$(basename "$0")' to generate a new key"
        exit 1
    fi
    check_key_permissions

    # Ensure role is set
    if [[ -z "$SSH_USER" ]]; then
        USER_ROLE="tunnel"
        SSH_USER="$ROLE_TUNNEL"
        echo "tunnel" > "$ROLE_FILE"
        ok "Auto-selected role: tunnel"
    fi

    local selected_ip=""
    local selected_method=""
    local other_ip=""
    local other_method=""

    # Use saved preference or auto-detect
    if [[ "$CONNECTION_METHOD" == "ipv6" ]]; then
        selected_ip=$IPV6_ADDRESS
        selected_method="IPv6"
        other_ip=$STATIC_IP
        other_method="IPv4"
    elif [[ "$CONNECTION_METHOD" == "direct" ]]; then
        selected_ip=$STATIC_IP
        selected_method="IPv4"
        other_ip=$IPV6_ADDRESS
        other_method="IPv6"
    else
        # No preference saved, auto-detect
        info "No saved preference. Auto-detecting best connection..."

        if auto_detect_connection; then
            if [[ "$CONNECTION_METHOD" == "ipv6" ]]; then
                selected_ip=$IPV6_ADDRESS
                selected_method="IPv6"
                other_ip=$STATIC_IP
                other_method="IPv4"
            else
                selected_ip=$STATIC_IP
                selected_method="IPv4"
                other_ip=$IPV6_ADDRESS
                other_method="IPv6"
            fi
        else
            # Auto-detect failed, show error with helpful info
            err "Could not auto-detect connection method"
            show_connection_help
            exit 1
        fi
    fi

    info "Using $selected_method connection ($selected_ip)"

    # Test connection first
    info "Testing connection..."
    if test_connection "$selected_ip"; then
        ok "Connection OK"
        start_tunnel_with_ip "$selected_ip" "$selected_method"
    else
        err "Connection failed to $selected_method ($selected_ip)"

        if [[ "$selected_method" == "IPv6" ]]; then
            warn "Make sure your network supports IPv6"
        fi

        # Auto-try other method
        info "Automatically trying $other_method ($other_ip)..."
        if test_connection "$other_ip"; then
            ok "Connection OK via $other_method"
            # Save this as new preference
            if [[ "$other_method" == "IPv6" ]]; then
                echo "ipv6" > "$PREF_FILE"
            else
                echo "direct" > "$PREF_FILE"
            fi
            ok "Saved $other_method as preferred connection"
            start_tunnel_with_ip "$other_ip" "$other_method"
        else
            err "Connection failed to both IPv4 and IPv6"
            show_connection_help
            exit 1
        fi
    fi
}

# Show connection help when all methods fail
show_connection_help() {
    echo ""
    err "Possible issues:"
    err "  1. Have you shared your public key with admin?"
    err "  2. Has admin added your key to the server?"
    err "  3. Is your SSH key correct?"
    err "  4. Is your IP address whitelisted on the server?"
    echo ""

    # Try to detect public IP
    local public_ip=""
    if command -v curl &>/dev/null; then
        public_ip=$(curl -s --connect-timeout 5 ifconfig.me 2>/dev/null || curl -s --connect-timeout 5 api.ipify.org 2>/dev/null)
    fi

    echo -e "${YELLOW}=== Information for Admin ===${NC}"
    echo ""

    if [[ -n "$public_ip" ]]; then
        echo -e "${BOLD}Your Public IP: $public_ip${NC}"
    else
        warn "Could not auto-detect your public IP"
    fi

    if [[ -f "${KEY_PATH}.pub" ]]; then
        echo ""
        display_key_attention
    fi

    echo ""
    info "Share this information with your administrator"
    info "Run '$(basename "$0") setup' to regenerate keys if needed"
}

# Start database tunnel for DBeaver/pgAdmin
db_tunnel() {
    info "Starting PostgreSQL tunnel on port $DB_LOCAL_PORT..."

    # Check if port is already in use
    if lsof -i :$DB_LOCAL_PORT &>/dev/null || ss -tuln 2>/dev/null | grep -q ":$DB_LOCAL_PORT "; then
        warn "Port $DB_LOCAL_PORT is already in use"
        info "Run '$(basename "$0") db-kill' to stop existing tunnel"
        return 1
    fi

    # Check SSH key
    if [[ ! -f "$KEY_PATH" ]]; then
        err "SSH key not found: $KEY_PATH"
        info "Run '$(basename "$0")' to setup first"
        return 1
    fi

    check_key_permissions

    # Start the tunnel
    ssh -o ConnectTimeout=$SSH_TIMEOUT -L 0.0.0.0:$DB_LOCAL_PORT:$DB_REMOTE_HOST:$DB_REMOTE_PORT -N -f "$HOST_ALIAS"

    if [[ $? -eq 0 ]]; then
        ok "Database tunnel started!"
        echo ""
        info "DBeaver/pgAdmin connection settings:"
        echo "  Host:     127.0.0.1"
        echo "  Port:     $DB_LOCAL_PORT"
        echo "  Database: valargen"
        echo "  Username: valargen"
        echo ""
        info "Stop with: $(basename "$0") db-kill"
    else
        err "Failed to start database tunnel"
        return 1
    fi
}

# Kill database tunnel
kill_db_tunnel() {
    info "Stopping database tunnel on port $DB_LOCAL_PORT..."

    local pid=""
    if command -v lsof &>/dev/null; then
        pid=$(lsof -ti :$DB_LOCAL_PORT 2>/dev/null)
    elif command -v ss &>/dev/null; then
        pid=$(ss -tlnp 2>/dev/null | grep ":$DB_LOCAL_PORT " | grep -oP 'pid=\K\d+')
    fi

    if [[ -n "$pid" ]]; then
        kill $pid 2>/dev/null && ok "Database tunnel stopped (PID: $pid)" || err "Failed to stop tunnel"
    else
        warn "No database tunnel running on port $DB_LOCAL_PORT"
    fi
}

# Main
case "${1:-}" in
    -h|--help|help)
        show_help
        ;;
    status)
        status
        ;;
    kill)
        kill_tunnel
        ;;
    restart)
        kill_tunnel
        sleep 1
        tunnel
        ;;
    tunnel)
        tunnel
        ;;
    setup)
        # Interactive setup with prompts
        run_setup_interactive
        tunnel
        ;;
    auto|autosetup)
        # Fully automated setup
        run_setup
        tunnel
        ;;
    reset)
        reset_account
        ;;
    showkey)
        show_key
        ;;
    showip)
        show_ip
        ;;
    updateip)
        update_ip
        ;;
    switch)
        switch_method
        ;;
    diagnose|diag|check)
        diagnose
        ;;
    db)
        db_tunnel
        ;;
    db-kill)
        kill_db_tunnel
        ;;
    *)
        # Default: automatic mode
        if check_requirements; then
            ok "All requirements met"
            tunnel
        else
            echo ""
            info "First-time setup detected. Running automated setup..."
            echo ""
            run_setup
            tunnel
        fi
        ;;
esac
