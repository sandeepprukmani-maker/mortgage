#!/bin/bash
# Pre-flight checks before starting Valargen

set -e

echo "🔍 Running pre-flight checks..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "   Install: https://docs.docker.com/engine/install/"
    exit 1
fi
echo "✅ Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    exit 1
fi
echo "✅ Docker Compose is installed"

# Check if .env.local exists
if [ ! -f "app/server/.env.local" ]; then
    echo "❌ app/server/.env.local not found"
    echo "   Run: cp app/server/.env.sample app/server/.env.local"
    exit 1
fi
echo "✅ Environment file exists"

# Check if UFW is active
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(sudo ufw status 2>/dev/null | grep -i "Status:" | awk '{print $2}' || echo "inactive")

    if [ "$UFW_STATUS" = "active" ]; then
        echo "⚠️  UFW firewall is active"

        # Check if Docker rules exist in UFW
        if sudo grep -q "Docker network bridge" /etc/ufw/before.rules 2>/dev/null; then
            echo "✅ UFW is configured for Docker"
        else
            echo "❌ UFW is NOT configured for Docker"
            echo ""
            echo "   Docker containers won't be able to access external networks."
            echo "   This will break Google OAuth, UWM API, and other external services."
            echo ""
            echo "   Fix: sudo ./scripts/fix_docker_ufw.sh"
            echo ""
            read -p "   Run the fix now? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                sudo ./scripts/fix_docker_ufw.sh
                echo "✅ UFW configured for Docker"
            else
                echo "⚠️  Continuing without UFW fix (external network access will fail)"
            fi
        fi
    else
        echo "✅ UFW is inactive (no firewall issues)"
    fi
else
    echo "✅ UFW not installed (no firewall issues)"
fi

# Check if required Docker images exist
if ! docker image inspect valargen-local-server:latest &> /dev/null; then
    echo "⚠️  Docker image 'valargen-local-server:latest' not found"
    echo "   Building server image..."
    docker build -t valargen-local-server:latest ./app/server
    echo "✅ Server image built"
else
    echo "✅ Server Docker image exists"
fi

if ! docker image inspect valargen-local-client:latest &> /dev/null; then
    echo "⚠️  Docker image 'valargen-local-client:latest' not found"
    echo "   Building client image..."
    docker build -t valargen-local-client:latest ./app/client
    echo "✅ Client image built"
else
    echo "✅ Client Docker image exists"
fi

echo ""
echo "✅ All pre-flight checks passed!"
echo ""
echo "You can now start the application:"
echo "  ./scripts/start_local.sh"
