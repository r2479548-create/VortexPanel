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

with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure we don't insert it multiple times
if 'showUserModal=false' not in text:
    plans_idx = text.find('<!-- PLANS PAGE -->')
    if plans_idx != -1:
        text = text[:plans_idx] + user_modal + '\n      ' + text[plans_idx:]
        with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\admin.html', 'w', encoding='utf-8') as f:
            f.write(text)
        print('User Modal inserted.')
    else:
        print('PLANS PAGE not found.')
else:
    print('Modal already exists')
