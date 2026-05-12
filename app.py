import streamlit as st
import random
import datetime

# Page configuration
st.set_page_config(page_title="CYS Claim - Free Rewards", page_icon="💰", layout="centered")

# App Title & Header
st.title("💰 CYS Claim & Share")
st.write("Welcome to the Ultimate Crypto Rewards & Referral Platform!")
st.markdown("---")

# Initialize Session State
if 'user_balance' not in st.session_state:
    st.session_state.user_balance = 0.0
if 'last_claim' not in st.session_state:
    st.session_state.last_claim = None

# Sidebar for Referral Info
st.sidebar.header("🔗 Your Referral Link")
st.sidebar.info("Share this link with friends to earn 10% bonus on every claim!")
st.sidebar.code("https://claimyshare.io?ref=CYS786XA", language="text")

# User Dashboard Area
st.subheader("👤 User Dashboard")
wallet_address = st.text_input("Enter your Crypto Wallet Address (SOL/USDT):", placeholder="e.g. 7xKjx... or 0x71...")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Your Current Balance", value=f"{round(st.session_state.user_balance, 5)} USDT")
with col2:
    status = "Never" if not st.session_state.last_claim else st.session_state.last_claim.strftime("%H:%M:%S")
    st.metric(label="Last Claim Status", value=status)

st.markdown("---")

# Claim Section
st.subheader("🎁 Claim Rewards")
if st.button("🚀 Claim Free Reward", use_container_width=True):
    if not wallet_address:
        st.error("⚠️ Please enter a valid wallet address first!")
    else:
        now = datetime.datetime.now()
        if st.session_state.last_claim and (now - st.session_state.last_claim).seconds < 10:
            time_left = 10 - (now - st.session_state.last_claim).seconds
            st.warning(f"⏳ Anti-Spam Cooldown active! Please wait {time_left} seconds.")
        else:
            reward = round(random.uniform(0.005, 0.025), 5)
            st.session_state.user_balance += reward
            st.session_state.last_claim = now
            st.success(f"🎉 Successfully claimed {reward} USDT!")
            st.balloons()

# Bottom Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2026 CYS Earning Platform. All Rights Reserved.</p>", unsafe_allow_html=True)
