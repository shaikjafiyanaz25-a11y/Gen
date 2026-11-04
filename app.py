
import streamlit as st
import datetime
import os
import pandas as pd

from dotenv import load_dotenv

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

from langchain_community.vectorstores import FAISS

from database import (
    add_appointment,
    get_appointments,
    appointment_exists,
    get_booked_times,
    cancel_appointment
)


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CarePlus Hospital",
    page_icon="🏥",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "sidebar_navigation" not in st.session_state:
    st.session_state.sidebar_navigation = "🏠 Home"


# =========================================================
# NAVIGATION CALLBACK
# =========================================================

def navigate_to(page_name):

    st.session_state.sidebar_navigation = page_name


# =========================================================
# ADMIN LOGIN FUNCTION
# =========================================================

def admin_login():

    st.title("🔐 CarePlus Hospital Admin Login")

    st.write(
        "Please login to access the Admin Dashboard."
    )

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        username = st.text_input(
            "👤 Username",
            placeholder="Enter admin username"
        )

        password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter admin password"
        )

        if st.button(
            "🔓 Login",
            use_container_width=True
        ):

            if (
                ADMIN_USERNAME
                and ADMIN_PASSWORD
                and username == ADMIN_USERNAME
                and password == ADMIN_PASSWORD
            ):

                st.session_state.admin_logged_in = True

                st.success(
                    "Login successful!"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password."
                )


# =========================================================
# RAG SETUP
# =========================================================

@st.cache_resource
def load_vectorstore():

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    vectorstore = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


@st.cache_resource
def load_llm():

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )

    return llm


vectorstore = load_vectorstore()

llm = load_llm()


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

pages = [

    "🏠 Home",

    "🤖 Hospital FAQ",

    "👨‍⚕️ Doctors & Departments",

    "📅 Appointment Booking",

    "📋 My Appointments",

    "🔐 Admin Login",

    "📚 Sources"

]

page = st.sidebar.radio(
    "Navigation",
    pages,
    key="sidebar_navigation"
)


# =========================================================
# HOME PAGE
# =========================================================

if page == "🏠 Home":

    st.title(
        "🏥 CarePlus Multispeciality Hospital"
    )

    st.subheader(
        "Welcome to CarePlus Hospital"
    )

    st.write(
        "CarePlus Hospital is a fictional demonstration hospital "
        "application providing hospital information, FAQ assistance "
        "and appointment management."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    # -----------------------------------------------------
    # HOSPITAL FAQ CARD
    # -----------------------------------------------------

    with col1:

        st.info(
            "🤖 **Hospital FAQ**"
        )

        st.write(
            "Ask questions about hospital services."
        )

        st.button(
            "Open Hospital FAQ →",
            key="home_faq",
            use_container_width=True,
            on_click=navigate_to,
            args=("🤖 Hospital FAQ",)
        )

    # -----------------------------------------------------
    # APPOINTMENTS CARD
    # -----------------------------------------------------

    with col2:

        st.success(
            "📅 **Appointments**"
        )

        st.write(
            "Book and manage appointments."
        )

        st.button(
            "Open Appointments →",
            key="home_appointments",
            use_container_width=True,
            on_click=navigate_to,
            args=("📅 Appointment Booking",)
        )

    # -----------------------------------------------------
    # DOCTORS CARD
    # -----------------------------------------------------

    with col3:

        st.warning(
            "👨‍⚕️ **Doctors**"
        )

        st.write(
            "View doctors and departments."
        )

        st.button(
            "View Doctors →",
            key="home_doctors",
            use_container_width=True,
            on_click=navigate_to,
            args=("👨‍⚕️ Doctors & Departments",)
        )

    st.divider()

    st.subheader(
        "🏥 Our Services"
    )

    service1, service2, service3 = st.columns(3)

    with service1:

        st.write("🤖 **Hospital FAQ**")

        st.caption(
            "Get general hospital information."
        )

    with service2:

        st.write("📅 **Online Appointments**")

        st.caption(
            "Book and manage appointments."
        )

    with service3:

        st.write("👨‍⚕️ **Doctor Information**")

        st.caption(
            "Explore doctors and departments."
        )

    st.divider()

    st.warning(
        "⚠️ This application provides general hospital information only. "
        "It does not provide medical diagnosis or treatment advice."
    )


# =========================================================
# HOSPITAL FAQ CHATBOT
# =========================================================

elif page == "🤖 Hospital FAQ":

    st.title(
        "🤖 Hospital FAQ Chatbot"
    )

    st.write(
        "Ask a question about CarePlus Hospital."
    )

    question = st.text_input(
        "Enter your question",
        placeholder="Example: What are the Cardiology OPD timings?"
    )

    if st.button("🔍 Ask"):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Finding your answer..."
            ):

                documents = vectorstore.similarity_search(
                    question,
                    k=3
                )

                context = "\n\n".join(
                    document.page_content
                    for document in documents
                )

                prompt = f"""
You are the CarePlus Hospital FAQ assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer is not available in the context,
say that the information is not available.

Do not provide medical diagnosis.
Do not provide treatment advice.
Do not invent hospital information.

Context:
{context}

User Question:
{question}
"""

                response = llm.invoke(
                    prompt
                )

            st.subheader(
                "💬 Answer"
            )

            st.write(
                response.content
            )

            st.divider()

            st.subheader(
                "📚 Sources Used"
            )

            for index, document in enumerate(
                documents,
                start=1
            ):

                with st.expander(
                    f"Source {index}"
                ):

                    st.write(
                        document.page_content
                    )


