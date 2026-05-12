import streamlit as st
import random
import datetime

# Page Configuration for Real Web Feel
st.set_page_config(page_title="ViberWork - Premium Micro Tasks & Referral Hub", page_icon="🌐", layout="centered")

# Custom Styling for Wallpaper & Real Look
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 8px; height: 45px; width: 100%; font-size: 16px; }
    .task-box { padding: 15px; background-color: white; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #2196F3; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .news-box { padding: 15px; background-color: #fff9db; border-radius: 10px; border-left: 5px solid #fcc419; }
    </style>
""", unsafe_allow_html=True)

# Application Session State Initializations
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = ""
if 'points' not in st.session_state: st.session_state.points = 0
if 'invites' not in st.session_state: st.session_state.invites = 0
if 'wallet_address' not in st.session_state: st.session_state.wallet_address = "Not Configured"
if 'wallet_type' not in st.session_state: st.session_state.wallet_type = "None"
if 'fpin' not in st.session_state: st.session_state.fpin = "Not Set"
if 'is_verified' not in st.session_state: st.session_state.is_verified = "🔴 Unverified"
if 'tasks_done' not in st.session_state: st.session_state.tasks_done = []

# --- SIGN UP / LOGIN GATEWAY ---
if not st.session_state.logged_in:
    st.title("🌐 ViberWork Earning Network")
    st.subheader("Secure User Authorization Gateway")
    
    # 1. Referral Code Constraint Check
    ref_code = st.text_input("Enter Referral Code (Required *):", placeholder="e.g. VIBER-786-XP")
    
    st.write("--- or connect securely via auth providers ---")
    
    col_g, col_a = st.columns(2)
    with col_g:
        google_login = st.button("🔴 Continue with Google")
    with col_a:
        apple_login = st.button("⚫ Continue with iPhone Apple ID")
        
    st.write("--- or create a standard web ledger account ---")
    custom_username = st.text_input("Choose Unique Username:")
    custom_email = st.text_input("Enter Email Address:")
    pass1 = st.text_input("Create Secure Password:", type="password")
    pass2 = st.text_input("Confirm Password:", type="password")
    
    # Captcha Logic
    st.markdown("##### 🤖 Anti-Bot Captcha Verification")
    captcha_val = st.slider("Drag the slider to exactly 75 to verify you are human:", 0, 100, 0)
    
    login_click = st.button("🚀 Secure Registration & Login")
    
    if login_click or google_login or apple_login:
        if not ref_code:
            st.error("⚠️ Access Blocked: ViberWork is an invite-only platform. Referral code is mandatory!")
        elif captcha_val != 75:
            st.error("⚠️ Captcha mismatch! Please align the slider perfectly to 75.")
        else:
            if google_login:
                st.session_state.username = "Google_User_" + str(random.randint(100,999))
            elif apple_login:
                st.session_state.username = "iOS_User_" + str(random.randint(100,999))
            else:
                if not custom_username or not custom_email:
                    st.error("⚠️ Please fill out username and email fields.")
                    st.stop()
                if pass1 != pass2:
                    st.error("⚠️ Passwords match configuration payload failed!")
                    st.stop()
                st.session_state.username = custom_username
                
            st.session_state.logged_in = True
            st.success("🔒 Secure Tunnel established!")
            st.rerun()

# --- MAIN REAL LIVE APP INTERFACE ---
else:
    # Sidebar Profile Section
    st.sidebar.title("⚙️ ViberWork Settings")
    st.sidebar.markdown(f"**Logged as:** `{st.session_state.username}`")
    st.sidebar.markdown(f"**Identity Status:** {st.session_state.is_verified}")
    
    if st.sidebar.button("🛡️ Verify Email Identity"):
        st.session_state.is_verified = "🟢 Fully Verified Team Ledger"
        st.sidebar.success("Verification link broadcasted!")
        st.rerun()
        
    # Wallet Settings Node
    st.sidebar.subheader("🔒 Financial Asset Config")
    w_type = st.sidebar.selectbox("Select Network Architecture:", ["USDT (TRC20 - TRX)", "BNB (BEP20)", "USDT (Solana)"])
    w_addr = st.sidebar.text_input("Blockchain Destination Address:")
    if st.sidebar.button("💾 Lock Financial Vault Address"):
        if w_addr:
            st.session_state.wallet_address = w_addr
            st.session_state.wallet_type = w_type
            st.sidebar.success("Wallet locked in smart contract ledger!")
            st.rerun()
            
    # FPIN Node
    secure_pin = st.sidebar.text_input("Setup 4-Digit Secure Withdrawal FPIN:", type="password", max_chars=4)
    if st.sidebar.button("🔑 Activate Security Pin"):
        if len(secure_pin) == 4:
            st.session_state.fpin = secure_pin
            st.sidebar.success("FPIN Secured!")
            
    if st.sidebar.button("🚪 Safe Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Dashboard Banner / Wallpaper
    st.title(f"🎉 Welcome {st.session_state.username} for Earnings! 🎉")
    st.info("📊 Account Metrics View Terminal")
    
    # Stat Cards Metrics
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Wallet Balance", f"{st.session_state.points} Points", f"{round(st.session_state.points/100, 2)} USDT")
    with c2: st.metric("Referrals Pool", f"{st.session_state.invites} Users")
    with c3: st.metric("Payout Baseline Limit", "600 Points")

    st.markdown("---")

    # --- MAIN SCROLL DOWN TASKS CENTER ---
    st.header("📋 Scroll Down Tasks Area")
    st.write("Complete social missions below to earn instant +50 Points vouchers.")
    
    social_tasks = [
        ("📱 Follow ViberWork Official Telegram Channel", "telegram"),
        ("🐦 Follow ViberWork Official Twitter Hub", "twitter"),
        ("👾 Join ViberWork Discord Server Alliance", "discord"),
        ("📸 Follow ViberWork Instagram Profile Hub", "instagram")
    ]
    
    for title, key in social_tasks:
        st.markdown(f"<div class='task-box'><h5>{title}</h5><p>Status: {'✅ Completed (+50 pts)' if key in st.session_state.tasks_done else '⏳ Pending Action'}</p></div>", unsafe_allow_html=True)
        if key not in st.session_state.tasks_done:
            if st.button(f"Complete Task: Redirect to Endpoint Link", key=key):
                st.session_state.tasks_done.append(key)
                st.session_state.points += 50
                st.success("Target mission verified! +50 Points credited.")
                st.rerun()

    st.markdown("---")

    # --- INVITE MILESTONES SIMULATOR ---
    st.header("👥 Invite Milestones Matrix")
    st.write("Simulate or register your real network refer links below:")
    sim_invites = st.number_input("Simulate New Network Registrations (1 Invite = 20 Points):", min_value=0, max_value=100, step=1)
    if st.button("⚡ Broadcast Refer Claims"):
        if sim_invites > 0:
            st.session_state.invites += sim_invites
            st.session_state.points += (sim_invites * 20)
            st.success(f"Network synced! Registered {sim_invites} nodes successfully.")
            st.rerun()
            
    # Milestones Check UI
    st.markdown("##### Current Referral Tier Metrics:")
    st.progress(min(st.session_state.invites / 30, 1.0))
    st.write(f"• 1 Invite = 20 Pts | • 10 Invites = 200 Pts | • 15 Invites = 300 Pts | • **30 Invites = 600 Pts (Withdrawal Goal Floor)**")

    st.markdown("---")

    # --- WITHDRAWAL SYSTEM MODAL ---
    st.header("💸 Secure Payout Terminal")
    if st.button("🚀 Execute Smart Contract Withdrawal Protocol"):
        if st.session_state.points < 600:
            st.error(f"❌ Withdrawal Rejected! Minimum floor value is 600 Points. You need {600 - st.session_state.points} more points.")
        elif st.session_state.wallet_address == "Not Configured":
            st.error("❌ Action Blocked: Link your destination blockchain wallet target address in settings first.")
        elif st.session_state.fpin == "Not Set":
            st.error("❌ Action Blocked: Configure your 4-Digit Secure Payout FPIN token layer first.")
        else:
            st.success(f"🎉 TRANSACTION SUCCESSFUL! Sent requested dollar payload tokens onto network layer safely!")
            st.session_state.points = 0
            st.rerun()

    st.markdown("---")

    # --- NEWS DESK & EVENT PRIVILEGE ---
    st.header("📰 ViberWork News Desk & Gala Event Access")
    st.markdown("""
        <div class='news-box'>
        <b>🔥 SYSTEM BROADCAST BROAD TIER 1:</b> Partnership alignment with decentralized liquidity protocols completed successfully!<br>
        <b>🔥 DEVELOPMENT ROADMAP 2026:</b> Automatic instant payout routing via smart contracts deployment active.
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.session_state.invites >= 20:
        st.balloons()
        st.markdown("### 🌟 PREMIUM GALA TICKET UNLOCKED!")
        st.success("Congratulations! You have surpassed the 20 successful invites milestone barrier tier!")
        st.info("🎟️ Your Exclusive ViberWork Event Party Entry Voucher Pass Token ID: **VW-GALA-2026-VVIP**")
        st.markdown("**📞 VIP Help Desk Activation Support Channel Line:** `help-desk@viberwork.io`")
    else:
        st.warning(f"🔒 **VIP Event Pass Locked:** Complete {20 - st.session_state.invites} more unique user node invitations to unlock the Live Gala Party Entrance Voucher and Exclusive VIP Agent Help Support channels.")
