# 🏥 CarePlus Hospital – AI-Powered RAG Assistant

CarePlus Hospital is an AI-powered hospital FAQ and appointment management application built using Retrieval-Augmented Generation (RAG). It helps users access hospital-related information, explore doctors and departments, and manage appointments through an interactive web application.

## 🚀 Features

- 🤖 **AI Hospital FAQ Chatbot** – Answers hospital-related questions using a RAG-based approach.
- 👨‍⚕️ **Doctors & Departments** – Displays hospital doctors and available departments.
- 📅 **Appointment Booking** – Allows users to book appointments.
- ⏰ **Automatic Time Slots** – Provides appointment time slots.
- 🚫 **Booked Slot Prevention** – Prevents booking already occupied slots.
- 📋 **My Appointments** – Allows users to view their appointments.
- 🔐 **Admin Login** – Provides administrator access.
- 📊 **Admin Dashboard** – Displays appointment information and analytics.
- 🔎 **Appointment Search & Filters** – Helps administrators find appointment records.
- ❌ **Appointment Cancellation** – Allows administrators to cancel appointments.
- 📥 **CSV Report Download** – Exports appointment records as a CSV file.
- 📅 **Date-Range Filtering** – Filters appointment records by selected dates.

## 🛠️ Technologies Used

- Python
- Streamlit
- LangChain
- Google Gemini API
- Retrieval-Augmented Generation (RAG)
- FAISS
- Sentence Transformers
- PyPDF
- SQLite
- Pandas

## 🧠 Project Concept

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from hospital documents and provide context-based answers through an AI chatbot.

## 📂 Project Structure

```text
HospitalFAQ_RAG/
│
├── app.py
├── create_vectorstore.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
├── vectorstore/
└── venv/
```

*Note: Update this structure if your actual project folders or filenames differ.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/shaikjafiyanaz25-a11y/Gen.git
```

### 2. Navigate to the project folder

```bash
cd Gen
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API key

Configure your Gemini API key using Streamlit secrets or environment variables. Never upload API keys to GitHub.

### 7. Run the application

```bash
streamlit run app.py
```

The application will open at:

```text
http://localhost:8501
```

## 🎯 Project Objective

The main objective of CarePlus Hospital is to simplify hospital information access and appointment management by combining AI-powered document retrieval with a user-friendly web interface.

## 🔮 Future Enhancements

- Multilingual hospital FAQ support.
- PDF appointment report generation.
- Improved chatbot response accuracy.
- Enhanced user authentication.
- Deployment with cloud hosting.

## 👩‍💻 Developer

**Shaik Jafiya Naz**

GitHub: [shaikjafiyanaz25-a11y](https://github.com/shaikjafiyanaz25-a11y)

Project Repository: [Gen](https://github.com/shaikjafiyanaz25-a11y/Gen)

---

⭐ If you find this project interesting, consider starring the repository!
