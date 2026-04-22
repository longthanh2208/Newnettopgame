from flask import Flask, render_template, jsonify, request
import json
import os
import smtplib
import ssl
import logging
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import time
import secrets
import socket

# --- Force IPv4 for Render (Fix smtplib connection issues) ---
orig_getaddrinfo = socket.getaddrinfo
def patched_getaddrinfo(*args, **kwargs):
    res = orig_getaddrinfo(*args, **kwargs)
    return [r for r in res if r[0] == socket.AF_INET]
socket.getaddrinfo = patched_getaddrinfo

# --- Setup Logging ---
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static/images')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Data Store Paths ---
USER_DB_PATH = os.path.join(os.path.dirname(__file__), 'users.json')
PRODUCT_DB_PATH = os.path.join(os.path.dirname(__file__), 'products.json')
ORDER_DB_PATH = os.path.join(os.path.dirname(__file__), 'orders.json')
MESSAGE_DB_PATH = os.path.join(os.path.dirname(__file__), 'messages.json')
REVIEW_DB_PATH = os.path.join(os.path.dirname(__file__), 'reviews.json')

# --- Email Configuration ---
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_SENDER = os.environ.get("MAIL_SENDER")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

# --- Anti-Spam Configuration ---
MAIL_LIMIT = 5
MAIL_BLOCK_DURATION = 300 

