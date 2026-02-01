#
# Valargen SSH Setup & Tunnel (Windows PowerShell)
#

param(
    [Parameter(Position=0)]
    [string]$Command = ""
)

$ErrorActionPreference = "Continue"

# Configuration
$KEY_PATH = "$env:USERPROFILE\.ssh\id_ed25519_valargen"
$SSH_CONFIG = "$env:USERPROFILE\.ssh\config"
$PREF_FILE = "$env:USERPROFILE\.ssh\.valargen_pref"
$ROLE_FILE = "$env:USERPROFILE\.ssh\.valargen_role"
$HOST_ALIAS = "valargen-staging-tunnel"
$IPV6_ADDRESS = "2603:1030:20e:1::5"
$STATIC_IP = "4.227.184.143"
$SSH_TIMEOUT = 15
$PROXY_PORT = 1080
$DB_LOCAL_PORT = 5433
$DB_REMOTE_HOST = "10.0.0.4"
$DB_REMOTE_PORT = 5432
$BIND_ADDRESS = "0.0.0.0"

# Role-based usernames
$ROLE_TUNNEL = "vg-tunnel"
$ROLE_ADMIN = "vg-admin"
$ROLE_SUPER = "vg-super"

# Script state
$script:CONNECTION_METHOD = ""
$script:USER_ROLE = ""
$script:SSH_USER = ""

# Output functions
function Write-Info { param([string]$Message) Write-Host "[INFO] $Message" -ForegroundColor Blue }
function Write-Ok { param([string]$Message) Write-Host "[OK] $Message" -ForegroundColor Green }
function Write-Warn { param([string]$Message) Write-Host "[WARN] $Message" -ForegroundColor Yellow }
function Write-Err { param([string]$Message) Write-Host "[ERROR] $Message" -ForegroundColor Red }
function Write-Attention {
    param([string]$Message)
    Write-Host ""
    Write-Host " $Message " -ForegroundColor Yellow -BackgroundColor DarkRed
    Write-Host ""
}

# Check if OpenSSH is available
function Test-OpenSSH {
    $sshPath = Get-Command ssh -ErrorAction SilentlyContinue
    if (-not $sshPath) {
        Write-Err "OpenSSH is not installed or not in PATH"
        Write-Host ""
        Write-Host "To install OpenSSH on Windows:" -ForegroundColor Yellow
        Write-Host "  1. Settings > Apps > Optional Features > Add a feature"
        Write-Host "  2. Search for 'OpenSSH Client' and install"
        Write-Host "  Or run: Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0"
        return $false
    }
    return $true
}

# Fix SSH key permissions for Windows (using icacls - most reliable method)
function Set-SSHKeyPermissions {
    param([string]$KeyPath)

    if (-not (Test-Path $KeyPath)) { return $false }

    # Use icacls directly - more reliable than ACL methods which require SeSecurityPrivilege
    try {
        $null = & icacls $KeyPath /inheritance:r /grant:r "${env:USERNAME}:(R)" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Ok "SSH key permissions set via icacls"
            return $true
        }
    } catch {}

    # Fallback: try ACL method
    try {
        $acl = Get-Acl $KeyPath
        $acl.SetAccessRuleProtection($true, $false)
        $acl.Access | ForEach-Object { $acl.RemoveAccessRule($_) } | Out-Null
        $identity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
        $rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
            $identity, "FullControl", "Allow"
        )
        $acl.AddAccessRule($rule)
        Set-Acl -Path $KeyPath -AclObject $acl -ErrorAction Stop
        Write-Ok "SSH key permissions set correctly"
        return $true
    } catch {
        Write-Warn "Could not set key permissions: $_"
        Write-Info "Manually run: icacls `"$KeyPath`" /inheritance:r /grant:r `"$env:USERNAME:(R)`""
        return $false
    }
}

# Check if port is in use
function Test-PortInUse {
    param([int]$Port)

    $connection = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    return $null -ne $connection
}

# Get process using port
function Get-PortProcess {
    param([int]$Port)

    $connection = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($connection) {
        return $connection.OwningProcess
    }
    return $null
}

# Test IPv6 connectivity
function Test-IPv6Support {
    Write-Info "Testing IPv6 connectivity to $IPV6_ADDRESS..."

    # Try ping (no -TimeoutSeconds for Windows PowerShell 5.x compatibility)
    $pingResult = Test-Connection -ComputerName $IPV6_ADDRESS -Count 1 -Quiet -ErrorAction SilentlyContinue
    if ($pingResult) {
        return $true
    }

    # Try SSH connection test
    $process = Start-Process -FilePath "ssh" -ArgumentList "-o", "ConnectTimeout=3", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=accept-new", "-o", "HostName=$IPV6_ADDRESS", "-N", $HOST_ALIAS -PassThru -WindowStyle Hidden
    Start-Sleep -Seconds 2

    if (-not $process.HasExited) {
        Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        return $true
    }

    return $false
}

