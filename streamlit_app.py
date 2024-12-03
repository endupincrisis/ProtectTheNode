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
    "Devices and Policies",
    "Data Sharing"
]
selected_tab = st.sidebar.radio("Navigation", menu_options, index=0)

# Generate consistent data
start_time = pd.Timestamp("2024-11-26 00:00:00")
end_time = pd.Timestamp.now().replace(hour=22, minute=30, second=0, microsecond=0)
time_range = pd.date_range(start=start_time, end=end_time, freq="15T")

# Function to generate realistic data with range validation
def generate_device_data(device_name, total_packets, total_requests):
    size = len(time_range)
    max_packets_per_interval = max(1, total_packets // size)
    max_requests_per_interval = max(1, total_requests // size)

    packets_sent = np.random.randint(1, max_packets_per_interval + 1, size)
    packets_received = np.maximum(0, packets_sent - np.random.randint(0, 3, size))
    requests_sent = np.random.randint(1, max_requests_per_interval + 1, size)
    requests_received = np.maximum(0, requests_sent - np.random.randint(0, 2, size))

    return pd.DataFrame({
        "Time": time_range,
        "Packets Sent": packets_sent,
        "Packets Received": packets_received,
        "Requests Sent": requests_sent,
        "Requests Received": requests_received,
        "Failures": requests_sent - requests_received,
        "Device": [device_name] * size
    })

# Data for devices
echo_total_packets = 20000
echo_total_requests = 15000
nest_total_packets = 10000
nest_total_requests = 8000

echo_data = generate_device_data("Amazon Echo", echo_total_packets, echo_total_requests)
nest_data = generate_device_data("Google Nest Doorbell", nest_total_packets, nest_total_requests)

# Combine all data
all_data = pd.concat([echo_data, nest_data])

# Data Sharing Page
if selected_tab == "Data Sharing":
    st.title("Data Sharing")
    st.header("Restricted Sites and User Controls")

    # Restricted Sites Table
    restricted_sites = pd.DataFrame({
        "User": ["Stephanie", "Lucy", "James"],
        "Device": ["Amazon Echo", "Google Nest Doorbell", "Amazon Echo"],
        "Restricted Site": ["iTunes", "YouTube", "Spotify"],
        "Reason for Restriction": ["Explicit Content", "Work Hours Restriction", "Data Sharing Limit"]
    })
    st.subheader("Restricted Sites")
    st.table(restricted_sites)

    # Data Sharing Preferences
    st.subheader("User Data Sharing Preferences")
    properties = [
        "Volume Control",
        "Light Settings",
        "Temperature",
        "Door Lock Status",
        "Camera Feed Access",
        "Motion Detection Sensitivity",
        "Device Location Sharing"
    ]
    data_sharing = pd.DataFrame({
        "Property": properties,
        "Frequency": np.random.choice(["Always", "Daily", "Weekly", "Never"], len(properties)),
        "Allowed by User": np.random.choice(["Yes", "No"], len(properties))
    })
    st.table(data_sharing)

    # User Customization
    st.subheader("Customize Data Sharing Preferences")
    for property in properties:
        st.write(f"Control for {property}")
        allowed = st.radio(f"Allow sharing of {property}?", ["Yes", "No"], key=property)
        frequency = st.selectbox(
            f"Set frequency for sharing {property}",
            ["Always", "Daily", "Weekly", "Never"],
            key=f"{property}_freq"
        )
        st.write(f"Your choice: Sharing {property} - {allowed}, Frequency - {frequency}")

# Other Pages (Device Reports, WireShark, etc.)
elif selected_tab == "Device Reports":
    st.title("Device Reports")
    st.header("Overall Device Metrics")

    # Totals Table
    device_totals = pd.DataFrame({
        "Device": ["Amazon Echo", "Google Nest Doorbell"],
        "Packets Sent": [echo_data["Packets Sent"].sum(), nest_data["Packets Sent"].sum()],
        "Packets Received": [echo_data["Packets Received"].sum(), nest_data["Packets Received"].sum()],
        "Requests Sent": [echo_data["Requests Sent"].sum(), nest_data["Requests Sent"].sum()],
        "Requests Received": [echo_data["Requests Received"].sum(), nest_data["Requests Received"].sum()],
        "Failures": [echo_data["Failures"].sum(), nest_data["Failures"].sum()]
    })
    st.table(device_totals)

    st.subheader("Device Totals Breakdown")
    st.bar_chart(device_totals.set_index("Device")[["Packets Sent", "Packets Received", "Requests Sent", "Requests Received"]])

# Placeholder for other pages
else:
    st.title(f"{selected_tab}")
    st.write(f"Content for {selected_tab} will be added here.")