# =========================================================
# DOCTORS & DEPARTMENTS
# =========================================================

elif page == "👨‍⚕️ Doctors & Departments":

    st.title(
        "👨‍⚕️ Doctors & Departments"
    )

    st.write(
        "Explore the doctors available at CarePlus Hospital."
    )

    doctors = [

        ["Dr. Arun Kumar", "Cardiology", "12 years"],

        ["Dr. Priya Sharma", "Dermatology", "8 years"],

        ["Dr. Rahul Verma", "Orthopedics", "10 years"],

        ["Dr. Anitha Rao", "Pediatrics", "9 years"],

        ["Dr. Kiran Kumar", "Neurology", "11 years"]

    ]

    df_doctors = pd.DataFrame(
        doctors,
        columns=[
            "Doctor",
            "Department",
            "Experience"
        ]
    )

    st.dataframe(
        df_doctors,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "🏥 Available Departments"
    )

    departments = [

        "General Medicine",

        "Cardiology",

        "Dermatology",

        "Orthopedics",

        "Pediatrics",

        "Neurology",

        "ENT",

        "Ophthalmology"

    ]

    for department in departments:

        st.write(
            f"🏥 {department}"
        )

    st.divider()

    st.button(
        "📅 Book an Appointment",
        use_container_width=True,
        on_click=navigate_to,
        args=("📅 Appointment Booking",)
    )


# =========================================================
# APPOINTMENT BOOKING
# =========================================================