# Test IPv4 connectivity
function Test-IPv4Support {
    Write-Info "Testing IPv4 connectivity to $STATIC_IP..."

    # Try ping (no -TimeoutSeconds for Windows PowerShell 5.x compatibility)
    $pingResult = Test-Connection -ComputerName $STATIC_IP -Count 1 -Quiet -ErrorAction SilentlyContinue
    if ($pingResult) {
        return $true
    }

    # Try SSH connection test
    $process = Start-Process -FilePath "ssh" -ArgumentList "-o", "ConnectTimeout=3", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=accept-new", "-o", "HostName=$STATIC_IP", "-N", $HOST_ALIAS -PassThru -WindowStyle Hidden
    Start-Sleep -Seconds 2

    if (-not $process.HasExited) {
        Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        return $true
    }

    return $false
}

# Auto-detect best connection method
function Get-BestConnectionMethod {
    Write-Info "Auto-detecting network connectivity..."

    $ipv6Ok = $false
    $ipv4Ok = $false

    # Test IPv6 first (preferred)
    if (Test-IPv6Support) {
        Write-Ok "IPv6 connectivity available"
        $ipv6Ok = $true
    } else {
        Write-Warn "IPv6 not available"
    }

    # Test IPv4
    if (Test-IPv4Support) {
        Write-Ok "IPv4 connectivity available"
        $ipv4Ok = $true
    } else {
        Write-Warn "IPv4 not available"
    }

    # Determine best method
    if ($ipv6Ok) {
        $script:CONNECTION_METHOD = "ipv6"
        Set-Content -Path $PREF_FILE -Value "ipv6" -Force
        Write-Ok "Auto-selected: IPv6 (Direct)"
        return $true
    } elseif ($ipv4Ok) {
        $script:CONNECTION_METHOD = "direct"
        Set-Content -Path $PREF_FILE -Value "direct" -Force
        Write-Ok "Auto-selected: IPv4 (Direct)"
        return $true
    } else {
        Write-Err "No connectivity available to server"
        return $false
    }
}

# Check if SSH config has entry for host
function Test-SSHConfigExists {
    if (Test-Path $SSH_CONFIG) {
        $content = Get-Content $SSH_CONFIG -Raw -ErrorAction SilentlyContinue
        return $content -match "Host $HOST_ALIAS"
    }
    return $false
}

# Safely update HostName in SSH config (line-by-line to avoid regex corruption)
function Update-SSHConfigHostName {
    param([string]$NewHostName)

    if (-not (Test-Path $SSH_CONFIG)) { return $false }

    $lines = Get-Content $SSH_CONFIG
    $newLines = @()
    $inTargetBlock = $false

    foreach ($line in $lines) {
        # Check if entering target host block
        if ($line -match "^Host\s+$HOST_ALIAS\s*$") {
            $inTargetBlock = $true
            $newLines += $line
            continue
        }

        # Check if leaving host block (new Host line or end of file)
        if ($inTargetBlock -and $line -match "^Host\s+") {
            $inTargetBlock = $false
        }

        # Replace HostName line within target block
        if ($inTargetBlock -and $line -match "^\s+HostName\s+") {
            $newLines += "    HostName $NewHostName"
        } else {
            $newLines += $line
        }
    }

    $newLines | Set-Content $SSH_CONFIG -Force
    return $true
}

# Load saved preference
function Read-Preference {
    if (Test-Path $PREF_FILE) {
        $script:CONNECTION_METHOD = (Get-Content $PREF_FILE -Raw).Trim()
    }
}

# Load saved role
function Read-Role {
    if (Test-Path $ROLE_FILE) {
        $script:USER_ROLE = (Get-Content $ROLE_FILE -Raw).Trim()
        switch ($script:USER_ROLE) {
            "tunnel" { $script:SSH_USER = $ROLE_TUNNEL }
            "admin" { $script:SSH_USER = $ROLE_ADMIN }
            "super" { $script:SSH_USER = $ROLE_SUPER }
            default { $script:SSH_USER = $ROLE_TUNNEL }
        }
    }
}

# Display key with attention formatting
function Show-KeyAttention {
    if (-not (Test-Path "$KEY_PATH.pub")) {
        Write-Err "Public key not found: $KEY_PATH.pub"
        return
    }

    $keyContent = Get-Content "$KEY_PATH.pub" -Raw

    Write-Host ""
    Write-Host "==================================================================" -ForegroundColor Red
    Write-Host "                                                                  " -ForegroundColor Red
    Write-Host "   ATTENTION: COPY THIS KEY AND SEND TO ADMINISTRATOR            " -ForegroundColor Red
    Write-Host "                                                                  " -ForegroundColor Red
    Write-Host "==================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Your SSH Public Key:" -ForegroundColor Green
    Write-Host "==================================================================" -ForegroundColor Yellow
    Write-Host $keyContent -ForegroundColor White
    Write-Host "==================================================================" -ForegroundColor Yellow
    Write-Host ""

    # Try to copy to clipboard
    try {
        $keyContent | Set-Clipboard
        Write-Host "KEY AUTOMATICALLY COPIED TO CLIPBOARD" -ForegroundColor Green
    } catch {
        Write-Attention "MANUALLY COPY THE KEY ABOVE"
    }

    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "  1. Send this key to your administrator"
    Write-Host "  2. Wait for confirmation that your key has been added"
    Write-Host "  3. Run this script again to connect"
    Write-Host ""
    Write-Host "NEVER share your private key (without .pub)!" -ForegroundColor Red
    Write-Host ""
}

