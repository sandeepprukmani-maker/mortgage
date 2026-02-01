#!/bin/bash
# Fix Docker networking with UFW
# This script configures UFW to allow Docker containers to access external networks

echo "Fixing Docker networking with UFW..."

# Backup UFW before.rules
sudo cp /etc/ufw/before.rules /etc/ufw/before.rules.backup.$(date +%Y%m%d_%H%M%S)

# Check if Docker rules already exist
if ! sudo grep -q "# Docker network bridge" /etc/ufw/before.rules; then
    echo "Adding Docker rules to UFW before.rules..."

    # Add Docker rules to before.rules (before the final COMMIT line)
    sudo sed -i '/^COMMIT$/i \
# Docker network bridge\
*nat\
:POSTROUTING ACCEPT [0:0]\
-A POSTROUTING ! -o docker0 -s 172.17.0.0/16 -j MASQUERADE\
-A POSTROUTING ! -o br-+ -s 172.18.0.0/16 -j MASQUERADE\
-A POSTROUTING ! -o br-+ -s 172.19.0.0/16 -j MASQUERADE\
-A POSTROUTING ! -o br-+ -s 172.20.0.0/16 -j MASQUERADE\
COMMIT\
' /etc/ufw/before.rules
else
    echo "Docker rules already exist in UFW before.rules"
fi

# Set default forward policy to ACCEPT
echo "Setting UFW forward policy to ACCEPT..."
sudo ufw default allow routed

# Reload UFW
echo "Reloading UFW..."
sudo ufw reload

# Restart Docker
echo "Restarting Docker..."
sudo systemctl restart docker

echo "Done! Docker should now be able to access external networks."
echo "You may need to restart your containers: docker compose restart"
