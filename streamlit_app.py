import streamlit as st

# Set page title
st.title("Login Page")

# Login form
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "admin" and password == "password":  # Replace with your own logic
        st.success("Login successful!")
        st.write("Welcome, admin!")  # Replace with your app's main content
    else:
        st.error("Invalid username or password")