# Generate SSH key
function New-SSHKey {
    # Ensure .ssh directory exists
    $sshDir = "$env:USERPROFILE\.ssh"
    if (-not (Test-Path $sshDir)) {
        New-Item -ItemType Directory -Path $sshDir -Force | Out-Null
    }

    # Generate email from username and hostname
    $autoEmail = "$env:USERNAME@$env:COMPUTERNAME"

    Write-Host ""
    $userEmail = Read-Host "Enter your email (for key comment) [$autoEmail]"
    if ([string]::IsNullOrWhiteSpace($userEmail)) {
        $userEmail = $autoEmail
    }

    Write-Host ""
    Write-Info "Generating SSH key..."

    # Generate key (empty passphrase)
    # Use '""' to pass empty string correctly on Windows
    $result = & ssh-keygen -t ed25519 -C $userEmail -f $KEY_PATH -N '""' 2>&1

    if ($LASTEXITCODE -eq 0 -and (Test-Path $KEY_PATH) -and (Test-Path "$KEY_PATH.pub")) {
        Set-SSHKeyPermissions -KeyPath $KEY_PATH
        Write-Ok "SSH key generated!"
        Show-KeyAttention
    } else {
        Write-Err "Failed to generate SSH key: $result"
        # Cleanup any partial files
        if (Test-Path $KEY_PATH) { Remove-Item $KEY_PATH -Force -ErrorAction SilentlyContinue }
        if (Test-Path "$KEY_PATH.pub") { Remove-Item "$KEY_PATH.pub" -Force -ErrorAction SilentlyContinue }
        return $false
    }

    $confirm = Read-Host "Press Enter after admin confirms your key is added..."
    return $true
}

# Configure SSH
function Set-SSHConfig {
    Write-Info "Configuring SSH..."

    $sshDir = "$env:USERPROFILE\.ssh"
    if (-not (Test-Path $sshDir)) {
        New-Item -ItemType Directory -Path $sshDir -Force | Out-Null
    }

    # Remove existing entry if present
    if (Test-Path $SSH_CONFIG) {
        $lines = Get-Content $SSH_CONFIG
        $newLines = @()
        $skipBlock = $false

        foreach ($line in $lines) {
            if ($line -match "^Host $HOST_ALIAS") {
                $skipBlock = $true
                continue
            }
            if ($skipBlock -and $line -match "^\s*(Host\s|$)") {
                $skipBlock = $false
            }
            if (-not $skipBlock) {
                $newLines += $line
            }
        }

        $newLines | Set-Content $SSH_CONFIG -Force
    }

    # Add new config entry
    $configEntry = @"

Host $HOST_ALIAS
    HostName $STATIC_IP
    User $script:SSH_USER
    IdentityFile $KEY_PATH
    ConnectTimeout $SSH_TIMEOUT
    ServerAliveInterval 60
    ServerAliveCountMax 3
"@

    Add-Content -Path $SSH_CONFIG -Value $configEntry
    Write-Ok "SSH config added"

    # Add host keys
    Write-Info "Adding server host keys..."
    & ssh-keyscan -H $STATIC_IP 2>$null | Add-Content "$env:USERPROFILE\.ssh\known_hosts"
    & ssh-keyscan -H $IPV6_ADDRESS 2>$null | Add-Content "$env:USERPROFILE\.ssh\known_hosts"
    Write-Ok "Host keys added"
}

# Test SSH connection
function Test-SSHConnection {
    param([string]$IP)

    $process = Start-Process -FilePath "ssh" -ArgumentList "-o", "ConnectTimeout=$SSH_TIMEOUT", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=accept-new", "-o", "HostName=$IP", "-N", $HOST_ALIAS -PassThru -WindowStyle Hidden
    Start-Sleep -Seconds 2

    if (-not $process.HasExited) {
        Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        return $true
    }

    return $false
}

# Kill tunnel
function Stop-Tunnel {
    Write-Info "Stopping tunnel on port $PROXY_PORT..."

    $processId = Get-PortProcess -Port $PROXY_PORT
    if ($processId) {
        try {
            Stop-Process -Id $processId -Force
            Write-Ok "Tunnel stopped (PID: $processId)"
        } catch {
            Write-Err "Failed to stop tunnel: $_"
        }
    } else {
        Write-Warn "No tunnel running on port $PROXY_PORT"
    }
}

# Start tunnel with IP
function Start-TunnelWithIP {
    param(
        [string]$IP,
        [string]$Method
    )

    Write-Info "Starting tunnel via $Method ($IP)..."
    Write-Info "Postman: Settings > Proxy > SOCKS5 > 127.0.0.1:$PROXY_PORT"

    if ($BIND_ADDRESS -eq "0.0.0.0") {
        Write-Info "Docker: Proxy accessible at host.docker.internal:$PROXY_PORT"
        Write-Warn "Binding to all interfaces - ensure firewall is configured!"
    } else {
        Write-Info "Binding to localhost only"
    }

    Write-Info "Press Ctrl+C to stop"
    Write-Host ""

    & ssh -o "ConnectTimeout=$SSH_TIMEOUT" -o "StrictHostKeyChecking=accept-new" -o "HostName=$IP" -D "${BIND_ADDRESS}:$PROXY_PORT" -N -C $HOST_ALIAS
}