elif page == "📅 Appointment Booking":

    st.title(
        "📅 Appointment Booking"
    )

    st.write(
        "Fill in your details to book an appointment."
    )

    patient_name = st.text_input(
        "Patient Name"
    )

    phone = st.text_input(
        "Phone Number"
    )

    departments = [

        "General Medicine",

        "Cardiology",

        "Dermatology",

        "Orthopedics",

        "Pediatrics",

        "Neurology",

        "ENT",

        "Ophthalmology"

    ]

    department = st.selectbox(
        "Department",
        departments
    )

    doctor_mapping = {

        "Cardiology": "Dr. Arun Kumar",

        "Dermatology": "Dr. Priya Sharma",

        "Orthopedics": "Dr. Rahul Verma",

        "Pediatrics": "Dr. Anitha Rao",

        "Neurology": "Dr. Kiran Kumar",

        "General Medicine": "No doctor listed",

        "ENT": "No doctor listed",

        "Ophthalmology": "No doctor listed"

    }

    doctor = doctor_mapping[department]

    st.write(
        f"**Doctor:** {doctor}"
    )

    appointment_date = st.date_input(
        "Appointment Date",
        min_value=datetime.date.today()
    )


    # -----------------------------------------------------
    # OPD TIMINGS
    # -----------------------------------------------------

    opd_timings = {

        "General Medicine": {
            "days": [0, 1, 2, 3, 4, 5],
            "start": 8,
            "end": 12
        },

        "Cardiology": {
            "days": [0, 1, 2, 3, 4],
            "start": 10,
            "end": 13
        },

        "Dermatology": {
            "days": [0, 1, 2, 3, 4, 5],
            "start": 14,
            "end": 17
        },

        "Orthopedics": {
            "days": [0, 1, 2, 3, 4],
            "start": 9,
            "end": 12
        },

        "Pediatrics": {
            "days": [0, 1, 2, 3, 4, 5],
            "start": 10,
            "end": 13
        },

        "Neurology": {
            "days": [1, 3],
            "start": 15,
            "end": 18
        },

        "ENT": {
            "days": [],
            "start": None,
            "end": None
        },

        "Ophthalmology": {
            "days": [],
            "start": None,
            "end": None
        }

    }

    timing = opd_timings[department]


    # -----------------------------------------------------
    # CHECK OPD AVAILABILITY
    # -----------------------------------------------------

    if not timing["days"]:

        st.warning(
            f"No appointment schedule is currently available for {department}."
        )

    elif appointment_date.weekday() not in timing["days"]:

        st.warning(
            f"{department} OPD is not available on "
            f"{appointment_date.strftime('%A')}."
        )

    else:

        # -------------------------------------------------
        # CREATE 30-MINUTE SLOTS
        # -------------------------------------------------

        slots = []

        current_time = datetime.datetime.combine(
            appointment_date,
            datetime.time(
                timing["start"],
                0
            )
        )

        end_time = datetime.datetime.combine(
            appointment_date,
            datetime.time(
                timing["end"],
                0
            )
        )

        while current_time < end_time:

            slots.append(
                current_time.strftime("%H:%M")
            )

            current_time += datetime.timedelta(
                minutes=30
            )


        # -------------------------------------------------
        # GET BOOKED TIMES
        # -------------------------------------------------

        booked_times = get_booked_times(
            doctor,
            appointment_date
        )

        booked_times_clean = []

        for booked in booked_times:

            try:

                booked_dt = datetime.datetime.strptime(
                    booked,
                    "%H:%M:%S"
                )

                booked_times_clean.append(
                    booked_dt.strftime("%H:%M")
                )

            except ValueError:

                try:

                    booked_dt = datetime.datetime.strptime(
                        booked,
                        "%H:%M"
                    )

                    booked_times_clean.append(
                        booked_dt.strftime("%H:%M")
                    )

                except ValueError:

                    booked_times_clean.append(booked)


        # -------------------------------------------------
        # AVAILABLE SLOTS
        # -------------------------------------------------

        available_slots = [

            slot

            for slot in slots

            if slot not in booked_times_clean

        ]

        st.subheader(
            "⏰ Available Time Slots"
        )

        if booked_times_clean:

            st.write(
                "🔴 Already booked:"
            )

            st.write(
                ", ".join(booked_times_clean)
            )

        if not available_slots:

            st.error(
                "❌ No available slots for this date."
            )

        else:

            appointment_time = st.selectbox(
                "Select Appointment Time",
                available_slots
            )

            # ---------------------------------------------
            # BOOK APPOINTMENT
            # ---------------------------------------------

            if st.button(
                "📅 Book Appointment",
                use_container_width=True
            ):

                if not patient_name.strip():

                    st.error(
                        "Please enter patient name."
                    )

                elif (
                    not phone.isdigit()
                    or len(phone) != 10
                ):

                    st.error(
                        "Please enter a valid 10-digit phone number."
                    )

                elif appointment_date < datetime.date.today():

                    st.error(
                        "Appointment date cannot be in the past."
                    )

                elif appointment_exists(
                    doctor,
                    appointment_date,
                    appointment_time
                ):

                    st.error(
                        "❌ This appointment slot has already been booked."
                    )

                else:

                    add_appointment(
                        patient_name,
                        phone,
                        department,
                        doctor,
                        appointment_date,
                        appointment_time
                    )

                    appointments = get_appointments()

                    appointment_id = appointments[0][0]

                    st.success(
                        "✅ Appointment booked successfully!"
                    )

                    st.subheader(
                        "🧾 Appointment Confirmation"
                    )

                    st.info(
                        f"Appointment ID: {appointment_id}"
                    )

                    st.write(
                        f"**Patient:** {patient_name}"
                    )

                    st.write(
                        f"**Phone:** {phone}"
                    )

                    st.write(
                        f"**Department:** {department}"
                    )

                    st.write(
                        f"**Doctor:** {doctor}"
                    )

                    st.write(
                        f"**Date:** {appointment_date}"
                    )

                    st.write(
                        f"**Time:** {appointment_time}"
                    )

                    st.success(
                        "Status: Confirmed"
                    )


