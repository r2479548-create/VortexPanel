import sys

new_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Storefront - Buy High Performance VPS</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/static/css/theme.css">
<script src="https://unpkg.com/alpinejs@3.14.9/dist/cdn.min.js" defer></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
  [x-cloak] { display: none !important; }
  .store-container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
  .header { text-align: center; margin-bottom: 60px; }
  .header h1 { font-size: 3rem; margin-bottom: 15px; background: linear-gradient(90deg, var(--accent), var(--accent-3)); -webkit-background-clip: text; color: transparent; }
  .plan-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
  .plan-card { background: var(--bg-card); border-radius: 20px; padding: 40px; text-align: center; box-shadow: var(--shadow-soft); transition: transform 0.3s ease; }
  .plan-card:hover { transform: translateY(-10px); }
  .plan-price { font-size: 2.5rem; font-weight: 700; margin: 20px 0; color: var(--text-primary); }
  .btn-buy { background: var(--accent); color: white; border: none; padding: 15px 30px; border-radius: 12px; font-weight: 600; cursor: pointer; width: 100%; font-size: 1.1rem; transition: background 0.3s; }
  .btn-buy:hover { background: #4f46e5; }
  .nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 40px; background: var(--bg-topbar); box-shadow: var(--shadow-soft); }
  
  /* Client Area Styles */
  .client-dashboard { margin-top: 40px; }
  .service-card { background: var(--bg-card); padding: 20px; border-radius: 15px; margin-bottom: 20px; box-shadow: var(--shadow-soft); display: flex; justify-content: space-between; align-items: center;}
  .service-details p { margin: 5px 0; }
  
  /* Crypto Modal */
  .crypto-box { border: 1px solid var(--border); padding: 20px; border-radius: 10px; margin-top: 20px; background: var(--bg-body); }
  .crypto-select { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid var(--border); background: var(--bg-card); color: var(--text-primary); margin-bottom: 15px; }