# Main tunnel function
function Start-Tunnel {
    if (Test-PortInUse -Port $PROXY_PORT) {
        Write-Err "Port $PROXY_PORT is already in use"
        Write-Info "Run: .\tunnel.ps1 kill"
        return
    }

    Read-Preference
    Read-Role

    # Ensure .ssh directory exists
    $sshDir = "$env:USERPROFILE\.ssh"
    if (-not (Test-Path $sshDir)) {
        New-Item -ItemType Directory -Path $sshDir -Force | Out-Null
    }

    # Check SSH key exists
    if (-not (Test-Path $KEY_PATH)) {
        Write-Err "SSH key not found: $KEY_PATH"
        Write-Info "Run: .\tunnel.ps1 setup"
        return
    }

    Set-SSHKeyPermissions -KeyPath $KEY_PATH

    # Ensure role is set
    if ([string]::IsNullOrWhiteSpace($script:SSH_USER)) {
        $script:USER_ROLE = "tunnel"
        $script:SSH_USER = $ROLE_TUNNEL
        Set-Content -Path $ROLE_FILE -Value "tunnel" -Force
        Write-Ok "Auto-selected role: tunnel"
    }

    $selectedIP = ""
    $selectedMethod = ""
    $otherIP = ""
    $otherMethod = ""

    # Use saved preference or auto-detect
    if ($script:CONNECTION_METHOD -eq "ipv6") {
        $selectedIP = $IPV6_ADDRESS
        $selectedMethod = "IPv6"
        $otherIP = $STATIC_IP
        $otherMethod = "IPv4"
    } elseif ($script:CONNECTION_METHOD -eq "direct") {
        $selectedIP = $STATIC_IP
        $selectedMethod = "IPv4"
        $otherIP = $IPV6_ADDRESS
        $otherMethod = "IPv6"
    } else {
        Write-Info "No saved preference. Auto-detecting best connection..."

        if (Get-BestConnectionMethod) {
            if ($script:CONNECTION_METHOD -eq "ipv6") {
                $selectedIP = $IPV6_ADDRESS
                $selectedMethod = "IPv6"
                $otherIP = $STATIC_IP
                $otherMethod = "IPv4"
            } else {
                $selectedIP = $STATIC_IP
                $selectedMethod = "IPv4"
                $otherIP = $IPV6_ADDRESS
                $otherMethod = "IPv6"
            }
        } else {
            Write-Err "Could not auto-detect connection method"
            Show-ConnectionHelp
            return
        }
    }

    Write-Info "Using $selectedMethod connection ($selectedIP)"
    Write-Info "Testing connection..."

    if (Test-SSHConnection -IP $selectedIP) {
        Write-Ok "Connection OK"
        Start-TunnelWithIP -IP $selectedIP -Method $selectedMethod
    } else {
        Write-Err "Connection failed to $selectedMethod ($selectedIP)"

        Write-Info "Automatically trying $otherMethod ($otherIP)..."
        if (Test-SSHConnection -IP $otherIP) {
            Write-Ok "Connection OK via $otherMethod"

            if ($otherMethod -eq "IPv6") {
                Set-Content -Path $PREF_FILE -Value "ipv6" -Force
            } else {
                Set-Content -Path $PREF_FILE -Value "direct" -Force
            }
            Write-Ok "Saved $otherMethod as preferred connection"
            Start-TunnelWithIP -IP $otherIP -Method $otherMethod
        } else {
            Write-Err "Connection failed to both IPv4 and IPv6"
            Show-ConnectionHelp
        }
    }
}

# Show connection help
function Show-ConnectionHelp {
    Write-Host ""
    Write-Err "Possible issues:"
    Write-Err "  1. Have you shared your public key with admin?"
    Write-Err "  2. Has admin added your key to the server?"
    Write-Err "  3. Is your SSH key correct?"
    Write-Err "  4. Is your IP address whitelisted on the server?"
    Write-Host ""

    # Try to detect public IP
    try {
        $publicIP = (Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing -TimeoutSec 5).Content
        Write-Host "Your Public IP: $publicIP" -ForegroundColor Yellow
    } catch {
        Write-Warn "Could not auto-detect your public IP"
    }

    if (Test-Path "$KEY_PATH.pub") {
        Show-KeyAttention
    }

    Write-Host ""
    Write-Info "Share this information with your administrator"
}