# =========================================================
# MY APPOINTMENTS
# =========================================================

elif page == "📋 My Appointments":

    st.title(
        "📋 My Appointments"
    )

    appointments = get_appointments()

    if not appointments:

        st.info(
            "No appointments found."
        )

    else:

        search = st.text_input(
            "🔍 Search appointment",
            placeholder=(
                "Search by ID, patient name, department or doctor"
            )
        )

        filtered_appointments = appointments

        if search.strip():

            search_lower = search.lower()

            filtered_appointments = [

                appointment

                for appointment in appointments

                if (

                    search_lower in str(
                        appointment[0]
                    ).lower()

                    or search_lower in appointment[1].lower()

                    or search_lower in appointment[3].lower()

                    or search_lower in appointment[4].lower()

                )

            ]

        if not filtered_appointments:

            st.warning(
                "No matching appointments found."
            )

        else:

            for appointment in filtered_appointments:

                (
                    appointment_id,
                    patient_name_db,
                    phone_db,
                    department_db,
                    doctor_db,
                    date_db,
                    time_db,
                    status_db
                ) = appointment

                with st.container():

                    st.subheader(
                        f"Appointment #{appointment_id}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"**Patient:** {patient_name_db}"
                        )

                        st.write(
                            f"**Phone:** {phone_db}"
                        )

                        st.write(
                            f"**Department:** {department_db}"
                        )

                        st.write(
                            f"**Doctor:** {doctor_db}"
                        )

                    with col2:

                        st.write(
                            f"**Date:** {date_db}"
                        )

                        st.write(
                            f"**Time:** {time_db}"
                        )

                        if status_db == "Confirmed":

                            st.success(
                                "Status: Confirmed"
                            )

                        else:

                            st.error(
                                "Status: Cancelled"
                            )

                    if status_db == "Confirmed":

                        if st.button(
                            "❌ Cancel Appointment",
                            key=f"cancel_{appointment_id}"
                        ):

                            cancel_appointment(
                                appointment_id
                            )

                            st.success(
                                "Appointment cancelled successfully."
                            )

                            st.rerun()

                    st.divider()


# =========================================================
# ADMIN LOGIN AND DASHBOARD
# =========================================================

