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

# Generate consistent data
start_time = pd.Timestamp("2024-11-26 00:00:00")
end_time = pd.Timestamp.now().replace(hour=22, minute=30, second=0, microsecond=0)
time_range = pd.date_range(start=start_time, end=end_time, freq="15T")

# Function to generate realistic data
def generate_device_data(device_name, total_packets, total_requests):
    size = len(time_range)
    packets_sent = np.random.randint(10, total_packets // size, size)
    packets_received = packets_sent - np.random.randint(0, 3, size)
    requests_sent = np.random.randint(10, total_requests // size, size)
    requests_received = requests_sent - np.random.randint(0, 2, size)

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

# Wireshark Reports
if selected_tab == "WireShark Reports":
    st.title("Wireshark Reports")
    st.header("Device Data Analysis")

    # Line/Curve Graphs
    st.subheader("Line and Curve Graphs")
    st.line_chart(echo_data[["Packets Sent", "Packets Received"]], height=250)
    st.line_chart(echo_data[["Requests Sent", "Requests Received"]], height=250)

    # Bar Chart of Sent to Received
    st.subheader("Bar Chart: Sent vs. Received")
    bar_data = echo_data[["Packets Sent", "Packets Received"]].sum()
    st.bar_chart(bar_data)

    # Failures for Both Devices
    st.subheader("Failures by Device")
    failure_data = pd.DataFrame({
        "Device": ["Amazon Echo", "Google Nest Doorbell"],
        "Failures": [echo_data["Failures"].sum(), nest_data["Failures"].sum()]
    })
    st.bar_chart(failure_data.set_index("Device"))

# Test Case Reports
elif selected_tab == "Test Case Reports":
    st.title("Test Case Reports")
    st.header("Amazon Echo Packet Timeline Analysis")

    # Filter for Date
    selected_date = st.date_input("Select Date", start_time.date())
    filtered_data = echo_data[echo_data["Time"].dt.date == selected_date]

    # Line Chart for Packets Over Time
    if not filtered_data.empty:
        st.line_chart(filtered_data[["Packets Sent", "Packets Received"]])
    else:
        st.write("No data available for the selected date.")

    st.subheader("Test Cases")
    test_cases = pd.DataFrame({
        "Test Case": [
            "Correct Song Plays",
            "Restriction Block - Request Blocked by User",
            "Echo - No Restrictions",
            "Echo - With Rules Enforced",
            "Data Sharing Across",
            "Suggestion for Contract Rule to Have Uniformity",
            "User Can Apply Smart Contract Rules",
            "Admin Can View and Filter",
            "Admin Creates Subuser",
            "Admin Deletes"
        ],
        "Success Rate %": np.random.choice(range(0, 101, 20), 10)
    })
    st.bar_chart(test_cases.set_index("Test Case"))

# Ledger Report
elif selected_tab == "Ledger Report":
    st.title("Ledger Report")
    st.header("Smart Contract Blocks")

    # Buttons for Ledgers and Sidechains
    sidechains = ["Main Blockchain", "Sidechain 1", "Sidechain 2"]
    for chain in sidechains:
        if st.button(f"View {chain}"):
            st.write(f"Smart contract blocks for {chain} are displayed here.")

# Users and Privileges
elif selected_tab == "Users and Privileges":
    st.title("Users and Privileges")
    st.header("User Policies and Blocks")

    user_privileges = pd.DataFrame({
        "User": ["Stephanie", "Lucy"],
        "Device": ["Amazon Echo", "Google Nest Doorbell"],
        "Policy": ["Site Restriction: iTunes", "Time Restriction: Yoga Time"],
        "Blocked Site/Time": ["iTunes", "3-5 PM"]
    })
    st.table(user_privileges)

# Devices and Policies
elif selected_tab == "Devices and Policies":
    st.title("Devices and Policies")
    st.header("Policy Management")

    policy_data = pd.DataFrame({
        "Device": ["Amazon Echo", "Google Nest Doorbell"],
        "Available Policies": [
            ["No Restriction", "Time Restriction", "Site Restriction", "Time Condition Restriction", "Music Genre Restriction"],
            ["No Restriction", "Time Restriction", "Site Restriction"]
        ]
    })

    # Show Policies
    for index, row in policy_data.iterrows():
        st.write(f"Device: {row['Device']}")
        selected_policy = st.selectbox(f"Apply Policy to {row['Device']}", row["Available Policies"])
        st.write(f"Selected Policy: {selected_policy}")

    # Suggestion Box
    st.text_area("Suggest a New Policy", placeholder="Enter your suggestion here.")

# Device Reports
else:
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
