from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random
import string

app = Flask(__name__)
app.secret_key = 'super_secret_crypto_key_cys'  # Isse secure rakhein
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///faucet_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Models ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    wallet_address = db.Column(db.String(100), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)  # Rewards balance (e.g., SOL/USDT)
    referral_code = db.Column(db.String(10), unique=True, nullable=False)
    referred_by = db.Column(db.String(10), nullable=True)
    last_claim_time = db.Column(db.DateTime, nullable=True)

# Function to generate unique referral code
def generate_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# --- Routes & Logic ---

@app.route('/')
def home():
    # URL se referral code check karna (e.g., ?ref=B52F61E7)
    ref = request.args.get('ref')
    if ref:
        session['joined_via_ref'] = ref
    return "<h1>Welcome to CYS Claim Website</h1><p>Use /register to start earning.</p>"

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    wallet = data.get('wallet_address')
    
    if User.query.filter((User.username == username) | (User.wallet_address == wallet)).first():
        return jsonify({"error": "User or Wallet already registered"}), 400
        
    ref_code = generate_ref_code()
    referred_by = session.get('joined_via_ref')
    
    new_user = User(
        username=username, 
        wallet_address=wallet, 
        referral_code=ref_code,
        referred_by=referred_by
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "message": "Registration successful!",
        "referral_link": f"https://yourdomain.com?ref={ref_code}"
    }), 201

@app.route('/claim', methods=['POST'])
def claim_reward():
    data = request.json
    wallet = data.get('wallet_address')
    
    user = User.query.filter_by(wallet_address=wallet).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    # Cooldown logic (e.g., 1 hour claim limit)
    current_time = datetime.utcnow()
    if user.last_claim_time and (current_time - user.last_claim_time) < timedelta(hours=1):
        time_left = timedelta(hours=1) - (current_time - user.last_claim_time)
        return jsonify({"error": f"Please wait {int(time_left.total_seconds() // 60)} minutes to claim again"}), 429
        
    # Generate random small crypto reward amount
    reward_amount = round(random.uniform(0.0005, 0.005), 5)
    user.balance += reward_amount
    user.last_claim_time = current_time
    
    # Referral Bonus Logic (Upar wale inviter ko 10% dena)
    if user.referred_by:
        inviter = User.query.filter_by(referral_code=user.referred_by).first()
        if inviter:
            inviter.balance += (reward_amount * 0.10) # 10% commission
            
    db.session.commit()
    return jsonify({
        "success": True, 
        "reward_claimed": reward_amount, 
        "new_balance": user.balance
    }), 200

@app.route('/user/<wallet>')
def get_user_stats(wallet):
    user = User.query.filter_by(wallet_address=wallet).first()
    if not user:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "username": user.username,
        "balance": user.balance,
        "referral_code": user.referral_code,
        "total_claims": user.last_claim_time.strftime('%Y-%m-%d %H:%M:%S') if user.last_claim_time else "Never"
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Database initialize karega
    app.run(debug=True)
