import os, secrets
from panel.utils.shell import sh

def provision_smm_panel(domain):
    # 1. Create directory structure for the domain
    site_dir = f"/var/www/{domain}"
    sh(f"mkdir -p {site_dir}/public_html")
    sh(f"mkdir -p {site_dir}/logs")
    
    # 2. Extract SMM script (assuming we have smm_script.zip in /opt/errormodz/)
    script_zip = "/opt/errormodz/smm_script.zip"
    if os.path.exists(script_zip):
        sh(f"unzip -q {script_zip} -d {site_dir}/public_html/")
    else:
        # Create a dummy index.html if zip doesn't exist for testing
        sh(f"echo '<h1>SMM Panel Provisioned for {domain}!</h1>' > {site_dir}/public_html/index.html")
        
    # 3. Create Nginx config
    # In reality, this would use panel/routes/websites_core.py logic to create the vhost
    # but for this script we assume it uses the core panel APIs or functions.
    
    # Generate random credentials
    username = 'admin'
    password = secrets.token_urlsafe(8)
    
    # 4. Set permissions
    sh(f"chown -R www-data:www-data {site_dir}")
    
    return username, password
