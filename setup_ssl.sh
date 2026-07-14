#!/bin/bash

# ERRORMODZ SSL Setup Script (Nginx + Let's Encrypt)
# Usage: sudo bash setup_ssl.sh <your_domain.com>

# Must run as root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run this script as root: sudo bash setup_ssl.sh"
  exit 1
fi

DOMAIN=$1

if [ -z "$DOMAIN" ]; then
    echo "Enter your domain name (e.g., panel.yourdomain.com):"
    read DOMAIN
fi

if [ -z "$DOMAIN" ]; then
    echo "❌ Domain name cannot be empty."
    exit 1
fi

echo "============================================="
echo " Setting up Real SSL for $DOMAIN"
echo "============================================="

# 1. Update and install Nginx & Certbot
echo "[1/4] Installing Nginx and Certbot..."
apt update
apt install -y nginx certbot python3-certbot-nginx

# 2. Stop Nginx to ensure ports 80/443 are free for the standalone certbot challenge
systemctl stop nginx

# 3. Request SSL Certificate
echo "[2/4] Requesting Let's Encrypt SSL certificate..."
# We use standalone in case Nginx isn't fully configured yet
certbot certonly --standalone -d "$DOMAIN" --non-interactive --agree-tos -m "admin@$DOMAIN"

if [ $? -ne 0 ]; then
    echo "❌ SSL Certificate request failed."
    echo "Please ensure that your domain ($DOMAIN) is pointing to this server's public IP address."
    systemctl start nginx
    exit 1
fi

# 4. Create Nginx Configuration
echo "[3/4] Configuring Nginx Reverse Proxy..."
NGINX_CONF="/etc/nginx/sites-available/$DOMAIN"
cat > "$NGINX_CONF" << EOF
server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN;

    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:8888;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

# Enable the site
ln -sf "$NGINX_CONF" "/etc/nginx/sites-enabled/"

# Remove default nginx site if exists
rm -f /etc/nginx/sites-enabled/default

# 5. Restart Nginx
echo "[4/4] Restarting Nginx..."
systemctl restart nginx

echo "============================================="
echo "✅ SSL Setup Complete!"
echo "You can now access your panel securely at:"
echo "👉 https://$DOMAIN"
echo "============================================="