# Run setup
function Start-Setup {
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "  Valargen SSH Setup (Windows)" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""

    # Check OpenSSH
    if (-not (Test-OpenSSH)) {
        return
    }

    # Ensure .ssh directory exists
    $sshDir = "$env:USERPROFILE\.ssh"
    if (-not (Test-Path $sshDir)) {
        New-Item -ItemType Directory -Path $sshDir -Force | Out-Null
    }

    # Set default role
    if (-not (Test-Path $ROLE_FILE)) {
        $script:USER_ROLE = "tunnel"
        $script:SSH_USER = $ROLE_TUNNEL
        Set-Content -Path $ROLE_FILE -Value "tunnel" -Force
        Write-Ok "Auto-selected role: tunnel (API access only)"
    } else {
        Read-Role
        Write-Ok "Using saved role: $script:USER_ROLE (user: $script:SSH_USER)"
    }

    # Generate SSH key if needed
    if (-not (Test-Path $KEY_PATH)) {
        Write-Info "No SSH key found. Generating new key..."
        if (-not (New-SSHKey)) {
            return
        }

        Write-Host ""
        Write-Host "=== Waiting for Admin Key Setup ===" -ForegroundColor Yellow
        Write-Info "Your SSH key has been generated and displayed above."
        Write-Info "Share this key with your administrator."
        Write-Host ""

        $confirm = Read-Host "Has admin confirmed your key is added? (y/n)"
        if ($confirm -notmatch "^[Yy]") {
            Write-Warn "Setup paused - waiting for admin to add your key"
            Write-Info "After admin confirms, run this script again"
            return
        }
    } else {
        Write-Ok "SSH key already exists"
        Set-SSHKeyPermissions -KeyPath $KEY_PATH
    }

    # Setup SSH config
    if (Test-SSHConfigExists) {
        Write-Ok "SSH config already exists"
    } else {
        Set-SSHConfig
    }

    # Auto-detect connection method
    Write-Host ""
    if (-not (Get-BestConnectionMethod)) {
        Write-Err "Could not establish connectivity to server"
        Write-Host ""
        Write-Warn "Possible issues:"
        Write-Warn "  1. Admin has not added your SSH key yet"
        Write-Warn "  2. Your IP address is not whitelisted"
        Write-Warn "  3. Network connectivity issue"
        Write-Host ""

        try {
            $publicIP = (Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing -TimeoutSec 5).Content
            Write-Host "Your public IP for whitelisting: $publicIP" -ForegroundColor Yellow
        } catch {}

        Write-Info "Share your public key and IP with admin, then try again"
        return
    }

    # Update SSH config with detected method
    if (Test-Path $SSH_CONFIG) {
        $newHostName = if ($script:CONNECTION_METHOD -eq "ipv6") { $IPV6_ADDRESS } else { $STATIC_IP }
        if (Update-SSHConfigHostName -NewHostName $newHostName) {
            Write-Ok "Updated SSH config for $script:CONNECTION_METHOD connection"
        }
    }

    # Test connection
    Write-Host ""
    $testIP = if ($script:CONNECTION_METHOD -eq "ipv6") { $IPV6_ADDRESS } else { $STATIC_IP }
    Write-Info "Testing SSH connection to $testIP..."

    if (Test-SSHConnection -IP $testIP) {
        Write-Ok "Connection successful!"
    } else {
        Write-Err "Connection test failed"
        Write-Warn "The server may not have your key yet. Contact admin."
        return
    }

    Write-Host ""
    Write-Ok "Setup complete!"
    Write-Host ""

    $startNow = Read-Host "Start tunnel now? (y/n)"
    if ($startNow -match "^[Yy]") {
        Start-Tunnel
    } else {
        Write-Info "Run: .\tunnel.ps1 tunnel"
    }
}

# Show status
function Show-Status {
    Write-Host "=== Connection Status ===" -ForegroundColor Green
    Write-Host ""

    $allOk = $true

    # SSH Key
    if (Test-Path $KEY_PATH) {
        Write-Ok "SSH key exists: $KEY_PATH"
    } else {
        Write-Err "SSH key not found: $KEY_PATH"
        $allOk = $false
    }

    # SSH Config
    if (Test-SSHConfigExists) {
        Write-Ok "SSH config exists for $HOST_ALIAS"
    } else {
        Write-Err "SSH config not found for $HOST_ALIAS"
        $allOk = $false
    }

    # Port check
    if (Test-PortInUse -Port $PROXY_PORT) {
        Write-Warn "Port $PROXY_PORT is in use"
    } else {
        Write-Ok "Port $PROXY_PORT is available"
    }

    # Test connections
    Write-Host ""
    Write-Info "Testing SSH connections..."

    if (Test-SSHConnection -IP $IPV6_ADDRESS) {
        Write-Ok "IPv6 ($IPV6_ADDRESS) - reachable"
    } else {
        Write-Warn "IPv6 ($IPV6_ADDRESS) - not reachable"
    }

    if (Test-SSHConnection -IP $STATIC_IP) {
        Write-Ok "Direct (static IP: $STATIC_IP) - reachable"
    } else {
        Write-Warn "Direct (static IP: $STATIC_IP) - not reachable"
    }

    Write-Host ""
    if ($allOk) {
        Write-Ok "Ready to start tunnel"
        Write-Host ""
        Write-Info "Test with: curl --socks5-hostname 127.0.0.1:$PROXY_PORT https://api.ipify.org"
    } else {
        Write-Warn "Some checks failed - run 'setup' to fix"
    }
}

