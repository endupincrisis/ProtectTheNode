import streamlit as st
import pandas as pd
import numpy as np

# Sidebar Menu
st.sidebar.title("Dashboard Menu")
menu_options = [
    "Device Reports",
    "WireShark Reports",
    "Test Case Reports",
    "Ledger Report",
    "Users and Privileges",
    "Devices and Policies"
]
selected_tab = st.sidebar.radio("Navigation", menu_options, index=0)

# Device Reports Tab
if selected_tab == "Device Reports":
    st.title("Smart Devices Blockchain Dashboard")
    
    # Sample DataFrames for the devices
    # Amazon Echo Data
    echo_data = pd.DataFrame({
        "Date": pd.date_range(start="2024-11-25", periods=10, freq="D"),
        "Request Type": ["Play Music", "Turn On Light", "Check Weather", "Set Alarm", "Volume Up"] * 2,
        "Requests Sent": np.random.randint(50, 100, size=10),
        "Requests Accepted": np.random.randint(40, 90, size=10),
        "Requests Failed": lambda x: x["Requests Sent"] - x["Requests Accepted"],
        "Source IP": [f"192.168.0.{i}" for i in range(10)],
        "Node Source IP": [f"10.0.0.{i}" for i in range(10)],
        "Data Shared": ["Music Metadata", "Location", "None", "Alarm Time", "Volume Level"] * 2,
        "Device": ["Amazon Echo"] * 10,
    })

    # Google Nest Doorbell Data
    doorbell_data = pd.DataFrame({
        "Date": pd.date_range(start="2024-11-25", periods=10, freq="D"),
        "Action Type": ["Packet Sent", "Stream Video", "Capture Snapshot", "Send Notification", "Idle"] * 2,
        "Packets Sent": np.random.randint(200, 500, size=10),
        "Packets Received": np.random.randint(190, 490, size=10),
        "Packets Dropped": lambda x: x["Packets Sent"] - x["Packets Received"],
        "Source IP": [f"192.168.1.{i}" for i in range(10)],
        "Node Source IP": [f"10.0.1.{i}" for i in range(10)],
        "Data Shared": ["Video Feed", "Snapshot", "None", "Notification Details", "None"] * 2,
        "Device": ["Google Nest Doorbell"] * 10,
    })

    # Merge Data for All Devices
    all_data = pd.concat([echo_data, doorbell_data])

    # Overview Section
    st.header("Overview")
    st.metric("Total Devices", len(all_data["Device"].unique()))
    st.metric("Total Packets Transmitted", all_data["Requests Sent"].sum() + all_data["Packets Sent"].sum())
    st.metric("Filtered Packets", f"{np.random.randint(70, 90)}%")
    st.metric("Unfiltered Packets", f"{np.random.randint(10, 30)}%")
    st.metric("Active Policies", 15)

    # Device-Specific Panels
    device_selected = st.selectbox("Select a Device to View Details:", ["Amazon Echo", "Google Nest Doorbell"])

    if device_selected == "Amazon Echo":
        st.subheader("Amazon Echo Details")
        st.dataframe(echo_data)
        st.bar_chart(echo_data[["Requests Sent", "Requests Accepted", "Requests Failed"]])

    elif device_selected == "Google Nest Doorbell":
        st.subheader("Google Nest Doorbell Details")
        st.dataframe(doorbell_data)
        st.line_chart(doorbell_data[["Packets Sent", "Packets Received", "Packets Dropped"]])

    # Policy Management Section
    st.header("Policy Management")
    st.write("Configure and manage data-sharing policies for connected devices.")

    # Policy Configuration Table
    policy_table = pd.DataFrame({
        "Device": ["Amazon Echo", "Google Nest Doorbell"],
        "Active Policies": ["Encrypt Music Metadata", "Anonymize Video Feed"],
        "Data Shared": ["Music Metadata", "Video Feed"],
        "Policy Compliance": ["Yes", "Yes"],
    })
    st.table(policy_table)

    # Alerts Section
    st.header("Alerts")
    alerts = [
        "Amazon Echo: High request failure rate detected!",
        "Google Nest Doorbell: Video feed data transmission unencrypted."
    ]
    for alert in alerts:
        st.error(alert)

    # Visualization Section
    st.header("Packet Flow Analysis")
    device_selected_viz = st.radio("Select a Device for Packet Analysis:", ["Amazon Echo", "Google Nest Doorbell"])

    if device_selected_viz == "Amazon Echo":
        st.line_chart(echo_data[["Requests Sent", "Requests Accepted", "Requests Failed"]])
    elif device_selected_viz == "Google Nest Doorbell":
        st.line_chart(doorbell_data[["Packets Sent", "Packets Received", "Packets Dropped"]])

    # Footer Section
    st.write("Developed for secure, transparent smart device monitoring using Hyperledger Fabric.")

# Placeholder for other tabs
else:
    st.title(f"{selected_tab}")
    st.write(f"Content for {selected_tab} will be added here.")

