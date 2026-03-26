import streamlit as st
import json
import random
from email_utils import send_otp_email
from utils import validate_password
from training.predict import predict_password
from training.predict import predict_password
from utils import validate_password
def generate_otp():
    return str(random.randint(100000, 999999))
# ======================
# LOAD DATA
# ======================
with open("users.json") as f:
    data = json.load(f)

# ======================
# SESSION STATE
# ======================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.page = "login"

# ======================
# LOGIN PAGE
# ======================
def login_page():
    st.title("🔐 Login System")

    col1, col2 = st.columns([3, 1])

    with col1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # 👇 Buttons in same row
        btn1, btn2, btn3 = st.columns(3)


        with btn1:
            if st.button("Login"):
                if username in data["users"] and data["users"][username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.role = "user"
                    st.session_state.username = username
                elif username in data["admin"] and data["admin"][username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.role = "admin"
                    st.session_state.username = username
                else:
                    st.error("Invalid credentials")

        with btn2:
            if st.button("Forgot Password"):
                st.session_state.page = "forgot"

        with btn3:
            if st.button("Create Account"):
                st.session_state.page = "signup"
# ======================
# FORGOT PASSWORD
# ======================
from email_utils import send_otp_email

def forgot_page():
    st.title("🔁 Forgot Password (OTP)")

    username = st.text_input("Enter Username")

    if st.button("Send OTP"):
        if username in data["users"]:
            otp = generate_otp()
            st.session_state.otp = otp
            st.session_state.reset_user = username

            email = data["users"][username]["email"]

            if send_otp_email(email, otp):
                st.success("OTP sent to your email")
            else:
                st.error("Failed to send email")

        else:
            st.error("User not found")

    otp_input = st.text_input("Enter OTP")

    if st.button("Verify OTP"):
        if otp_input == st.session_state.get("otp"):
            st.session_state.verified = True
            st.success("OTP Verified")
        else:
            st.error("Invalid OTP")

    if st.session_state.get("verified"):
        new_pass = st.text_input("New Password", type="password")

        if st.button("Update Password"):
            valid = validate_password(new_pass)

            if valid == "Valid":
                user = st.session_state.reset_user
                data["users"][user]["password"] = new_pass

                with open("users.json", "w") as f:
                    json.dump(data, f)

                st.success("Password updated successfully")
            else:
                st.error(valid)

    if st.button("Back"):
        st.session_state.page = "login"
# ======================
# USER DASHBOARD
# ======================
def user_dashboard():
    st.title("👤 User Dashboard")

    st.write(f"Welcome, {st.session_state.username}")

    # Password strength checker
    pwd = st.text_input("Check Password Strength", type="password")

    if st.button("Analyze"):
        st.write("ML:", predict_password(pwd))

    # Change password
    st.subheader("🔄 Change Password")

    old_pass = st.text_input("Old Password", type="password")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Update Password"):
        user = st.session_state.username

        if data["users"][user]["password"] == old_pass:
            valid = validate_password(new_pass)

            if valid == "Valid":
                data["users"][user]["password"] = new_pass
                with open("users.json", "w") as f:
                    json.dump(data, f)
                st.success("Password updated")
            else:
                st.error(valid)
        else:
            st.error("Wrong old password")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"

# ======================
# ADMIN DASHBOARD
# ======================
def admin_dashboard():
    st.title("🛠️ Admin Dashboard")

    st.write(f"Welcome Admin: {st.session_state.username}")

    # Show all users
    for user, info in data["users"].items():
        st.write(f"👤 {user}")
        st.write(f"🔐 Password: {info['password']}")
        st.write(f"📧 Email: {info['email']}")
        st.write("---")

    # Change admin password
    st.subheader("🔄 Change Admin Password")

    old_pass = st.text_input("Old Password", type="password")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Update Admin Password"):
        admin = st.session_state.username

        if data["admin"][admin]["password"] == old_pass:
            valid = validate_password(new_pass)

            if valid == "Valid":
                data["admin"][admin]["password"] = new_pass
                with open("users.json", "w") as f:
                    json.dump(data, f)
                st.success("Admin password updated")
            else:
                st.error(valid)
        else:
            st.error("Wrong old password")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"

# SIGN UP PAGE
def signup_page():
    st.title("🆕 Create Account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    # 🔥 Real-time strength check
    if password:
        st.write("Strength:", predict_password(password))

    if password != confirm:
        st.error("Passwords do not match")

    # SEND OTP
    if st.button("Send OTP"):
        if username in data["users"]:
            st.error("User already exists")
        else:
            otp = generate_otp()
            st.session_state.signup_otp = otp
            st.session_state.temp_user = {
                "username": username,
                "email": email,
                "password": password
            }

            if send_otp_email(email, otp):
                st.success("OTP sent to your email")
            else:
                st.error("Failed to send OTP")

    # VERIFY OTP
    otp_input = st.text_input("Enter OTP")

    if st.button("Verify & Create Account"):
        if otp_input == st.session_state.get("signup_otp"):
            user = st.session_state.temp_user

            # Validate password
            valid = validate_password(user["password"])

            if valid == "Valid":
                data["users"][user["username"]] = {
                    "password": user["password"],
                    "email": user["email"]
                }

                with open("users.json", "w") as f:
                    json.dump(data, f)

                st.success("Account created successfully 🎉")
            else:
                st.error(valid)
        else:
            st.error("Invalid OTP")

    if st.button("Back to Login"):
        st.session_state.page = "login"


# ======================
# ROUTING
# ======================
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "forgot":
        forgot_page()
    elif st.session_state.page == "signup":
        signup_page()
else:
    if st.session_state.role == "user":
        user_dashboard()
    elif st.session_state.role == "admin":
        admin_dashboard()