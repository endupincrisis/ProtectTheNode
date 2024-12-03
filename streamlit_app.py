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

# Define the time range for hourly data
start_time = pd.Timestamp("2024-11-26 00:00:00")  # Tuesday before Thanksgiving
end_time = pd.Timestamp.now().replace(hour=22, minute=30, second=0, microsecond=0)
time_range = pd.date_range(start=start_time, end=end_time, freq="H")

# Generate sample data
def generate_device_data(device_name, actions, data_shared):
    data = pd.DataFrame({
        "DateTime": time_range,
        "Action Type": np.random.choice(actions, size=len(time_range)),
        "Requests Sent": np.random.randint(50, 100, size=len(time_range)),
        "Requests Accepted": np.random.randint(40, 90, size=len(time_range)),
        "Requests Failed": lambda x: x["Requests Sent"] - x["Requests Accepted"],
        "Source IP": [f"192.168.{np.random.randint(0, 10)}.{i % 255}" for i in range(len(time_range))],
        "Node Source IP": [f"10.0.{np.random.randint(0, 10)}.{i % 255}" for i in range(len(time_range))],
        "Data Shared": np.random.choice(data_shared, size=len(time_range)),
        "Device": [device_name] * len(time_range),
    })
    return data

# Amazon Echo Data
echo_data = generate_device_data(
    "Amazon Echo",
    actions=["Play Music", "Turn On Light", "Check Weather", "Set Alarm", "Volume Up"],
    data_shared=["Music Metadata", "Location", "None", "Alarm Time", "Volume Level"]
)

# Google Nest Doorbell Data
doorbell_data = generate_device_data(
    "Google Nest Doorbell",
    actions=["Packet Sent", "Stream Video", "Capture Snapshot", "Send Notification", "Idle"],
    data_shared=["Video Feed", "Snapshot", "None", "Notification Details", "None"]
)

# Merge Data for All Devices
all_data = pd.concat([echo_data, doorbell_data])

# Device Reports Tab
if selected_tab == "Device Reports":
    st.title("Smart Devices Blockchain Dashboard")

    # Overview Section
    st.header("Overview")
    st.metric("Total Devices", len(all_data["Device"].unique()))
    st.metric("Total Packets Transmitted", all_data["Requests Sent"].sum())
    st.metric("Filtered Packets", f"{np.random.randint(70, 90)}%")
    st.metric("Unfiltered Packets", f"{np.random.randint(10, 30)}%")
    st.metric("Active Policies", 15)

    # Device-Specific Panels
    device_selected = st.selectbox("Select a Device to View Details:", ["Amazon Echo", "Google Nest Doorbell"])

    if device_selected == "Amazon Echo":
        st.subheader("Amazon Echo Details")
        st.dataframe(echo_data)
        st.bar_chart(echo_data.groupby("DateTime")[["Requests Sent", "Requests Accepted", "Requests Failed"]].sum())

    elif device_selected == "Google Nest Doorbell":
        st.subheader("Google Nest Doorbell Details")
        st.dataframe(doorbell_data)
        st.line_chart(doorbell_data.groupby("DateTime")[["Requests Sent", "Requests Accepted", "Requests Failed"]].sum())

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
        st.line_chart(echo_data.groupby("DateTime")[["Requests Sent", "Requests Accepted", "Requests Failed"]].sum())
    elif device_selected_viz == "Google Nest Doorbell":
        st.line_chart(doorbell_data.groupby("DateTime")[["Requests Sent", "Requests Accepted", "Requests Failed"]].sum())

    # Footer Section
    st.write("Developed for secure, transparent smart device monitoring using Hyperledger Fabric.")

# Placeholder for other tabs
else:
    st.title(f"{selected_tab}")
    st.write(f"Content for {selected_tab} will be added here.")