# --- Helper Functions ---
def load_data(path, default=[]):
    if not os.path.exists(path):
        return default
    with open(path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default

def save_data(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def send_reset_email(to_email, reset_link):
    subject = "Khôi phục mật khẩu - NETTOPGAME"
    text_body = f"Chào bạn,\n\nNhấn vào link sau để đặt lại mật khẩu:\n{reset_link}\n\nLink này chỉ dùng được 1 lần và có hiệu lực trong 15 phút.\n\nTrân trọng,\nNETTOPGAME"
    html_body = f"""
    <html>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f7f9; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: #2563eb; margin: 0;">NETTOPGAME</h1>
                <p style="color: #64748b; font-size: 0.9rem;">Hệ thống nạp game uy tín</p>
            </div>
            <div style="border-top: 4px solid #2563eb; padding-top: 20px;">
                <h2 style="color: #1e293b; font-size: 1.5rem; margin-top: 0;">Khôi phục mật khẩu</h2>
                <p>Chào bạn,</p>
                <p>Chúng tôi nhận được yêu cầu đặt lại mật khẩu cho tài khoản gắn với email này. Nếu bạn không thực hiện yêu cầu này, hãy bỏ qua email.</p>
                <div style="text-align: center; margin: 35px 0;">
                    <a href="{reset_link}" style="background-color: #2563eb; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: 600; display: inline-block; box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);">ĐẶT LẠI MẬT KHẨU</a>
                </div>
                <p style="font-size: 0.9rem; color: #64748b;">Hoặc nhấn vào link dưới đây:</p>
                <p style="word-break: break-all; font-size: 0.85rem;"><a href="{reset_link}" style="color: #2563eb;">{reset_link}</a></p>
                <p style="font-size: 0.85rem; color: #94a3b8; background: #f8fafc; padding: 10px; border-radius: 6px;">Lưu ý: Link này chỉ có hiệu lực trong <strong>15 phút</strong> và chỉ sử dụng được 1 lần duy nhất.</p>
            </div>
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; text-align: center; color: #94a3b8; font-size: 0.8rem;">
                <p>© 2024 NETTOPGAME. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    message = MIMEMultipart("alternative")
    message["From"] = MAIL_SENDER
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(text_body, "plain", "utf-8"))
    message.attach(MIMEText(html_body, "html", "utf-8"))
    
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT, timeout=30) as server:
            server.starttls(context=context)
            server.login(MAIL_SENDER, MAIL_PASSWORD)
            server.sendmail(MAIL_SENDER, to_email, message.as_string())
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/products")
def get_products():
    return jsonify(load_data(PRODUCT_DB_PATH))

# --- Authentication ---
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data['email'].lower()
    users = load_data(USER_DB_PATH)
    if any(u['email'].lower() == email for u in users):
        return jsonify({"status": "error", "message": "Email đã được đăng ký!"}), 400
    new_user = {"id": len(users) + 1, "name": data['name'], "email": email, "password": generate_password_hash(data['password']), "role": "user"}
    users.append(new_user)
    save_data(USER_DB_PATH, users)
    user_copy = new_user.copy()
    user_copy.pop('password', None)
    return jsonify({"status": "success", "message": "Đăng ký thành công!", "user": user_copy})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data['email'].lower()
    users = load_data(USER_DB_PATH)
    user = next((u for u in users if u['email'].lower() == email), None)
    if user and check_password_hash(user.get('password', ''), data['password']):
        user_copy = user.copy()
        user_copy.pop('password', None)
        return jsonify({"status": "success", "message": "Đăng nhập thành công!", "user": user_copy})
    return jsonify({"status": "error", "message": "Email hoặc mật khẩu không chính xác!"}), 401

@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.json
    email = data.get('email', '').lower()
    users = load_data(USER_DB_PATH)
    user = next((u for u in users if u['email'].lower() == email), None)
    if not user:
        return jsonify({"status": "error", "message": "Email chưa đăng ký!"}), 404
        
    now = time.time()
    attempts = user.get('mail_attempts', [])
    recent_attempts = [t for t in attempts if now - t < MAIL_BLOCK_DURATION]
    if len(recent_attempts) >= MAIL_LIMIT:
        wait_time = int((recent_attempts[0] + MAIL_BLOCK_DURATION) - now)
        return jsonify({"status": "error", "message": f"Thử lại sau {wait_time} giây."}), 429
        
    reset_token = secrets.token_urlsafe(32)
    user['reset_token'] = reset_token
    user['reset_token_expiry'] = now + 900
    recent_attempts.append(now)
    user['mail_attempts'] = recent_attempts
    save_data(USER_DB_PATH, users)
    
    reset_link = f"{request.host_url.rstrip('/')}/reset-password?email={email}&token={reset_token}"
    if send_reset_email(email, reset_link):
        return jsonify({"status": "success", "message": "Link đã gửi đến Gmail!"})
    return jsonify({"status": "error", "message": "Lỗi gửi mail!"}), 500

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET": return render_template("index.html")
    data = request.json
    email = data.get('email', '').lower()
    new_password = data.get('password')
    token = data.get('token')
    
    users = load_data(USER_DB_PATH)
    for user in users:
        if user['email'].lower() == email:
            if user.get('reset_token') != token or time.time() > user.get('reset_token_expiry', 0):
                return jsonify({"status": "error", "message": "Token không hợp lệ!"}), 401
            user['password'] = generate_password_hash(new_password)
            user.pop('reset_token', None)
            user.pop('reset_token_expiry', None)
            save_data(USER_DB_PATH, users)
            return jsonify({"status": "success", "message": "Đã đổi mật khẩu!"})
    return jsonify({"status": "error", "message": "Không tìm thấy user!"}), 404

# --- Admin API (CRUD Products) ---
@app.route("/api/products", methods=["POST"])
def add_product():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "Thiếu ảnh!"}), 400
    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"status": "error", "message": "Ảnh không hợp lệ!"}), 400
    
    filename = secure_filename(f"{int(time.time())}_{file.filename}")
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    products = load_data(PRODUCT_DB_PATH)
    new_product = {
        "id": int(time.time()),
        "name": request.form.get('name'),
        "price": int(request.form.get('price')),
        "category": request.form.get('category'),
        "image": f"images/{filename}"
    }
    products.insert(0, new_product)
    save_data(PRODUCT_DB_PATH, products)
    return jsonify({"status": "success", "message": "Thêm thành công!"})

@app.route("/api/products/<int:p_id>", methods=["PUT", "DELETE"])
def manage_product(p_id):
    products = load_data(PRODUCT_DB_PATH)
    product = next((p for p in products if p['id'] == p_id), None)
    if not product: return jsonify({"status": "error", "message": "Lỗi!"}), 404

    if request.method == "DELETE":
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(product['image']))
        if os.path.exists(img_path): os.remove(img_path)
        products = [p for p in products if p['id'] != p_id]
        save_data(PRODUCT_DB_PATH, products)
        return jsonify({"status": "success", "message": "Đã xóa!"})

    elif request.method == "PUT":
        product['name'] = request.form.get('name')
        product['price'] = int(request.form.get('price'))
        product['category'] = request.form.get('category')
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                old_img = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(product['image']))
                if os.path.exists(old_img): os.remove(old_img)
                filename = secure_filename(f"{int(time.time())}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                product['image'] = f"images/{filename}"
        save_data(PRODUCT_DB_PATH, products)
        return jsonify({"status": "success", "message": "Đã cập nhật!"})

# --- Orders API ---
@app.route("/api/orders", methods=["GET", "POST"])
def manage_orders():
    orders = load_data(ORDER_DB_PATH)
    if request.method == "POST":
        data = request.json
        new_order = {
            "id": int(time.time()),
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "customer": data.get("customer", {}),
            "items": data.get("items", []),
            "subtotal": data.get("subtotal", 0),
            "shipping_fee": data.get("shipping_fee", 0),
            "total": data.get("total", 0),
            "payment": data.get("payment", {}),
            "status": "Chờ xử lý"
        }
        orders.insert(0, new_order)
        save_data(ORDER_DB_PATH, orders)
        return jsonify({"status": "success", "message": "Đặt hàng thành công!", "order_id": new_order["id"]})
    return jsonify(orders)

@app.route("/api/orders/<int:o_id>", methods=["PUT", "DELETE"])
def update_order(o_id):
    orders = load_data(ORDER_DB_PATH)
    order = next((o for o in orders if o['id'] == o_id), None)
    if not order: return jsonify({"status": "error", "message": "Lỗi!"}), 404
    if request.method == "DELETE":
        orders = [o for o in orders if o['id'] != o_id]
        save_data(ORDER_DB_PATH, orders)
        return jsonify({"status": "success", "message": "Đã xóa!"})
    elif request.method == "PUT":
        data = request.json
        new_status = data.get('status')
        if new_status in ["Chờ xử lý", "Đang giao", "Đã giao", "Đã hủy"]:
            order['status'] = new_status
            save_data(ORDER_DB_PATH, orders)
            return jsonify({"status": "success", "message": "Đã cập nhật!"})
        return jsonify({"status": "error", "message": "Lỗi!"}), 400

@app.route("/api/my-orders", methods=["GET"])
def get_my_orders():
    email = request.args.get('email', '').lower()
    if not email: return jsonify([])
    orders = load_data(ORDER_DB_PATH)
    user_orders = [o for o in orders if o.get('customer', {}).get('email', '').lower() == email]
    return jsonify(user_orders)

# --- Support Messages (Chat) ---
@app.route("/api/messages", methods=["GET", "POST"])
def handle_messages():
    messages = load_data(MESSAGE_DB_PATH)
    if request.method == "POST":
        data = request.json
        new_msg = {
            "id": int(time.time() * 1000),
            "user_email": data.get('user_email', '').lower(),
            "content": data.get('content', ''),
            "sender_role": data.get('sender_role', 'user'),
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        messages.append(new_msg)
        save_data(MESSAGE_DB_PATH, messages)
        return jsonify({"status": "success"})
    user_email = request.args.get('email', '').lower()
    is_admin = request.args.get('admin') == 'true'
    if is_admin: return jsonify(messages)
    return jsonify([m for m in messages if m['user_email'] == user_email])

# --- Product Reviews ---
@app.route("/api/reviews", methods=["POST"])
def add_review():
    data = request.json
    order_id = data.get('order_id')
    product_id = data.get('product_id')
    orders = load_data(ORDER_DB_PATH)
    order = next((o for o in orders if o['id'] == order_id), None)
    if not order or order.get('status') != "Đã giao":
        return jsonify({"status": "error", "message": "Chưa nhận hàng!"}), 403
    reviews = load_data(REVIEW_DB_PATH)
    if any(r.get('order_id') == order_id and r.get('product_id') == product_id for r in reviews):
        return jsonify({"status": "error", "message": "Đã đánh giá!"}), 400
    new_review = {
        "id": int(time.time() * 1000),
        "order_id": order_id,
        "product_id": product_id,
        "user_name": data.get('user_name', 'Ẩn danh'),
        "rating": int(data.get('rating', 5)),
        "comment": data.get('comment', ''),
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    reviews.append(new_review)
    save_data(REVIEW_DB_PATH, reviews)
    return jsonify({"status": "success", "message": "Cảm ơn!"})

@app.route("/api/reviews/<int:p_id>", methods=["GET"])
def get_product_reviews(p_id):
    reviews = load_data(REVIEW_DB_PATH)
    return jsonify([r for r in reviews if int(r['product_id']) == p_id])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
