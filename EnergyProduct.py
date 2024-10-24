import streamlit as st
import pandas as pd
from datetime import datetime
import random
import cloudinary
import cloudinary.uploader
import os
st.markdown(
    """
    <style>
    .st-emotion-cache-1huvf7z {
        display: none; /* Hides the button */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Hide the avatar image
st.markdown(
    """
    <style>
    ._profileImage_1yi6l_74 {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use Streamlit's image function to show the image on the left side
col1, col2 = st.columns([1, 3])  # Create 2 columns with ratios (left narrower than right)

with col1:  # Left column
    st.image("Huawei.jpg", width=80)

cloudinary.config(
    cloud_name="drpkmvcdb",  # Replace with your Cloudinary cloud name
    api_key="421723639371647",        # Replace with your Cloudinary API key
    api_secret="AWpJzomMBrw-5DHNqujft5scUbM"   # Replace with your Cloudinary API secret
)

def upload_to_cloudinary(file_path, public_id):
    try:
        response = cloudinary.uploader.upload(
            file_path,
            resource_type="raw",
            public_id=public_id,
            overwrite=True,  # Allow overwriting
            invalidate=True,  # Invalidate cached versions on CDN
            unique_filename=False,  # Do not generate a unique filename
            use_filename=True  # Use the file's original filename
        )
        return response['secure_url']
    except cloudinary.exceptions.Error as e:
        st.error(f"Cloudinary upload failed: {str(e)}")
        return None

# Function to save results to Excel
def save_results(username, total_attempted, correct_answers, wrong_answers, total_score, time_taken, details):   
    try:
        df = pd.read_excel("quiz_results_EnergyProduct.xlsx")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Username", "Date", "Total Attempted", "Correct Answers", "Wrong Answers", "Total Score", "Time Taken", "Details"])

    new_data = pd.DataFrame([[username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_attempted, correct_answers, wrong_answers, total_score, time_taken, details]],
                            columns=["Username", "Date", "Total Attempted", "Correct Answers", "Wrong Answers", "Total Score", "Time Taken", "Details"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel("quiz_results_EnergyProduct.xlsx", index=False)
       # Upload the file to Cloudinary
    uploaded_url = upload_to_cloudinary("quiz_results_EnergyProduct.xlsx", "quiz_results_EnergyProduct")
    if uploaded_url:
        st.success(f"Quiz results uploaded successfully!")
        # st.markdown(f"Access your file here: [quiz_results.xlsx]({uploaded_url})")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'flattened_questions' not in st.session_state:
    st.session_state.flattened_questions = []
# List of allowed usernames
allowed_usernames = {
"Farrukh.Hussain",
"HIC_ISB_TrainingTeam_01.",
"HIC_ISB_TrainingTeam_02",
"HIC_ISB_TrainingTeam_03",
"HIC_ISB_TrainingTeam_04",
"HIC_ISB_TrainingTeam_05"
    
}
# Define your questions
EP= {
"true_false": [
    {"question": "Delta-Star Connections are Commonly used in Step Up Transformers for Power Distribution.", "answer": "False"},
    {"question": "Star Connection has a neutral point while Delta connection doesn’t have a neutral point.", "answer": "True"},
    {"question": "In P=√3VLILcos(θ), θ represents Power Factor.", "answer": "True"},
    {"question": "Grounding and Earthing are the Same thing.", "answer": "False"},
    {"question": "A Single Phase can be used to run heavy Loads like Industrial Motors on a single Phase Supply.", "answer": "False"},
    {"question": "Telecom towers typically rely on DC power for their operations.", "answer": "True"},
    {"question": "GPRS Stands for Global Positioning Radius System.", "answer": "False"},
    {"question": "Earthing is Primarily used to avoid Shocks.", "answer": "True"},
    {"question": "There are only 2 types of Surge Protection Devices (SPD).", "answer": "False"},
    {"question": "A Diode allows current to flow easily through in one direction but restricts the flow of current in the opposite direction.", "answer": "True"},
    {"question": "PSU is used to convert AC input Voltage into -48 DC voltage.", "answer": "True"},
    {"question": "Once a fuse is blown, it must be replaced with a new one.", "answer": "True"},
    {"question": "A rectifier is an electrical device used to convert direct current (DC) into alternating current (AC).", "answer": "False"},
    {"question": "Batteries in telecom power systems provide backup power during an outage.", "answer": "True"},
    {"question": "Rectifiers convert AC power to DC power in telecom sites.", "answer": "True"},
    {"question": "Solar power systems can be integrated with telecom towers to provide additional power.", "answer": "True"},
    {"question": "Uninterruptible Power Supplies (UPS) are never used in telecom systems.", "answer": "False"},
    {"question": "Telecom towers require grounding to protect equipment from lightning strikes.", "answer": "True"},
    {"question": "Lead-acid batteries are frequently used for backup power in telecom systems.", "answer": "True"},
    {"question": "Overvoltage can cause damage to sensitive telecom equipment.", "answer": "True"},
    {"question": "Backup generators in data centers often run on diesel fuel.", "answer": "True"},
    {"question": "Power distribution units (PDUs) are used to distribute power from the main source to servers.", "answer": "True"},
    {"question": "Yellow/Green Ground Cable can be dismetal in the start of dismentling activity.", "answer": "False"},
    {"question": "Power cable and signal cables can be bind and route together within cabinet.", "answer": "False"},
    {"question": "AC 4 Core cable can be inserted into breaker with O-Lugs at the end of cable.", "answer": "False"},
    {"question": "As per Huawei SOP, CPRI should inter from left side of the cabinet and connect with BBU, when facing the cabinet.", "answer": "True"},
    {"question": "Anti static Wrist should be used once working inside the PowerCube for Cards and Cable connection.", "answer": "True"},
    {"question": "AC 4 Core cable outside the Powercube Cabinet should must be protected with corrugated Pipe.", "answer": "True"},
    {"question": "<0.1 Ohm be the value of ground resistance for PowerCube and other Huawei equipments?", "answer": "True"},
    {"question": "8 Dry output ports are there in UIM02C.", "answer": "True"},
    {"question": "6 Dry contact input ports are there in UIM02C.", "answer": "True"},
    {"question": "Bending radius of power cables, grounding cables and signal cables >Greater than 6 times their diameter.", "answer": "False"},
    {"question": "60mm recommended minimum distance to bind cables of different categories.", "answer": "False"},
    {"question": "52mm to 60mm should be the hole depth for fixing PowerCube(ICC Series).", "answer": "True"},
    {"question": "DC Current of Cable can be Measured with DMM with Clap feature.", "answer": "True"},
    {"question": "Ground test can done with Multi meter.", "answer": "False"},
    {"question": "On Site RJ45 LAN Cable's connector can be made with Diagonal Plier.", "answer": "False"},
    {"question": "Cooling systems consume a large portion of the total power in a data center.", "answer": "True"}
],

    "single_choice": [
     {
        "question": "What is the main function of a rectifier in telecom power systems?",
        "options": ["A) Convert DC to AC", "B) Convert AC to DC", "C) Store energy", "D) Distribute power"],
        "answer": "B) Convert AC to DC"
    },
    {
        "question": "Which type of battery is commonly used for telecom backup power?",
        "options": ["A) Lithium-ion", "B) Nickel-Cadmium", "C) Lead-acid", "D) Alkaline"],
        "answer": "C) Lead-acid"
    },
    {
        "question": "What is the typical output voltage of telecom DC power systems?",
        "options": ["A) 5V", "B) 48V", "C) 220V", "D) 12V"],
        "answer": "B) 48V"
    },
    {
        "question": "What is the purpose of grounding in telecom power systems?",
        "options": ["A) To reduce power consumption", "B) To protect against lightning", "C) To increase efficiency", "D) To provide backup power"],
        "answer": "B) To protect against lightning"
    },
    {
        "question": "Which device is responsible for converting DC power to AC power in telecom systems?",
        "options": ["A) Transformer", "B) Rectifier", "C) Inverter", "D) Capacitor"],
        "answer": "C) Inverter"
    },
    {
        "question": "What is a common renewable energy source used in telecom power systems?",
        "options": ["A) Wind", "B) Hydroelectric", "C) Geothermal", "D) Solar"],
        "answer": "D) Solar"
    },
    {
        "question": "Purpose of a Type 2 SPD?",
        "options": ["A) Protect against Lightning Strike", "B) Protect against overvoltage from electrical network", "C) Provide Grounding for electrical System", "D) To filter out electromagnetic interference"],
        "answer": "B) Protect against overvoltage from electrical network"
    },
    {
        "question": "Purpose of Grounding in electrical System:",
        "options": ["A) Improve Energy efficiency", "B) Prevent Electric Shock and ensure safety", "C) Increase Voltage of System", "D) For better Transmission Speed"],
        "answer": "B) Prevent Electric Shock and ensure safety"
    },
    {
        "question": "Voltage of Single Phase Supply is",
        "options": ["A) 215V", "B) 230V", "C) 415V", "D) 430V"],
        "answer": "B) 230V"
    },
    {
        "question": "Star Connections is used when",
        "options": ["A) Neutral and 2 separate voltages are Needed", "B) Neutral and 3 separate voltages are Needed", "C) Only 2 Separate Voltages are needed", "D) None of the above"],
        "answer": "A) Neutral and 2 separate voltages are Needed"
    },
    {
        "question": "What is the role of a Power Distribution Unit (PDU) in telecom towers?",
        "options": ["A) Store energy", "B) Distribute power", "C) Regulate voltage", "D) Convert DC to AC"],
        "answer": "B) Distribute power"
    },
    {
        "question": "Which of the following is NOT a component of telecom power systems?",
        "options": ["A) Rectifier", "B) Transformer", "C) Battery", "D) Firewall"],
        "answer": "D) Firewall"
    },
    {
        "question": "In hybrid telecom power systems, which of the following is used alongside solar power?",
        "options": ["A) Capacitor", "B) Generator", "C) Inverter", "D) Resistor"],
        "answer": "B) Generator"
    },
    {
        "question": "What does the abbreviation 'UPS' stand for?",
        "options": ["A) Universal Power Supply", "B) Uninterrupted Power Supply", "C) Uninterrupted Power Source", "D) Utility Power System"],
        "answer": "B) Uninterrupted Power Supply"
    },
    {
        "question": "What is the main function of UPS in data centers?",
        "options": ["A) Provide long-term power storage", "B) Provide short-term power during an outage", "C) Convert AC to DC", "D) Distribute power to servers"],
        "answer": "B) Provide short-term power during an outage"
    },
    {
        "question": "What is the purpose of Power Usage Effectiveness (PUE) in a data center?",
        "options": ["A) Measure energy efficiency", "B) Manage cooling systems", "C) Improve network performance", "D) Ensure data security"],
        "answer": "A) Measure energy efficiency"
    },
    {
        "question": "Which of the following power distribution methods is commonly used in data centers?",
        "options": ["A) Radial", "B) Ring", "C) Mesh", "D) Grid"],
        "answer": "A) Radial"
    },
    {
        "question": "What is a common source of power redundancy in data centers?",
        "options": ["A) Multiple PDUs", "B) Battery banks", "C) Dual power feeds", "D) Cooling systems"],
        "answer": "C) Dual power feeds"
    },
    {
        "question": "What is the primary function of a Power Distribution Unit (PDU) in a data center?",
        "options": ["A) Backup power", "B) Cooling", "C) Distribute power", "D) Manage network traffic"],
        "answer": "C) Distribute power"
    },
    {
        "question": "Which type of power is commonly used to operate servers in data centers?",
        "options": ["A) AC", "B) DC", "C) Solar", "D) Wind"],
        "answer": "A) AC"
    },
    {
        "question": "What is the typical voltage used for power distribution to servers in data centers?",
        "options": ["A) 120V", "B) 220V", "C) 48V", "D) 400V"],
        "answer": "B) 220V"
    },
    {
        "question": "Which of the following is a power efficiency metric used in data centers?",
        "options": ["A) RPM", "B) PUE", "C) MVA", "D) UPS"],
        "answer": "B) PUE"
    },
    {
        "question": "What is a common cooling solution for data centers?",
        "options": ["A) Liquid immersion cooling", "B) Air-cooled radiators", "C) Fans", "D) Heat sinks"],
        "answer": "A) Liquid immersion cooling"
    },
    {
        "question": "Which of the following is a common fuel source for data center backup generators?",
        "options": ["A) Natural Gas", "B) Coal", "C) Diesel", "D) Wind"],
        "answer": "C) Diesel"
    },
    {
        "question": "RRU are situated at",
        "options": ["A) Near the Antenna", "B) Foot of the tower", "C) In BTS cabinet", "D) Near Generator"],
        "answer": "A) Near the Antenna"
    },
    {
        "question": "Grounding BUS Bar is available on Tower, where should be the RRU Grounded?",
        "options": ["A) Tower Leg", "B) Grounding BUS Bar", "C) Grounding is not required", "D) Ground later"],
        "answer": "A) Tower Leg"
    },
    {
        "question": "Packing of Rectifier and Batteries should be removed when Equipment is on-------?",
        "options": ["A) On Site", "B) WH", "C) Outside WH", "D) Supplier WH"],
        "answer": "A) On Site"
    },
    {
        "question": "Batteries within the Power should be proper spacing on----mm?",
        "options": ["A) 10mm", "B) 5mm", "C) 15mm", "D) 20mm"],
        "answer": "A) 10mm"
    },
    {
        "question": "Batteries can be transported to site in -----packing?",
        "options": ["A) Wooden Packing", "B) Polythen packing", "C) No Packing", "D) Any Packing"],
        "answer": "A) Wooden Packing"
    },
    {
        "question": "What is the Name of Controller used in ICC710?",
        "options": ["A) SMU01B", "B) SMU03A", "C) SMU02B", "D) UIMC01"],
        "answer": "C) SMU02B"
    },
    {
        "question": "Where to patch AC SPD alarm in ICC710 (     )?",
        "options": ["A) DIN6", "B) DIN4", "C) DIN8", "D) DIN3"],
        "answer": "A) DIN6"
    },
    {
        "question": "What is the login Browser IP of Power Cube 1CC710-ICC500 (     )?",
        "options": ["A) 192.168.10.1", "B) 192.168.0.10", "C) 192.168.1.1", "D) 192.168.10.1"],
        "answer": "B) 192.168.0.10"
    },
    {
        "question": "Which module is used to convert AC input voltage into -48V DC voltage?",
        "options": ["A) BBU", "B) SPLU", "C) PSU", "D) RFU"],
        "answer": "C) PSU"
    },
    {
        "question": "When On Site status is 'COM NOK', which tool can be used to confirm Ping from Site to NetEco?",
        "options": ["A) Putty", "B) FileZilla", "C) Lan Tester", "D) Web Browser"],
        "answer": "A) Putty"
    },
    {
        "question": "For tightening Battery Terminal and Rawal Bolts how much N.M for Torque Wrench Torque Required?",
        "options": ["A) 17N.m & 46 N.m", "B) 17N.m & 45 N.m", "C) 40 N.M & 70 N.M", "D) 40 N.m & 60 N.m"],
        "answer": "B) 17N.m & 45 N.m"
    }

        
    ],
    "multiple_choice": [
       {
        "question": "The Network Communication Modes include (   ).",
        "options": [
            "A) Simplex",
            "B) Half Duplex",
            "C) Full Duplex",
            "D) Microwave",
            "E) Simplex+Half Duplex+Full Duplex"
        ],
        "answer": ["A) Simplex", "B) Half Duplex", "C) Full Duplex"]
    },
    {
        "question": "OSI Model Network Layers Include (   ).",
        "options": [
            "A) Transport Layer",
            "B) Control Layer",
            "C) Physical Layer",
            "D) Protocol Layer",
            "E) Transport Layer + Physical Layer"
        ],
        "answer": ["A) Transport Layer", "C) Physical Layer"]
    },
    {
        "question": "Types of Diode Include (   ).",
        "options": [
            "A) Laser Diode",
            "B) Zener Diode",
            "C) Light Emitting Diode",
            "D) PN junction Diode",
            "E) Laser Diode+Zener Diode+Light Emitting Diode"
        ],
        "answer": ["A) Laser Diode", "B) Zener Diode", "C) Light Emitting Diode"]
    },
    {
        "question": "Lithium battery: ESM-48100A6 can be used for cabinets (   ).",
        "options": [
            "A) ICC330-HA1-C11",
            "B) ICC330-HD1-C6",
            "C) ICC360-HA1-C2",
            "D) ICC800-A1-C2",
            "E) ICC330-HA1-C11 + ICC360-HA1-C2 + ICC330-HD1-C6 + ICC800-A1-C2"
        ],
        "answer": ["A) ICC330-HA1-C11", "B) ICC330-HD1-C6", "C) ICC360-HA1-C2", "D) ICC800-A1-C2"]
    },
    {
        "question": "Lithium Ion Cells are used in applications like (   ).",
        "options": [
            "A) Smartphones",
            "B) Medical devices",
            "C) Power tools",
            "D) Vehicles",
            "E) Smartphone+Medical devices+Power tools"
        ],
        "answer": ["A) Smartphones", "B) Medical devices", "C) Power tools"]
    },
    {
        "question": "The Major types of UPS system configurations are (   ).",
        "options": [
            "A) Online double conversion",
            "B) Battery back up",
            "C) Line interactive",
            "D) Single Conversion",
            "E) Online double conversion+Battery back up+Line interactive"
        ],
        "answer": ["A) Online double conversion", "B) Battery back up", "C) Line interactive"]
    },
    {
        "question": "Which of the following components are typically used in telecom power systems? (   ).",
        "options": [
            "A) Rectifier",
            "B) Inverter",
            "C) Battery",
            "D) Firewall",
            "E) Rectifier+Inverter+Battery"
        ],
        "answer": ["A) Rectifier", "B) Inverter", "C) Battery"]
    },
    {
        "question": "What Sensors does a cabinet contain (   ).",
        "options": [
            "A) Smoke",
            "B) Water",
            "C) Dust",
            "D) GPS",
            "E) Smoke+Dust+Water+GPS"
        ],
        "answer": ["A) Smoke", "B) Water", "C) Dust", "D) GPS"]
    },
    {
        "question": "What are the benefits of using DC power in telecom systems (   ).",
        "options": [
            "A) Lower energy losses",
            "B) Higher efficiency",
            "C) Simple power conversion",
            "D) Higher voltage",
            "E) Lower energy losses+Higher efficiency+Simple power conversion"
        ],
        "answer": ["A) Lower energy losses", "B) Higher efficiency", "C) Simple power conversion"]
    },
    {
        "question": "Which of the following are power sources for telecom towers? (   ).",
        "options": [
            "A) Diesel generators",
            "B) Solar panels",
            "C) Wind turbines",
            "D) Battery banks",
            "E) Diesel generators+Solar panels+Wind turbines+Battery banks"
        ],
        "answer": ["A) Diesel generators", "B) Solar panels", "C) Wind turbines"]
    },
    {
        "question": "Telecom backup power systems typically include (   ).",
        "options": [
            "A) Generators",
            "B) Rectifiers",
            "C) Batteries",
            "D) PDUs",
            "E) Generators+Rectifiers+Batteries"
        ],
        "answer": ["A) Generators", "B) Rectifiers", "C) Batteries"]
    },
    {
        "question": "Hybrid telecom power systems may use (   ).",
        "options": [
            "A) Solar power",
            "B) Wind power",
            "C) Diesel generators",
            "D) UPS systems",
            "E) Solar power+Wind power+Diesel generators+UPS systems"
        ],
        "answer": ["A) Solar power", "B) Wind power", "C) Diesel generators"]
    },
    {
        "question": "Data Center Power Scenario (   ).",
        "options": [
            "A) UPS systems",
            "B) Power Distribution Units (PDUs)",
            "C) Cooling systems",
            "D) Network switches",
            "E) UPS systems+Power Distribution Units (PDUs)+Cooling systems"
        ],
        "answer": ["A) UPS systems", "B) Power Distribution Units (PDUs)", "C) Cooling systems"]
    },
    {
        "question": "Which of the following are used to ensure power redundancy in data centers? (   ).",
        "options": [
            "A) Backup generators",
            "B) Multiple UPS systems",
            "C) Dual power supplies",
            "D) Battery banks",
            "E) Backup generators+Multiple UPS systems+Dual power supplies+Battery banks"
        ],
        "answer": ["A) Backup generators", "B) Multiple UPS systems", "C) Dual power supplies"]
    },
    {
        "question": "Power usage in a data center can be optimized by (   ).",
        "options": [
            "A) Using high-efficiency PDUs",
            "B) Reducing cooling power consumption",
            "C) Implementing power monitoring",
            "D) Increasing server density",
            "E) Using high-efficiency PDUs+Reducing cooling power consumption+Implementing power monitoring"
        ],
        "answer": ["A) Using high-efficiency PDUs", "B) Reducing cooling power consumption", "C) Implementing power monitoring"]
    },
    {
        "question": "Which of the following metrics are used to measure data center power efficiency? (   ).",
        "options": [
            "A) PUE (Power Usage Effectiveness)",
            "B) UPS runtime",
            "C) Load balancing",
            "D) Cooling energy efficiency",
            "E) PUE (Power Usage Effectiveness)"
        ],
        "answer": ["A) PUE (Power Usage Effectiveness)"]
    },
    {
        "question": "Data center power management includes (   ).",
        "options": [
            "A) Load distribution",
            "B) Energy efficiency monitoring",
            "C) Generator maintenance",
            "D) Heat dissipation management",
            "E) Load distribution+Energy efficiency monitoring+Generator maintenance"
        ],
        "answer": ["A) Load distribution", "B) Energy efficiency monitoring", "C) Generator maintenance"]
    },
    {
        "question": "Which of the following are common voltage levels used in telecom power systems (   ).",
        "options": [
            "A) 24V",
            "B) 48V",
            "C) 110V",
            "D) 220V",
            "E) 24V+48V+110V"
        ],
        "answer": ["A) 24V", "B) 48V", "C) 110V"]
    },
    {
        "question": "Which components are essential for converting AC to DC in telecom systems (   ).",
        "options": [
            "A) Rectifier",
            "B) Transformer",
            "C) Inverter",
            "D) UPS",
            "E) Rectifier"
        ],
        "answer": ["A) Rectifier"]
    },
    {
        "question": "What types of batteries are commonly used in telecom power systems (   ).",
        "options": [
            "A) Lead-acid",
            "B) Lithium-ion",
            "C) Nickel-Cadmium",
            "D) Alkaline",
            "E) Lead-acid+Lithium-ion+Nickel-Cadmium"
        ],
        "answer": ["A) Lead-acid", "B) Lithium-ion", "C) Nickel-Cadmium"]
    },
    {
        "question": "Which of the following are benefits of using DC power in telecom networks (   ).",
        "options": [
            "A) Lower energy losses",
            "B) Simpler design",
            "C) Reduced cooling needs",
            "D) Enhanced signal quality",
            "E) Lower energy losses+Simpler design"
        ],
        "answer": ["A) Lower energy losses", "B) Simpler design"]
    },
    {
        "question": "What types of backup power sources can be found in telecom sites (   ).",
        "options": [
            "A) Batteries",
            "B) Solar panels",
            "C) Diesel generators",
            "D) Fuel cells",
            "E) Batteries+Solar panels+Diesel generators"
        ],
        "answer": ["A) Batteries", "B) Solar panels", "C) Diesel generators"]
    },
    {
        "question": "Which of the following devices are used to protect telecom equipment from voltage spikes (   ).",
        "options": [
            "A) Circuit Breaker",
            "B) SPD (Surge Protection Device)",
            "C) Transformer",
            "D) Inverter",
            "E) SPD (Surge Protection Device)"
        ],
        "answer": ["B) SPD (Surge Protection Device)"]
    },
    {
        "question": "Which renewable energy sources are integrated into telecom power systems (   ).",
        "options": [
            "A) Wind power",
            "B) Solar power",
            "C) Hydroelectric power",
            "D) Geothermal power",
            "E) Wind power+Solar power"
        ],
        "answer": ["A) Wind power", "B) Solar power"]
    },
    {
        "question": "Which components can be found in a telecom power distribution unit (   ).",
        "options": [
            "A) Circuit breakers",
            "B) Meters",
            "C) UPS",
            "D) Transformers",
            "E) Circuit breakers+Meters+Transformers"
        ],
        "answer": ["A) Circuit breakers", "B) Meters", "D) Transformers"]
    },
    {
        "question": "What are the main functions of a Battery Management System (BMS) (   ).",
        "options": [
            "A) Monitor battery health",
            "B) Regulate voltage",
            "C) Optimize charging",
            "D) Distribute power",
            "E) Monitor battery health+Regulate voltage+Optimize charging"
        ],
        "answer": ["A) Monitor battery health", "B) Regulate voltage", "C) Optimize charging"]
    },
    {
        "question": "Which of the following issues can affect telecom power systems (   ).",
        "options": [
            "A) Overvoltage",
            "B) Under-voltage",
            "C) Power surges",
            "D) Network congestion",
            "E) Overvoltage+Under-voltage+Power surges"
        ],
        "answer": ["A) Overvoltage", "B) Under-voltage", "C) Power surges"]
    },
    {
        "question": "Which types of energy sources are increasingly being used in hybrid telecom power systems (   ).",
        "options": [
            "A) Diesel generators",
            "B) Solar panels",
            "C) Wind turbines",
            "D) Biomass",
            "E) Solar panels+Wind turbines"
        ],
        "answer": ["B) Solar panels", "C) Wind turbines"]
    },
    {
        "question": "What are the advantages of using a UPS in telecom applications (   ).",
        "options": [
            "A) Provides immediate backup",
            "B) Stabilizes voltage",
            "C) Reduces energy costs",
            "D) Increases system complexity",
            "E) Provides immediate backup+Stabilizes voltage"
        ],
        "answer": ["A) Provides immediate backup", "B) Stabilizes voltage"]
    },
    {
        "question": "Which components are commonly used for voltage regulation in telecom systems (   ).",
        "options": [
            "A) Voltage regulators",
            "B) Transformers",
            "C) Capacitors",
            "D) Inductors",
            "E) Voltage regulators+Transformers"
        ],
        "answer": ["A) Voltage regulators", "B) Transformers"]
    },
    {
        "question": "What are common maintenance practices for telecom power systems (   ).",
        "options": [
            "A) Regular battery checks",
            "B) Inspection of power distribution",
            "C) Cleaning of solar panels",
            "D) Software updates",
            "E) Regular battery checks+Inspection of power distribution+Cleaning of solar panels"
        ],
        "answer": ["A) Regular battery checks", "B) Inspection of power distribution", "C) Cleaning of solar panels"]
    },
    {
        "question": "Which safety measures are critical in telecom power installations (   ).",
        "options": [
            "A) Proper grounding",
            "B) Use of fuses",
            "C) Circuit breakers",
            "D) Fire suppression systems",
            "E) Proper grounding+Use of fuses+Circuit breakers"
        ],
        "answer": ["A) Proper grounding", "B) Use of fuses", "C) Circuit breakers"]
    },
    {
        "question": "What are the key components of a solar power system used in telecom (   ).",
        "options": [
            "A) Solar panels",
            "B) Inverters",
            "C) Battery storage",
            "D) Charge controllers",
            "E) Solar panels+Inverters+Battery storage"
        ],
        "answer": ["A) Solar panels", "B) Inverters", "C) Battery storage"]
    },
    {
        "question": "Which of the following are indicators of good power quality in telecom systems (   ).",
        "options": [
            "A) Low total harmonic distortion (THD)",
            "B) Stable voltage levels",
            "C) Minimal power interruptions",
            "D) High energy consumption",
            "E) Low total harmonic distortion (THD)+Stable voltage levels+Minimal power interruptions"
        ],
        "answer": ["A) Low total harmonic distortion (THD)", "B) Stable voltage levels", "C) Minimal power interruptions"]
    },
    {
        "question": "What types of communication networks commonly use DC power (   ).",
        "options": [
            "A) Mobile networks",
            "B) Fiber optic networks",
            "C) Fixed-line networks",
            "D) Satellite networks",
            "E) Mobile networks+Fixed-line networks"
        ],
        "answer": ["A) Mobile networks", "C) Fixed-line networks"]
    },
    {
        "question": "Which types of electrical connections are used in telecom power systems (   ).",
        "options": [
            "A) Star connection",
            "B) Delta connection",
            "C) Series connection",
            "D) Parallel connection",
            "E) Star connection+Delta connection+Parallel connection"
        ],
        "answer": ["A) Star connection", "B) Delta connection", "D) Parallel connection"]
    },
    {
        "question": "What are typical energy-saving technologies used in telecom systems (   ).",
        "options": [
            "A) Energy-efficient batteries",
            "B) Power factor correction devices",
            "C) Smart grids",
            "D) High-voltage transmission lines",
            "E) Energy-efficient batteries+Power factor correction devices+Smart grids"
        ],
        "answer": ["A) Energy-efficient batteries", "B) Power factor correction devices"]
    },
    {
        "question": "Which of the following are common types of UPS systems used in data centers (   ).",
        "options": [
            "A) Offline UPS",
            "B) Line-interactive UPS",
            "C) Online UPS",
            "D) Hybrid UPS",
            "E) Offline UPS+Line-interactive UPS+Online UPS"
        ],
        "answer": ["A) Offline UPS", "B) Line-interactive UPS", "C) Online UPS"]
    },
    {
        "question": "What are the typical cooling methods employed in data centers (   ).",
        "options": [
            "A) Air cooling",
            "B) Liquid cooling",
            "C) Evaporative cooling",
            "D) Solar cooling",
            "E) Air cooling+Liquid cooling+Evaporative cooling"
        ],
        "answer": ["A) Air cooling", "B) Liquid cooling", "C) Evaporative cooling"]
    },
    {
        "question": "Which power metrics are commonly used to assess data center efficiency (   ).",
        "options": [
            "A) PUE (Power Usage Effectiveness)",
            "B) DCiE (Data Center Infrastructure Efficiency)",
            "C) TCO (Total Cost of Ownership)",
            "D) CAPEX (Capital Expenditure)",
            "E) PUE (Power Usage Effectiveness)+DCiE (Data Center Infrastructure Efficiency)"
        ],
        "answer": ["A) PUE (Power Usage Effectiveness)", "B) DCiE (Data Center Infrastructure Efficiency)"]
    },
    {
        "question": "What types of energy sources can be integrated into data centers (   ).",
        "options": [
            "A) Diesel generators",
            "B) Natural gas",
            "C) Solar panels",
            "D) Wind turbines",
            "E) Diesel generators+Solar panels+Wind turbines"
        ],
        "answer": ["A) Diesel generators", "C) Solar panels", "D) Wind turbines"]
    },
    {
        "question": "Which of the following devices can be used for power monitoring in data centers (   ).",
        "options": [
            "A) Smart PDUs",
            "B) Energy meters",
            "C) Circuit breakers",
            "D) Transformers",
            "E) Smart PDUs+Energy meters"
        ],
        "answer": ["A) Smart PDUs", "B) Energy meters"]
    },
    {
        "question": "What factors can impact the reliability of power systems in data centers (   ).",
        "options": [
            "A) Redundant power supplies",
            "B) UPS configuration",
            "C) Cooling efficiency",
            "D) Power distribution architecture",
            "E) Redundant power supplies+UPS configuration"
        ],
        "answer": ["A) Redundant power supplies", "B) UPS configuration", "D) Power distribution architecture"]
    },
    {
        "question": "Which components are typically included in a data center power distribution system (   ).",
        "options": [
            "A) Transformers",
            "B) Circuit breakers",
            "C) PDUs",
            "D) Servers",
            "E) Transformers+Circuit breakers+PDUs"
        ],
        "answer": ["A) Transformers", "B) Circuit breakers", "C) PDUs"]
    },
    {
        "question": "What strategies can be employed to reduce energy consumption in data centers (   ).",
        "options": [
            "A) Efficient cooling systems",
            "B) Virtualization of servers",
            "C) Energy-efficient lighting",
            "D) Increased server count",
            "E) Efficient cooling systems+Virtualization of servers+Energy-efficient lighting"
        ],
        "answer": ["A) Efficient cooling systems", "B) Virtualization of servers", "C) Energy-efficient lighting"]
    },
    {
        "question": "Which factors should be considered when selecting a UPS for a data center (   ).",
        "options": [
            "A) Load capacity",
            "B) Runtime requirements",
            "C) Battery technology",
            "D) Cost",
            "E) Load capacity+Runtime requirements+Battery technology"
        ],
        "answer": ["A) Load capacity", "B) Runtime requirements", "C) Battery technology"]
    },
    {
        "question": "What is the purpose of redundancy in data center power systems (   ).",
        "options": [
            "A) Improve performance",
            "B) Ensure continuous operation during failures",
            "C) Reduce costs",
            "D) Increase cooling efficiency",
            "E) Ensure continuous operation during failures"
        ],
        "answer": ["B) Ensure continuous operation during failures"]
    },
    {
        "question": "What are some common causes of power interruptions in data centers (   ).",
        "options": [
            "A) Weather conditions",
            "B) Utility outages",
            "C) Equipment failures",
            "D) Maintenance activities",
            "E) Weather conditions+Utility outages+Equipment failures+Maintenance activities"
        ],
        "answer": ["A) Weather conditions", "B) Utility outages", "C) Equipment failures"]
    },
    {
        "question": "There should be ---- engineers from Suppliers for any major activity includes Huawei (   ).",
        "options": [
            "A) 2 Subon +1 Huawei",
            "B) 2 Subon +2 Huawei",
            "C) 1 Subon +0 Huawei",
            "D) 1 Subon +1 Huawei",
            "E) 2 Subon +1 Huawei & 1 Subcon + 1 Huawei"
        ],
        "answer": ["A) 2 Subon +1 Huawei", "E) 2 Subon +1 Huawei & 1 Subcon + 1 Huawei"]
    },
    {
        "question": "Core Site Activity which prerequisites Required in Core Room implemented by customer (   ).",
        "options": [
            "A) Proper EHS + Insulated Tools",
            "B) No EHS + Proper Tools",
            "C) Customer Regulations Follow",
            "D) No Need any Rules",
            "E) Proper EHS + Insulated Tools & Customer Regulations Follow"
        ],
        "answer": ["A) Proper EHS + Insulated Tools", "E) Proper EHS + Insulated Tools & Customer Regulations Follow"]
    },
    {
        "question": "BBU and RRU should be connected to which type of breakers (   ).",
        "options": [
            "A) 63 Amps LLVD",
            "B) 63 Amps BLVD",
            "C) 32Amps LLVD",
            "D) 32Amps BLVD",
            "E) 63 Amps LLVD & 32Amps BLVD"
        ],
        "answer": ["A) 63 Amps LLVD", "E) 63 Amps LLVD & 32Amps BLVD"]
    },
    {
        "question": "During Battery Installation, AC Power Should be Switched ---- while Battery Breaker should be switched---- (   ).",
        "options": [
            "A) ON/ON",
            "B) OFF/OFF",
            "C) ON/OFF",
            "D) OFF/ON",
            "E) OFF/OFF"
        ],
        "answer": ["B) OFF/OFF"]
    },
    {
        "question": "ICC710 can be used with following batteries back up (   ).",
        "options": [
            "A) ACB",
            "B) FCB",
            "C) TCB",
            "D) Narada",
            "E) ACB, FCB, TCB"
        ],
        "answer": ["E) ACB, FCB, TCB"]
    },
    {
        "question": "On Site SMU NetEco Port and UPEU/UEIU Card ports name are (   ).",
        "options": [
            "A) FE & ALM",
            "B) MON1 & RS485/232",
            "C) MON0 & RS485/232",
            "D) MON0 & FE",
            "E) MON1 & RS485/232 + MON0 & RS485/232"
        ],
        "answer": ["E) MON1 & RS485/232 + MON0 & RS485/232"]
    },
    {
        "question": "On Site LAN Cable's can be made with which Tools and Tested with which Meter (   ).",
        "options": [
            "A) Digonal Plier",
            "B) Cripping tool",
            "C) LAN Cable Tester",
            "D) DMM",
            "E) Cripping tool & LAN Cable Tester"
        ],
        "answer": ["E) Cripping tool & LAN Cable Tester"]
    },
    {
        "question": "240mm2 DC Cable Thimble can be made with-----and straight with------- (   ).",
        "options": [
            "A) Nose Plier",
            "B) Thimble Presser",
            "C) Hammer",
            "D) Screw Driver",
            "E) Thimble presser and Hammer"
        ],
        "answer": ["B) Thimble Presser", "C) Hammer"]
    }
    ]
}
# Flatten questions for navigation
if not st.session_state.flattened_questions:
    flattened_questions = []

    for category, qs in EP.items():
        for q in qs:
            q['type'] = category  # Set the type for each question
            flattened_questions.append(q)

    # Shuffle questions within each type
    random.shuffle(flattened_questions)

    true_false_questions = [q for q in flattened_questions if q['type'] == 'true_false']
    single_choice_questions = [q for q in flattened_questions if q['type'] == 'single_choice']
    mcq_questions = [q for q in flattened_questions if q['type'] == 'multiple_choice']

    # Combine the questions in the desired order
    all_questions = (
    true_false_questions[:15] + 
    single_choice_questions[:15] + 
    mcq_questions[:10]
)

    # Limit to the first 20 questions
    st.session_state.flattened_questions = all_questions[:40]

# Initialize answers
if len(st.session_state.answers) != len(st.session_state.flattened_questions):
    st.session_state.answers = [None] * len(st.session_state.flattened_questions)


# Login form
if not st.session_state.logged_in:
    st.header("Welcome to Huawei Quiz Portal")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")  # You might want to handle password validation separately

    if st.button("Login"):
        if username in allowed_usernames and password:  # Add password validation as needed
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.start_time = datetime.now()  # Track start time on login
            st.success("Logged in successfully!")
            st.session_state.logged_in = True
            st.experimental_set_query_params()  # Ensures the state is saved and reloaded without rerunning the entire script
              
        else:
            st.error("Please enter a valid username and password.")
else:
    st.sidebar.markdown(f"## Welcome **{st.session_state.username}** For The Quiz Of Energy Product ")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_question = 0  # Reset current question
        st.session_state.answers = [None] * len(st.session_state.flattened_questions)  # Reset answers
        st.session_state.username = ""
        st.session_state.quiz_submitted = False  # Reset quiz submission status
        st.session_state.flattened_questions = []  # Reset questions
        st.success("You have been logged out.")
        # st.experimental_rerun()  # Refresh the page to reflect the new state

    # Quiz Page
    st.header(f"Welcome {st.session_state.username} For The Quiz Of Energy Product")
    
    # Navigation buttons
    col1, col2 = st.columns(2)

    # Only show navigation buttons if the quiz hasn't been submitted
    if not st.session_state.quiz_submitted:
        if st.session_state.current_question > 0:
            with col1:
                if st.button("Previous", key="prev"):
                    st.session_state.current_question -= 1

    if st.session_state.current_question < len(st.session_state.flattened_questions) - 1:  # Show "Next" button if not on the last question
        with col2:
            if st.button("Next", key="next"):
                st.session_state.current_question += 1

    if st.session_state.current_question == len(st.session_state.flattened_questions) - 1 and not st.session_state.quiz_submitted:
        if st.button("Submit", key="submit"):
            if not st.session_state.quiz_submitted:  # Only process if not already submitted
                total_score = 0
                questions_attempted = 0
                correct_answers = 0
                wrong_answers = 0
                result_details = []

                for idx, question_detail in enumerate(st.session_state.flattened_questions):
                    user_answer = st.session_state.answers[idx]
                    if user_answer is not None:
                        questions_attempted += 1
                        
                        if question_detail["type"] == "true_false":
                            
                            score = 2
                            if user_answer == question_detail["answer"]:
                                correct_answers += 1
                                total_score += score
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Correct"))
                            else:
                                wrong_answers += 1
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Wrong"))
                        elif question_detail["type"] == "single_choice":
                            score = 2
                            if sorted(user_answer) == sorted(question_detail["answer"]):
                                correct_answers += 1
                                total_score += score
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Correct"))
                            else:
                                wrong_answers += 1
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Wrong"))
                        elif question_detail["type"] == "multiple_choice":
                            score = 4
                            if user_answer == question_detail["answer"]:
                                correct_answers += 1
                                total_score += score
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Correct"))
                            else:
                                wrong_answers += 1
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Wrong"))

                end_time = datetime.now()
                time_taken = end_time - st.session_state.start_time
                
                save_results(st.session_state.username, questions_attempted, correct_answers, wrong_answers, total_score, str(time_taken), str(result_details))
                st.success("Quiz submitted successfully!")
                st.session_state.quiz_submitted = True

                total_marks = 100  # Total marks for the quiz
                percentage = (total_score / total_marks) * 100
                result_message = "<h1 style='color: green;'>Congratulations! You passed the Test!</h1>" if percentage >= 70 else "<h1 style='color: red;'>Sorry You Have Failed The Test!.</h1>"

                # Display results in a card
                st.markdown("<div class='card'><h3>Quiz Results</h3>", unsafe_allow_html=True)
                st.markdown(result_message, unsafe_allow_html=True)
                st.write(f"**Total Questions Attempted:** {questions_attempted}")
                st.write(f"**Correct Answers:** {correct_answers}")
                st.write(f"**Wrong Answers:** {wrong_answers}")
                st.write(f"**Total Score:** {total_score}")
                st.write(f"**Percentage:** {percentage:.2f}%")
                st.markdown("</div>", unsafe_allow_html=True)

    # CSS for enhanced design
    st.markdown("""<style>
        .card {
            background-color: #ffcccc; /* Light background */
            border: 1px solid #ddd; /* Subtle border */
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .question-card {
            background-color: #ffcccc; /* Light red color for questions */
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
    </style>""", unsafe_allow_html=True)

    # Display current question if quiz is not submitted
    if not st.session_state.quiz_submitted and st.session_state.current_question < len(st.session_state.flattened_questions):
        current_question = st.session_state.flattened_questions[st.session_state.current_question]
        total_questions = 40
        question_number = st.session_state.current_question + 1 
        progress_percentage = question_number / total_questions
        st.write(f"**Question {question_number} of {total_questions}**")  # Question count
        st.progress(progress_percentage)
        
        st.markdown(f"<div class='question-card'><h4>Question {question_number}: {current_question['question']}</h4></div>", unsafe_allow_html=True)

        # Display options based on question type
        if current_question["type"] == "multiple_choice":
            st.header('Multiple Choice Questions')
            st.session_state.answers[st.session_state.current_question] =  st.multiselect("Choose Multiple Choice option:", current_question["options"], key=f"mc_{st.session_state.current_question}")
        elif current_question["type"] == "true_false":
            st.header('True False')
         
            st.session_state.answers[st.session_state.current_question] =st.radio("Choose an  option:", ["True", "False"], key=f"tf_{st.session_state.current_question}")
        elif current_question["type"] == "single_choice":
            st.header('Single Choice Questions')
           
            st.session_state.answers[st.session_state.current_question] =st.radio("Choose Single Choice options:", current_question["options"], key=f"cc_{st.session_state.current_question}")

# Add a footer
st.markdown("<footer style='text-align: center; margin-top: 20px;'>© 2024 Huawei Training Portal. All Rights Reserved.</footer>", unsafe_allow_html=True)
