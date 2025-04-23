# FBD Analyzer & APDL Script Generator

A powerful Streamlit web app that helps mechanical engineers and students **analyze Free Body Diagrams (FBDs)** and **automatically generate ANSYS APDL scripts** using **OpenAI GPT-4 Vision**. Just upload your problem PDF and optionally an image of the FBD, and let AI do the rest.

---

## 🚀 Features

- 📄 **PDF Parsing**: Upload a PDF of the problem statement to automatically extract text.
- 🖼️ **FBD Image Analysis** (Optional): Upload an FBD image for visual understanding using GPT-4 Vision.
- 🧠 **AI-Powered Script Generation**: Generate complete ANSYS APDL scripts with material properties, boundary conditions, and loads.
- 📥 **Downloadable Output**: Get a ready-to-use `.inp` APDL script for your analysis.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **AI Model:** OpenAI GPT-4 Turbo + GPT-4 Vision  
- **PDF Processing:** PyPDF2  
- **Environment Management:** `python-dotenv`

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/lihtnes_14/fbd-apdl-generator.git
cd fbd-apdl-generator
```

### 2. Create venv and install the required packages
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create .env file and store the OPENAI API KEY
```bash
touch .env
```

### 4. Run the app
```bash
streamlit run app.py
```