# Show key
function Show-Key {
    if (-not (Test-Path "$KEY_PATH.pub")) {
        Write-Err "Public key not found: $KEY_PATH.pub"
        Write-Info "Run: .\tunnel.ps1 setup"
        return
    }
    Show-KeyAttention
}

# Show IP
function Show-IP {
    Write-Host "=== Configured Server IPs ===" -ForegroundColor Green
    Write-Host ""

    Read-Preference
    Read-Role

    Write-Host "Static IP (Direct SSH):     $STATIC_IP"
    Write-Host "IPv6 Address:               $IPV6_ADDRESS"
    Write-Host ""

    switch ($script:CONNECTION_METHOD) {
        "direct" { Write-Ok "Current mode: IPv4 Direct (using $STATIC_IP)" }
        "ipv6" { Write-Ok "Current mode: IPv6 (using $IPV6_ADDRESS)" }
        default { Write-Info "Current mode: Not set" }
    }

    if (-not [string]::IsNullOrWhiteSpace($script:USER_ROLE)) {
        Write-Ok "Current role: $script:USER_ROLE (user: $script:SSH_USER)"
    } else {
        Write-Info "Current role: Not set"
    }
}

# Switch connection method
function Switch-Method {
    Read-Preference

    Write-Host "=== Switch Connection Method ===" -ForegroundColor Green
    Write-Host ""

    if (-not [string]::IsNullOrWhiteSpace($script:CONNECTION_METHOD)) {
        Write-Info "Current method: $script:CONNECTION_METHOD"
    } else {
        Write-Info "Current method: not set"
    }
    Write-Host ""

    Write-Host "1) IPv6 - Direct IPv6 connection: $IPV6_ADDRESS"
    Write-Host "2) IPv4 - Static IP: $STATIC_IP"
    Write-Host ""

    $choice = Read-Host "Select [1/2]"

    switch ($choice) {
        "1" {
            Set-Content -Path $PREF_FILE -Value "ipv6" -Force
            if (Update-SSHConfigHostName -NewHostName $IPV6_ADDRESS) {
                Write-Ok "Updated SSH config to use: $IPV6_ADDRESS"
            }
            Write-Ok "Switched to: IPv6 (Direct)"
        }
        "2" {
            Set-Content -Path $PREF_FILE -Value "direct" -Force
            if (Update-SSHConfigHostName -NewHostName $STATIC_IP) {
                Write-Ok "Updated SSH config to use: $STATIC_IP"
            }
            Write-Ok "Switched to: Direct SSH"
        }
        default {
            Write-Err "Invalid choice"
        }
    }
}

# Database tunnel
function Start-DBTunnel {
    Write-Info "Starting PostgreSQL tunnel on port $DB_LOCAL_PORT..."

    if (Test-PortInUse -Port $DB_LOCAL_PORT) {
        Write-Warn "Port $DB_LOCAL_PORT is already in use"
        Write-Info "Run: .\tunnel.ps1 db-kill"
        return
    }

    if (-not (Test-Path $KEY_PATH)) {
        Write-Err "SSH key not found: $KEY_PATH"
        Write-Info "Run: .\tunnel.ps1 setup"
        return
    }

    Set-SSHKeyPermissions -KeyPath $KEY_PATH

    # Start tunnel in background
    Start-Process -FilePath "ssh" -ArgumentList "-o", "ConnectTimeout=$SSH_TIMEOUT", "-o", "StrictHostKeyChecking=accept-new", "-L", "0.0.0.0:${DB_LOCAL_PORT}:${DB_REMOTE_HOST}:${DB_REMOTE_PORT}", "-N", $HOST_ALIAS -WindowStyle Hidden

    Start-Sleep -Seconds 2

    if (Test-PortInUse -Port $DB_LOCAL_PORT) {
        Write-Ok "Database tunnel started!"
        Write-Host ""
        Write-Info "DBeaver/pgAdmin connection settings:"
        Write-Host "  Host:     127.0.0.1"
        Write-Host "  Port:     $DB_LOCAL_PORT"
        Write-Host "  Database: valargen"
        Write-Host "  Username: valargen"
        Write-Host ""
        Write-Info "Stop with: .\tunnel.ps1 db-kill"
    } else {
        Write-Err "Failed to start database tunnel"
    }
}

# Kill database tunnel
function Stop-DBTunnel {
    Write-Info "Stopping database tunnel on port $DB_LOCAL_PORT..."

    $processId = Get-PortProcess -Port $DB_LOCAL_PORT
    if ($processId) {
        try {
            Stop-Process -Id $processId -Force
            Write-Ok "Database tunnel stopped (PID: $processId)"
        } catch {
            Write-Err "Failed to stop tunnel: $_"
        }
    } else {
        Write-Warn "No database tunnel running on port $DB_LOCAL_PORT"
    }
}

