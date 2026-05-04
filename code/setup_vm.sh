#!/bin/bash
# =============================================================================
# VaidyaAI — GCP VM Setup Script
# Run this ONCE on a fresh GCP VM to set everything up
# =============================================================================
# What this script does, step by step:
#   1. Installs Nginx (the web server that will serve your site)
#   2. Installs Python dependencies for the mock/real server
#   3. Creates the folder where the frontend lives
#   4. Copies your frontend HTML into that folder
#   5. Configures Nginx to serve frontend + forward API calls to Python
#   6. Starts the mock server as a background service
# =============================================================================

set -e  # stop if any command fails

echo ""
echo "============================================"
echo "  VaidyaAI GCP VM Setup"
echo "============================================"
echo ""

# ── STEP 1: Install Nginx ─────────────────────────────────────────────────────
# Nginx is a web server. Think of it as the "receptionist" for your VM.
# - Someone visits your IP → Nginx answers
# - If they want the website → Nginx gives them the HTML file
# - If they call an API → Nginx passes the request to your Python app
echo "[1/6] Installing Nginx..."
sudo apt-get update -qq
sudo apt-get install -y nginx
echo "      ✓ Nginx installed"

# ── STEP 2: Install Python dependencies ──────────────────────────────────────
# FastAPI = the Python web framework your mock_server.py and ayush_app.py use
# Uvicorn = the process that actually runs FastAPI (like a runner for the app)
echo "[2/6] Installing Python dependencies..."
pip install fastapi uvicorn --break-system-packages -q
echo "      ✓ Python deps installed"

# ── STEP 3: Create frontend folder ───────────────────────────────────────────
# This is where Nginx will look for your HTML file when someone visits your IP
# /var/www/ is the standard Linux location for websites
echo "[3/6] Creating frontend directory..."
sudo mkdir -p /var/www/vaidyaai
echo "      ✓ Created /var/www/vaidyaai"

# ── STEP 4: Copy frontend HTML ───────────────────────────────────────────────
# The frontend HTML file needs to live in /var/www/vaidyaai/index.html
# Nginx will serve this file when anyone visits your VM's IP in a browser
echo "[4/6] Deploying frontend..."
if [ -f "vaidyaai_frontend.html" ]; then
    sudo cp vaidyaai_frontend.html /var/www/vaidyaai/index.html
    echo "      ✓ Frontend deployed to /var/www/vaidyaai/index.html"
else
    echo "      ⚠ vaidyaai_frontend.html not found in current folder"
    echo "        Copy it here and run: sudo cp vaidyaai_frontend.html /var/www/vaidyaai/index.html"
fi

# ── STEP 5: Configure Nginx ───────────────────────────────────────────────────
# This tells Nginx the rules:
#   - Serve HTML from /var/www/vaidyaai when someone visits /
#   - Forward any /api/ calls to Python on port 8001
echo "[5/6] Configuring Nginx..."
sudo cp nginx_vaidyaai.conf /etc/nginx/sites-available/vaidyaai
sudo ln -sf /etc/nginx/sites-available/vaidyaai /etc/nginx/sites-enabled/vaidyaai

# Remove the default Nginx page so it doesn't interfere
sudo rm -f /etc/nginx/sites-enabled/default

# Test that the config is valid before applying
sudo nginx -t
sudo systemctl reload nginx
sudo systemctl enable nginx
echo "      ✓ Nginx configured and running"

# ── STEP 6: Start the mock server ────────────────────────────────────────────
# The mock server runs on port 8001 in the background
# Nginx will forward /api/ requests to it
echo "[6/6] Starting mock server on port 8001..."
pkill -f "uvicorn mock_server" 2>/dev/null || true
nohup uvicorn mock_server:app --host 127.0.0.1 --port 8001 > /tmp/vaidyaai_server.log 2>&1 &
echo $! > /tmp/vaidyaai_server.pid
sleep 2

# Quick health check
if curl -s http://127.0.0.1:8001/health > /dev/null; then
    echo "      ✓ Mock server is running"
else
    echo "      ⚠ Mock server may not have started. Check: tail -20 /tmp/vaidyaai_server.log"
fi

# ── Done ─────────────────────────────────────────────────────────────────────
VM_IP=$(curl -s ifconfig.me 2>/dev/null || echo "YOUR_VM_IP")
echo ""
echo "============================================"
echo "  ✅ Setup complete!"
echo "============================================"
echo ""
echo "  Open in browser:  http://$VM_IP"
echo "  API health check: http://$VM_IP/health"
echo "  Server logs:      tail -f /tmp/vaidyaai_server.log"
echo ""
echo "  To switch to real backend later:"
echo "    ./start_real.sh"
echo ""