elif page == "🔐 Admin Login":

    # -----------------------------------------------------
    # ADMIN LOGIN
    # -----------------------------------------------------

    if not st.session_state.admin_logged_in:

        admin_login()

    # -----------------------------------------------------
    # ADMIN DASHBOARD
    # -----------------------------------------------------

    else:

        st.title(
            "🔐 CarePlus Admin Dashboard"
        )

        st.success(
            "You are logged in as Admin."
        )

        if st.button(
            "🚪 Logout"
        ):

            st.session_state.admin_logged_in = False

            st.rerun()

        st.divider()

        appointments = get_appointments()

        if not appointments:

            st.info(
                "No appointments available."
            )

        else:

            df = pd.DataFrame(
                appointments,
                columns=[
                    "Appointment ID",
                    "Patient",
                    "Phone",
                    "Department",
                    "Doctor",
                    "Date",
                    "Time",
                    "Status"
                ]
            )

            # ---------------------------------------------
            # CONVERT DATE COLUMN
            # ---------------------------------------------

            df["Date"] = pd.to_datetime(
                df["Date"]
            ).dt.date

            # ---------------------------------------------
            # APPOINTMENT STATISTICS
            # ---------------------------------------------

            st.subheader(
                "📊 Appointment Statistics"
            )

            total = len(df)

            confirmed = len(
                df[df["Status"] == "Confirmed"]
            )

            cancelled = len(
                df[df["Status"] == "Cancelled"]
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Total Appointments",
                    total
                )

            with col2:

                st.metric(
                    "Confirmed",
                    confirmed
                )

            with col3:

                st.metric(
                    "Cancelled",
                    cancelled
                )

            st.divider()

            # ---------------------------------------------
            # SEARCH AND FILTER
            # ---------------------------------------------

            st.subheader(
                "🔎 Manage Appointments"
            )

            search = st.text_input(
                "Search",
                placeholder=(
                    "Patient name, phone, doctor, department or ID"
                )
            )

            department_filter = st.selectbox(
                "Filter by Department",

                ["All Departments"] + sorted(
                    df["Department"].unique().tolist()
                )
            )

            status_filter = st.selectbox(
                "Filter by Status",

                [
                    "All Status",
                    "Confirmed",
                    "Cancelled"
                ]
            )

            # ---------------------------------------------
            # DATE RANGE FILTER
            # ---------------------------------------------

            st.subheader(
                "📅 Filter by Date Range"
            )

            min_date = min(df["Date"])

            max_date = max(df["Date"])

            col1, col2 = st.columns(2)

            with col1:

                start_date = st.date_input(
                    "From Date",
                    value=min_date,
                    min_value=min_date,
                    max_value=max_date,
                    key="admin_start_date"
                )

            with col2:

                end_date = st.date_input(
                    "To Date",
                    value=max_date,
                    min_value=min_date,
                    max_value=max_date,
                    key="admin_end_date"
                )

            # ---------------------------------------------
            # APPLY FILTERS
            # ---------------------------------------------

            filtered_df = df.copy()

            # Search filter

            if search.strip():

                search_lower = search.lower()

                filtered_df = filtered_df[
                    filtered_df.apply(
                        lambda row:

                        search_lower in str(
                            row["Appointment ID"]
                        ).lower()

                        or search_lower in str(
                            row["Patient"]
                        ).lower()

                        or search_lower in str(
                            row["Phone"]
                        ).lower()

                        or search_lower in str(
                            row["Doctor"]
                        ).lower()

                        or search_lower in str(
                            row["Department"]
                        ).lower(),

                        axis=1
                    )
                ]

            # Department filter

            if department_filter != "All Departments":

                filtered_df = filtered_df[
                    filtered_df["Department"] == department_filter
                ]

            # Status filter

            if status_filter != "All Status":

                filtered_df = filtered_df[
                    filtered_df["Status"] == status_filter
                ]

            # Date range filter

            if start_date > end_date:

                st.error(
                    "From Date cannot be later than To Date."
                )

                filtered_df = filtered_df.iloc[0:0]

            else:

                filtered_df = filtered_df[
                    (filtered_df["Date"] >= start_date)
                    &
                    (filtered_df["Date"] <= end_date)
                ]

            st.write(
                f"Showing {len(filtered_df)} appointment(s)"
            )

            st.divider()

            # ---------------------------------------------
            # APPOINTMENT MANAGEMENT
            # ---------------------------------------------

            st.subheader(
                "📋 Appointment Management"
            )

            if filtered_df.empty:

                st.warning(
                    "No appointments match your filters."
                )

            else:

                for _, row in filtered_df.iterrows():

                    appointment_id = row["Appointment ID"]

                    with st.container():

                        st.markdown(
                            f"### 🧾 Appointment #{appointment_id}"
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            st.write(
                                f"**Patient:** {row['Patient']}"
                            )

                            st.write(
                                f"**Phone:** {row['Phone']}"
                            )

                            st.write(
                                f"**Department:** {row['Department']}"
                            )

                            st.write(
                                f"**Doctor:** {row['Doctor']}"
                            )

                        with col2:

                            st.write(
                                f"**Date:** {row['Date']}"
                            )

                            st.write(
                                f"**Time:** {row['Time']}"
                            )

                            st.write(
                                f"**Status:** {row['Status']}"
                            )

                        if row["Status"] == "Confirmed":

                            if st.button(
                                "❌ Cancel Appointment",
                                key=f"admin_cancel_{appointment_id}"
                            ):

                                cancel_appointment(
                                    appointment_id
                                )

                                st.success(
                                    "Appointment cancelled by admin."
                                )

                                st.rerun()

                        else:

                            st.error(
                                "This appointment is already cancelled."
                            )

                        st.divider()

            # ---------------------------------------------
            # APPOINTMENT ANALYTICS
            # ---------------------------------------------

            st.subheader(
                "📈 Appointment Analytics"
            )

            st.write(
                "Appointments by Department"
            )

            department_chart = (
                df["Department"].value_counts()
            )

            st.bar_chart(
                department_chart
            )

            st.write(
                "Appointments by Doctor"
            )

            doctor_chart = (
                df["Doctor"].value_counts()
            )

            st.bar_chart(
                doctor_chart
            )

            st.write(
                "Appointment Status"
            )

            status_chart = (
                df["Status"].value_counts()
            )

            st.bar_chart(
                status_chart
            )

            st.write(
                "Appointments by Date"
            )

            date_chart = (
                df["Date"].astype(str).value_counts().sort_index()
            )

            st.line_chart(
                date_chart
            )

            st.divider()

            # ---------------------------------------------
            # COMPLETE APPOINTMENT TABLE
            # ---------------------------------------------

            st.subheader(
                "📋 All Appointment Records"
            )

            display_df = df.copy()

            display_df["Date"] = (
                display_df["Date"].astype(str)
            )

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            # ---------------------------------------------
            # DOWNLOAD CSV REPORT
            # ---------------------------------------------

            st.subheader(
                "📥 Download Appointment Report"
            )

            st.write(
                "Download all appointment records as a CSV file."
            )

            csv_data = df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="📥 Download CSV Report",
                data=csv_data,
                file_name="careplus_appointment_report.csv",
                mime="text/csv",
                use_container_width=True
            )


# =========================================================
# SOURCES
# =========================================================

elif page == "📚 Sources":

    st.title(
        "📚 Sources Used by RAG"
    )

    st.write(
        "The chatbot uses the following hospital documents "
        "to retrieve information and answer questions."
    )

    source_files = [

        "hospital_information.txt",

        "departments.txt",

        "doctors.txt",

        "opd_timings.txt",

        "fees.txt",

        "appointment_rules.txt"

    ]

    for source in source_files:

        st.write(
            f"📄 {source}"
        )

    st.divider()

    st.info(
        "These documents are used as the knowledge base "
        "for the CarePlus Hospital FAQ chatbot."
    )