# Reset account
function Reset-Account {
    Write-Host "=== RESET ACCOUNT ===" -ForegroundColor Red
    Write-Host ""
    Write-Warn "This will remove all Valargen SSH configuration"
    Write-Host ""

    $confirm = Read-Host "Are you sure? This cannot be undone (y/n)"
    if ($confirm -notmatch "^[Yy]") {
        Write-Info "Reset cancelled"
        return
    }

    Write-Host ""
    Write-Info "Resetting account..."

    # Kill tunnel
    $processId = Get-PortProcess -Port $PROXY_PORT
    if ($processId) {
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        Write-Ok "Tunnel stopped"
    }

    # Remove SSH key (fix permissions first to avoid access denied)
    if (Test-Path $KEY_PATH) {
        # Grant full control before deletion to avoid permission errors
        $null = & icacls $KEY_PATH /grant "${env:USERNAME}:(F)" 2>&1
        Remove-Item $KEY_PATH -Force -ErrorAction SilentlyContinue
        if (-not (Test-Path $KEY_PATH)) {
            Write-Ok "Removed SSH private key"
        } else {
            Write-Warn "Could not remove private key - delete manually: $KEY_PATH"
        }
    }
    if (Test-Path "$KEY_PATH.pub") {
        Remove-Item "$KEY_PATH.pub" -Force -ErrorAction SilentlyContinue
        if (-not (Test-Path "$KEY_PATH.pub")) {
            Write-Ok "Removed SSH public key"
        } else {
            Write-Warn "Could not remove public key - delete manually: $KEY_PATH.pub"
        }
    }

    # Remove preference file
    if (Test-Path $PREF_FILE) {
        Remove-Item $PREF_FILE -Force
        Write-Ok "Removed connection preference"
    }

    # Remove role file
    if (Test-Path $ROLE_FILE) {
        Remove-Item $ROLE_FILE -Force
        Write-Ok "Removed role preference"
    }

    # Remove SSH config entry
    if (Test-Path $SSH_CONFIG) {
        $lines = Get-Content $SSH_CONFIG
        $newLines = @()
        $skipBlock = $false

        foreach ($line in $lines) {
            # Check if entering target host block
            if ($line -match "^Host\s+$HOST_ALIAS\s*$") {
                $skipBlock = $true
                continue
            }
            # Check if leaving host block (new Host line that's not our target)
            if ($skipBlock -and $line -match "^Host\s+" -and $line -notmatch "^Host\s+$HOST_ALIAS") {
                $skipBlock = $false
            }
            # Add line only if not in skip block
            if (-not $skipBlock) {
                $newLines += $line
            }
        }

        # Filter out empty lines at start/end and write
        $newLines = $newLines | Where-Object { $_.Trim() -ne "" -or $newLines.IndexOf($_) -gt 0 }
        if ($newLines.Count -gt 0) {
            $newLines | Set-Content $SSH_CONFIG -Force
        } else {
            # Config only had our entry, remove the file
            Remove-Item $SSH_CONFIG -Force -ErrorAction SilentlyContinue
        }
        Write-Ok "Removed SSH config entry for $HOST_ALIAS"
    }

    # Remove known_hosts entries for server IPs
    $knownHostsFile = "$env:USERPROFILE\.ssh\known_hosts"
    if (Test-Path $knownHostsFile) {
        $knownHostsContent = Get-Content $knownHostsFile
        $newKnownHosts = $knownHostsContent | Where-Object {
            $_ -notmatch [regex]::Escape($STATIC_IP) -and
            $_ -notmatch [regex]::Escape($IPV6_ADDRESS)
        }

        if ($newKnownHosts.Count -lt $knownHostsContent.Count) {
            if ($newKnownHosts.Count -gt 0) {
                $newKnownHosts | Set-Content $knownHostsFile -Force
            } else {
                Remove-Item $knownHostsFile -Force -ErrorAction SilentlyContinue
            }
            Write-Ok "Removed server entries from known_hosts"
        }
    }

    Write-Host ""
    Write-Ok "Account reset complete"
    Write-Info "Run: .\tunnel.ps1 setup"
}

