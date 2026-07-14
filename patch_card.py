with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\storefront.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('<div class="plan-card">')
end_idx = content.find('</template>', start_idx)

if start_idx != -1 and end_idx != -1:
    old_card = content[start_idx:end_idx]
    new_card = '''<div class="plan-card" style="padding: 0; border: 1px solid #e5e7eb; border-radius: 4px; background: #fff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; display: flex; flex-direction: column; overflow: hidden; transition: box-shadow 0.3s ease;">
            
            <div style="padding: 30px;">
              <!-- Top Section -->
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                  <h3 x-text="plan.name" style="margin: 0; font-size: 1.5rem; color: #1f2937;"></h3>
                  <img src="https://flagcdn.com/24x18/in.png" alt="India Flag" style="border-radius: 2px; width: 24px; height: 16px;">
                </div>
                <div style="color: #1f2937; font-size: 1.4rem; display: flex; gap: 10px;">
                  <i class="fa-brands fa-ubuntu"></i>
                  <i class="fa-brands fa-windows"></i>
                </div>
              </div>
              
              <div style="text-align: left; color: #dc2626; font-size: 0.95rem; font-weight: 600; margin-bottom: 25px;">Up to 35% Lifetime</div>
              
              <!-- Pricing -->
              <div class="plan-price" style="font-size: 2.5rem; font-weight: 700; color: #111827; margin: 10px 0;">
                $<span x-text="plan.price"></span><span style="font-size: 1.2rem; color: #4b5563; font-weight: 500;">/mo</span>
              </div>
              <div style="text-decoration: line-through; color: #6b7280; font-size: 1.1rem; margin-bottom: 5px;">
                $<span x-text="(plan.price * 1.53).toFixed(2)"></span>/mo
              </div>
              <div style="color: #dc2626; font-size: 0.95rem; margin-bottom: 25px;">1GBPS network speed</div>
              
              <!-- Order Button -->
              <button class="btn-buy" style="background: #0ea5e9; color: white; border: none; border-radius: 4px; padding: 12px; font-weight: 500; font-size: 1.1rem; width: 100%; margin-bottom: 30px; transition: background 0.2s; cursor: pointer;" @click="openCheckout(plan)" onmouseover="this.style.background='#0284c7'" onmouseout="this.style.background='#0ea5e9'">
                Order Now
              </button>
              
              <hr style="border: none; border-top: 1px solid #e5e7eb; margin-bottom: 20px;">
              <div style="color: #4b5563; font-size: 1rem; margin-bottom: 30px;">Renew at same discount price</div>
              
              <!-- Features List -->
              <div style="text-align: left; display: flex; flex-direction: column; gap: 25px;">
                <template x-for="(feature, index) in plan.description.split(' • ')" :key="index">
                  <div style="display: flex; align-items: center; gap: 20px;">
                    <div style="color: #0ea5e9; font-size: 1.8rem; width: 35px; text-align: center;">
                      <i class="fa-solid" :class="{
                        'fa-microchip': index === 0,
                        'fa-memory': index === 1,
                        'fa-hard-drive': index === 2,
                        'fa-gauge-high': index === 3,
                        'fa-clock': index === 4,
                        'fa-check': index > 4
                      }"></i>
                    </div>
                    <div style="display: flex; flex-direction: column;">
                      <span style="color: #4b5563; font-size: 0.9rem; margin-bottom: 4px;" x-text="['Processor', 'Memory / RAM', 'Storage Space', 'Network Speed', 'Delivery Time'][index] || 'Feature'"></span>
                      <span style="color: #111827; font-weight: 500; font-size: 1rem;" x-text="feature"></span>
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </div>
          '''
    content = content.replace(old_card, new_card)
    
    with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\storefront.html', 'w', encoding='utf-8') as f:
        f.write(content)
        print("Updated successfully")
else:
    print("Could not find block")