</style>
</head>
<body x-data="storefront()">

  <nav class="nav">
    <div style="font-weight:700;font-size:1.5rem;color:var(--accent)"><i class="fa-solid fa-server"></i> VPS STORE</div>
    <div>
      <template x-if="!user">
        <div>
          <button @click="view = 'login'" class="btn" style="margin-right:10px">Login</button>
          <button @click="view = 'register'" class="btn btn-primary">Register</button>
        </div>
      </template>
      <template x-if="user">
        <div>
          <span x-text="'Hello, ' + user.username" style="margin-right:20px; font-weight:600;"></span>
          <button @click="view = 'dashboard'" class="btn" style="margin-right:10px">Dashboard</button>
          <button @click="logout()" class="btn btn-danger">Logout</button>
        </div>
      </template>
    </div>
  </nav>

  <div class="store-container">
    
    <!-- HOME / PRICING VIEW -->
    <div x-show="view === 'home'" x-cloak>
      <div class="header">
        <h1>High Performance VPS Hosting</h1>
        <p style="color:var(--text-muted); font-size:1.2rem;">Enterprise-grade servers with crypto payments.</p>
      </div>

      <div class="plan-grid">
        <template x-for="plan in plans" :key="plan.id">
          <div class="plan-card">
            <h3 x-text="plan.name"></h3>
            <div class="plan-price" x-text="'$' + plan.price + '/mo'"></div>
            <div style="color:var(--text-secondary); margin-bottom:30px; text-align:left; font-size:0.95rem; line-height: 1.8;">
              <template x-for="feature in plan.description.split(' • ')">
                 <div><i class="fa-solid fa-check" style="color:var(--success); margin-right:8px;"></i> <span x-text="feature"></span></div>
              </template>
            </div>
            <button class="btn-buy" @click="openCheckout(plan)">Buy Now <i class="fa-solid fa-arrow-right"></i></button>
          </div>
        </template>
      </div>
    </div>
    
    <!-- CHECKOUT MODAL -->
    <div x-show="view === 'checkout'" x-cloak style="max-width:500px; margin:0 auto; background:var(--bg-card); padding:40px; border-radius:20px; box-shadow: var(--shadow-strong);">
      <h2>Checkout</h2>
      <p>You are purchasing: <strong x-text="selectedPlan?.name"></strong> for <strong x-text="'$' + selectedPlan?.price"></strong></p>
      
      <div style="margin-top:20px;">
        <label style="font-weight:600;display:block;margin-bottom:8px;">Select Payment Method</label>
        <select x-model="selectedMethod" class="crypto-select">
          <option value="BTC">Bitcoin (BTC)</option>
          <option value="ETH">Ethereum (ETH)</option>
          <option value="XMR">Monero (XMR)</option>
        </select>
      </div>
      
      <div class="crypto-box" x-show="selectedMethod">
        <p style="margin-top:0; font-weight:600;">Please send <span x-text="'$' + selectedPlan?.price"></span> in <span x-text="selectedMethod"></span> to:</p>
        <div style="background:#000; color:#0f0; padding:15px; border-radius:8px; font-family:monospace; word-break:break-all; font-size:0.9rem;" x-text="cryptoAddresses[selectedMethod]"></div>
        <p style="font-size:0.85rem; color:var(--text-muted); margin-top:10px;">Once paid, click the button below. Your VPS will be provisioned after 1 network confirmation.</p>
      </div>
      
      <div style="display:flex; gap:10px; margin-top:30px;">
        <button class="btn" style="flex:1;" @click="view = 'home'">Cancel</button>
        <button class="btn-buy" style="flex:2;" @click="completeOrder()" :disabled="orderLoading">
          <span x-show="!orderLoading">I have paid</span>
          <span x-show="orderLoading">Processing...</span>
        </button>
      </div>
    </div>

    <!-- CLIENT DASHBOARD VIEW -->
    <div x-show="view === 'dashboard'" x-cloak>
      <h2>My Services</h2>
      <template x-if="orders.length === 0">
        <p>You don't have any active services yet. <a href="#" @click.prevent="view = 'home'">Browse Plans</a></p>
      </template>
      <template x-for="order in orders" :key="order.id">
        <div class="service-card">
          <div class="service-details">
            <h3 x-text="order.plan"></h3>
            <p><strong>Hostname:</strong> <span x-text="order.domain"></span></p>
            <p><strong>Status:</strong> <span class="badge" x-text="order.status"></span></p>
          </div>
          <div class="service-credentials" style="background:#f1f5f9; padding:15px; border-radius:10px;" x-show="order.status === 'active'">
            <h4 style="margin-top:0;">Server Login</h4>
            <p><strong>IP Address:</strong> <span x-text="order.username"></span></p>
            <p><strong>Root Password:</strong> <span x-text="order.password"></span></p>
          </div>
          <div x-show="order.status === 'pending'" style="color:var(--warning)">
            <i class="fa-solid fa-clock fa-spin"></i> Awaiting Crypto Confirmation
          </div>
        </div>
      </template>
    </div>

    <!-- LOGIN/REGISTER MODALS -->
    <div x-show="view === 'login'" x-cloak style="max-width:400px; margin:0 auto; background:var(--bg-card); padding:40px; border-radius:20px;">
      <h2>Login</h2>
      <input type="email" x-model="loginData.email" class="form-input" placeholder="Email" style="margin-bottom:15px">
      <input type="password" x-model="loginData.password" class="form-input" placeholder="Password" style="margin-bottom:20px">
      <button class="btn-buy" @click="doLogin()">Login</button>
      <p style="text-align:center; margin-top:15px; cursor:pointer;" @click="view = 'register'">Don't have an account? Register</p>
    </div>

    <div x-show="view === 'register'" x-cloak style="max-width:400px; margin:0 auto; background:var(--bg-card); padding:40px; border-radius:20px;">
      <h2>Register</h2>
      <input type="text" x-model="registerData.username" class="form-input" placeholder="Username" style="margin-bottom:15px">
      <input type="email" x-model="registerData.email" class="form-input" placeholder="Email" style="margin-bottom:15px">
      <input type="password" x-model="registerData.password" class="form-input" placeholder="Password" style="margin-bottom:20px">
      <button class="btn-buy" @click="doRegister()">Create Account</button>
      <p style="text-align:center; margin-top:15px; cursor:pointer;" @click="view = 'login'">Already have an account? Login</p>
    </div>

  </div>

  <script>
    document.addEventListener('alpine:init', () => {
      Alpine.data('storefront', () => ({
        view: 'home',
        user: null,
        plans: [],
        orders: [],
        loginData: { email: '', password: '' },
        registerData: { username: '', email: '', password: '' },
        
        // Checkout state
        selectedPlan: null,
        selectedMethod: 'BTC',
        orderLoading: false,
        cryptoAddresses: {
            'BTC': 'bc1q_YOUR_BTC_ADDRESS_HERE_CHANGE_ME_LATER',
            'ETH': '0xYOUR_ETH_ADDRESS_HERE_CHANGE_ME_LATER',
            'XMR': '4YOUR_MONERO_ADDRESS_HERE_CHANGE_ME_LATER'
        },

        init() {
          this.fetchPlans();
          this.checkAuth();
        },
        async fetchPlans() {
          const res = await fetch('/api/store/plans');
          this.plans = await res.json();
        },
        async checkAuth() {
          const res = await fetch('/api/store/me');
          const data = await res.json();
          if (data.loggedIn) {
            this.user = data.user;
            this.orders = data.orders;
          }
        },
        openCheckout(plan) {
            if (!this.user) {
                alert('Please login or register first to buy a VPS.');
                this.view = 'register';
                return;
            }
            this.selectedPlan = plan;
            this.view = 'checkout';
        },
        async completeOrder() {
            this.orderLoading = true;
            try {
                const res = await fetch('/api/store/buy', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        plan_id: this.selectedPlan.id,
                        payment_method: this.selectedMethod,
                        domain: 'vps-' + Math.floor(Math.random() * 1000000) + '.local'
                    })
                });
                const data = await res.json();
                if (data.success) {
                    alert('Order placed successfully! It will be provisioned once crypto payment is verified.');
                    await this.checkAuth();
                    this.view = 'dashboard';
                } else {
                    alert(data.error || 'Failed to place order.');
                }
            } catch (e) {
                alert('An error occurred.');
            }
            this.orderLoading = false;
        },
        async doLogin() {
          const res = await fetch('/api/store/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(this.loginData)
          });
          if (res.ok) {
            await this.checkAuth();
            this.view = 'home';
          } else {
            alert('Invalid login');
          }
        },
        async doRegister() {
          const res = await fetch('/api/store/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(this.registerData)
          });
          if (res.ok) {
            alert('Registered successfully! You can now login.');
            this.view = 'login';
          } else {
            alert('Registration failed');
          }
        },
        async logout() {
          await fetch('/api/store/logout', { method: 'POST' });
          this.user = null;
          this.orders = [];
          this.view = 'home';
        }
      }));
    });
  </script>
</body>
</html>
"""

with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\storefront.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Storefront HTML completely updated.")