# Diagnose
function Start-Diagnose {
    Write-Host "=== Client Machine Diagnostics ===" -ForegroundColor Green
    Write-Host ""

    $issues = 0

    # Check dependencies
    Write-Host "[1/5] Checking dependencies..." -ForegroundColor Blue

    if (Get-Command ssh -ErrorAction SilentlyContinue) {
        $sshVersion = & ssh -V 2>&1
        Write-Ok "ssh installed: $sshVersion"
    } else {
        Write-Err "ssh NOT installed - required"
        $issues++
    }

    if (Get-Command ssh-keygen -ErrorAction SilentlyContinue) {
        Write-Ok "ssh-keygen installed"
    } else {
        Write-Err "ssh-keygen NOT installed - required"
        $issues++
    }

    # Check network
    Write-Host ""
    Write-Host "[2/5] Checking network connectivity..." -ForegroundColor Blue

    try {
        $publicIP = (Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing -TimeoutSec 5).Content
        Write-Ok "Internet connectivity OK"
        Write-Info "Your public IP: $publicIP"
    } catch {
        Write-Warn "Cannot reach internet - check network"
    }

    # Check IPv6/IPv4
    Write-Host ""
    Write-Host "[3/5] Checking IPv6/IPv4 support..." -ForegroundColor Blue

    $ipv6Supported = Test-Connection -ComputerName "2001:4860:4860::8888" -Count 1 -Quiet -ErrorAction SilentlyContinue
    if ($ipv6Supported) {
        Write-Ok "IPv6 supported on this network"
    } else {
        Write-Warn "IPv6 not working (will use IPv4)"
    }

    $ipv4Supported = Test-Connection -ComputerName "8.8.8.8" -Count 1 -Quiet -ErrorAction SilentlyContinue
    if ($ipv4Supported) {
        Write-Ok "IPv4 supported"
    } else {
        Write-Err "IPv4 not working"
        $issues++
    }

    # Check SSH port
    Write-Host ""
    Write-Host "[4/5] Checking SSH port access..." -ForegroundColor Blue

    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $asyncResult = $tcpClient.BeginConnect($STATIC_IP, 22, $null, $null)
        $wait = $asyncResult.AsyncWaitHandle.WaitOne(5000, $false)
        if ($wait -and $tcpClient.Connected) {
            Write-Ok "SSH port 22 reachable on $STATIC_IP"
        } else {
            Write-Warn "Server $STATIC_IP not reachable - may need IP whitelist"
        }
        $tcpClient.Close()
    } catch {
        Write-Warn "Could not test SSH port"
    }

    # Check existing setup
    Write-Host ""
    Write-Host "[5/5] Checking existing setup..." -ForegroundColor Blue

    if (Test-Path $KEY_PATH) {
        Write-Ok "SSH key exists"
    } else {
        Write-Info "SSH key not generated yet"
    }

    if (Test-SSHConfigExists) {
        Write-Ok "SSH config exists"
    } else {
        Write-Info "SSH config not set up yet"
    }

    # Summary
    Write-Host ""
    Write-Host "=== Diagnosis Summary ===" -ForegroundColor Green

    if ($issues -eq 0) {
        Write-Ok "All checks passed! Ready to run: .\tunnel.ps1"
        Write-Host ""
        if ($ipv6Supported) {
            Write-Info "Recommended: IPv6 connection"
        } else {
            Write-Info "Will use: IPv4 connection"
        }
    } else {
        Write-Err "$issues issue(s) found"
        Write-Host ""
        Write-Warn "Fix the issues above before running setup"

        if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) {
            Write-Host ""
            Write-Info "Install OpenSSH:"
            Write-Info "  Settings > Apps > Optional Features > Add a feature"
            Write-Info "  Search for 'OpenSSH Client' and install"
        }
    }
}

# Show help
function Show-Help {
    Write-Host @"
Valargen SSH Setup & Tunnel (Windows)

Usage: .\tunnel.ps1 [COMMAND]

Commands:
  (none)          Auto-setup + auto-detect IPv6/IPv4 + start tunnel
  tunnel          Start SOCKS proxy tunnel for Postman (port $PROXY_PORT)
  kill            Stop existing tunnel on port $PROXY_PORT
  restart         Stop existing tunnel and start new one
  setup           Run setup wizard
  switch          Switch connection method (IPv6/IPv4)
  reset           Reset account - remove all configuration
  showkey         Display your public SSH key
  showip          Display configured server IPs and current mode
  status          Check connection status and requirements
  diagnose        Run client machine diagnostics
  db              Start PostgreSQL tunnel for DBeaver/pgAdmin (port $DB_LOCAL_PORT)
  db-kill         Stop PostgreSQL database tunnel
  help            Show this help message

First-Time Setup:
  1. Run: .\tunnel.ps1
  2. Copy the displayed SSH public key (auto-copied to clipboard)
  3. Send the key to your administrator
  4. Wait for admin to confirm key is added
  5. Run the script again to connect

Postman Proxy Setup:
  1. Run: .\tunnel.ps1 tunnel
  2. Postman > Settings > Proxy > SOCKS5 > 127.0.0.1:$PROXY_PORT

Files:
  SSH Key:    $KEY_PATH
  SSH Config: $SSH_CONFIG

"@
}

# Main switch
switch ($Command.ToLower()) {
    "" {
        if ((Test-Path $KEY_PATH) -and (Test-SSHConfigExists)) {
            Write-Ok "All requirements met"
            Start-Tunnel
        } else {
            Write-Host ""
            Write-Info "First-time setup detected. Running setup..."
            Write-Host ""
            Start-Setup
        }
    }
    "tunnel" { Start-Tunnel }
    "kill" { Stop-Tunnel }
    "restart" {
        Stop-Tunnel
        Start-Sleep -Seconds 1
        Start-Tunnel
    }
    "setup" { Start-Setup }
    "switch" { Switch-Method }
    "reset" { Reset-Account }
    "showkey" { Show-Key }
    "showip" { Show-IP }
    "status" { Show-Status }
    "diagnose" { Start-Diagnose }
    "diag" { Start-Diagnose }
    "check" { Start-Diagnose }
    "db" { Start-DBTunnel }
    "db-kill" { Stop-DBTunnel }
    "help" { Show-Help }
    "-h" { Show-Help }
    "--help" { Show-Help }
    default {
        Write-Err "Unknown command: $Command"
        Write-Info "Run: .\tunnel.ps1 help"
    }
}
