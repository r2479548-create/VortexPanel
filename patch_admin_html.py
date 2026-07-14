with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add User button
old_user_header = '''<div class="page-header">
          <div><div class="page-title">SaaS Users</div><div class="page-sub">Manage users who registered on the Storefront</div></div>
        </div>'''
new_user_header = '''<div class="page-header">
          <div><div class="page-title">SaaS Users</div><div class="page-sub">Manage users who registered on the Storefront</div></div>
          <button class="btn btn-primary" @click="userForm={username:'',email:'',password:''}; showUserModal=true"><i class="fa-solid fa-plus"></i> Add User</button>
        </div>'''
content = content.replace(old_user_header, new_user_header)

# Add User Modal
user_modal = '''
        <div class="modal" x-show="showUserModal" style="display:none">
          <div class="modal-content" @click.outside="showUserModal=false">
            <h3>Add New User</h3>
            <label class="form-label">Username</label>
            <input type="text" class="form-input" x-model="userForm.username">
            <label class="form-label">Email</label>
            <input type="email" class="form-input" x-model="userForm.email">
            <label class="form-label">Password</label>
            <input type="password" class="form-input" x-model="userForm.password">
            <div style="margin-top:20px; display:flex; justify-content:flex-end; gap:10px;">
              <button class="btn" @click="showUserModal=false">Cancel</button>
              <button class="btn btn-primary" @click="saveUser()">Save</button>
            </div>
          </div>
        </div>
'''
content = content.replace('      <!-- PLANS PAGE -->', user_modal + '\n      <!-- PLANS PAGE -->')

# Add Order button
old_order_header = '''<div class="page-header">
          <div><div class="page-title">SaaS Orders</div><div class="page-sub">View provisioned panels and domains</div></div>
        </div>'''
new_order_header = '''<div class="page-header">
          <div><div class="page-title">SaaS Orders</div><div class="page-sub">View provisioned panels and domains</div></div>
          <button class="btn btn-primary" @click="orderForm={username:'',plan_id:'',domain:'',status:'active'}; showOrderModal=true"><i class="fa-solid fa-plus"></i> Add Order</button>
        </div>'''
content = content.replace(old_order_header, new_order_header)

# Add Order Modal
order_modal = '''
        <div class="modal" x-show="showOrderModal" style="display:none">
          <div class="modal-content" @click.outside="showOrderModal=false">
            <h3>Add New Order</h3>
            <label class="form-label">Username (Must exist)</label>
            <input type="text" class="form-input" x-model="orderForm.username">
            <label class="form-label">Plan ID</label>
            <input type="number" class="form-input" x-model="orderForm.plan_id">
            <label class="form-label">Domain/Hostname</label>
            <input type="text" class="form-input" x-model="orderForm.domain">
            <label class="form-label">Status</label>
            <select class="form-input" x-model="orderForm.status">
              <option value="active">Active</option>
              <option value="pending">Pending</option>
              <option value="suspended">Suspended</option>
            </select>
            <div style="margin-top:20px; display:flex; justify-content:flex-end; gap:10px;">
              <button class="btn" @click="showOrderModal=false">Cancel</button>
              <button class="btn btn-primary" @click="saveOrder()">Save</button>
            </div>
          </div>
        </div>
'''
content = content.replace('      </div>\n\n    </div>\n  </div>', order_modal + '\n      </div>\n\n    </div>\n  </div>')

with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated admin.html')
