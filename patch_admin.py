import os
import sys

with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

pages_html = '''
      <!-- USERS PAGE -->
      <div x-show="page==='users'" x-data="usersPage()">
        <div class="page-header">
          <div><div class="page-title">SaaS Users</div><div class="page-sub">Manage users who registered on the Storefront</div></div>
        </div>
        <div class="card">
          <table class="table">
            <thead><tr><th>ID</th><th>Username</th><th>Email</th><th>Registered On</th></tr></thead>
            <tbody>
              <template x-for="u in users" :key="u.id">
                <tr>
                  <td x-text="u.id"></td>
                  <td x-text="u.username"></td>
                  <td x-text="u.email"></td>
                  <td x-text="u.created_at"></td>
                </tr>
              </template>
              <tr x-show="users.length===0"><td colspan="4" style="text-align:center">No users found.</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- PLANS PAGE -->
      <div x-show="page==='plans'" x-data="plansPage()">
        <div class="page-header">
          <div><div class="page-title">SaaS Plans</div><div class="page-sub">Manage your hosting products and prices</div></div>
          <div><button class="btn btn-primary" @click="edit(null)">Create New Plan</button></div>
        </div>
        <div class="card">
          <table class="table">
            <thead><tr><th>ID</th><th>Plan Name</th><th>Price</th><th>Billing Cycle</th><th>Type</th><th>Actions</th></tr></thead>
            <tbody>
              <template x-for="p in plans" :key="p.id">
                <tr>
                  <td x-text="p.id"></td>
                  <td x-text="p.name"></td>
                  <td x-text="'$' + p.price"></td>
                  <td x-text="p.billing_cycle" style="text-transform:capitalize"></td>
                  <td x-text="p.script_type"></td>
                  <td>
                    <button class="btn btn-sm btn-ghost" @click="edit(p)">Edit</button>
                    <button class="btn btn-sm btn-ghost" style="color:var(--red)" @click="del(p.id)">Delete</button>
                  </td>
                </tr>
              </template>
              <tr x-show="plans.length===0"><td colspan="6" style="text-align:center">No plans created yet.</td></tr>
            </tbody>
          </table>
        </div>
        
        <!-- Plan Modal -->
        <div x-show="showModal" class="modal-overlay" style="display:none" x-transition>
          <div class="modal" @click.outside="showModal=false">
            <div class="modal-header">
              <div class="modal-title" x-text="form.id ? 'Edit Plan' : 'Create Plan'"></div>
              <button class="modal-close" @click="showModal=false">×</button>
            </div>
            <div class="modal-body">
              <div class="form-group">
                <label>Plan Name</label>
                <input type="text" class="form-control" x-model="form.name" placeholder="e.g. Basic SMM">
              </div>
              <div class="form-group">
                <label>Description</label>
                <textarea class="form-control" x-model="form.description" rows="2"></textarea>
              </div>
              <div class="form-group">
                <label>Price ($)</label>
                <input type="number" class="form-control" x-model="form.price" step="0.01">
              </div>
              <div class="form-group">
                <label>Billing Cycle</label>
                <select class="form-control" x-model="form.billing_cycle">
                  <option value="monthly">Monthly</option>
                  <option value="yearly">Yearly</option>
                  <option value="one-time">One-Time</option>
                </select>
              </div>
              <div class="form-group">
                <label>Provisioning Script</label>
                <select class="form-control" x-model="form.script_type">
                  <option value="smm">Auto-Install SMM Panel</option>
                  <option value="wordpress">Auto-Install WordPress</option>
                  <option value="none">None (Empty Hosting)</option>
                </select>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-ghost" @click="showModal=false">Cancel</button>
              <button class="btn btn-primary" @click="save()">Save Plan</button>
            </div>
          </div>
        </div>
      </div>

      <!-- ORDERS PAGE -->
      <div x-show="page==='orders'" x-data="ordersPage()">
        <div class="page-header">
          <div><div class="page-title">SaaS Orders</div><div class="page-sub">View provisioned panels and domains</div></div>
        </div>
        <div class="card">
          <table class="table">
            <thead><tr><th>ID</th><th>User</th><th>Plan</th><th>Domain</th><th>Status</th><th>Created</th></tr></thead>
            <tbody>
              <template x-for="o in orders" :key="o.id">
                <tr>
                  <td x-text="o.id"></td>
                  <td x-text="o.username"></td>
                  <td x-text="o.plan"></td>
                  <td x-text="o.domain"></td>
                  <td>
                    <span :class="'badge ' + (o.status==='active'?'badge-green':'badge-gray')" x-text="o.status"></span>
                  </td>
                  <td x-text="o.created_at"></td>
                </tr>
              </template>
              <tr x-show="orders.length===0"><td colspan="6" style="text-align:center">No orders yet.</td></tr>
            </tbody>
          </table>
        </div>
      </div>
'''

target_tag = '<!-- -- NEONCODEX AI PANEL (inside main layout) --------------------------- -->'
if target_tag in html:
    html = html.replace(target_tag, pages_html + '\n    ' + target_tag)
else:
    # Append right before closing tag
    html = html.replace('</div>\n</div>\n\n<!-- Auth Overlay', pages_html + '\n</div>\n</div>\n\n<!-- Auth Overlay')

with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
