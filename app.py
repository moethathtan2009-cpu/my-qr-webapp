from flask import Flask, render_template, request
import qrcode
import os

app = Flask(__name__)

# static folder မရှိရင် အလိုအလျောက် ဆောက်ခိုင်းခြင်း
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # HTML Form ကနေ User ရိုက်လိုက်တဲ့ အချက်အလက်တွေကို လှမ်းယူခြင်း
    user_input = request.form['user_input']
    file_name = request.form['file_name']
    full_file_name = file_name + ".png"
    
    # QR Code ပြုလုပ်ခြင်း
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(user_input)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # static folder ထဲမှာ ပုံကို သိမ်းဆည်းခြင်း (HTML ထဲမှာ ပြန်ပြလို့ရအောင်)
    img_path = os.path.join('static', full_file_name)
    img.save(img_path)
    
    return render_template('index.html', qr_image=full_file_name)

if __name__ == '__main__':
    # Server ပေါ်မှာ port နံပါတ် အရှင်ဖြစ်အောင် ပြောင်းလဲလိုက်တာပါ
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
