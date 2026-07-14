with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# First, remove the misplaced user_modal
user_modal_start = text.find('<div class="modal" x-show="showUserModal" style="display:none">')
if user_modal_start != -1:
    user_modal_end = text.find('<!-- PLANS PAGE -->')
    user_modal_block = text[user_modal_start:user_modal_end]
    text = text.replace(user_modal_block, '')

# We also need to remove the misplaced order_modal if it exists
order_modal_start = text.find('<div class="modal" x-show="showOrderModal" style="display:none">')
if order_modal_start != -1:
    order_modal_end = text.find('<!-- -- NEONCODEX AI PANEL')
    if order_modal_end != -1:
        order_modal_block = text[order_modal_start:order_modal_end]
        text = text.replace(order_modal_block, '')

# Now properly insert them inside the closing </div> of the respective pages.
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
users_end = '        </div>\n      </div>\n\n      <!-- PLANS PAGE -->'
text = text.replace(users_end, '        </div>\n' + user_modal + '      </div>\n\n      <!-- PLANS PAGE -->')

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
orders_end = '        </div>\n      </div>\n\n    <!-- -- NEONCODEX AI PANEL'
text = text.replace(orders_end, '        </div>\n' + order_modal + '      </div>\n\n    <!-- -- NEONCODEX AI PANEL')

with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed HTML modals')
