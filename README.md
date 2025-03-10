# 📄 ATS Resume Evaluator

## 🚀 Project Overview

This project is an **AI-powered ATS (Applicant Tracking System) Resume Evaluator** that analyzes resumes against job descriptions. It leverages **Google Gemini AI** to extract key insights, match scores, and missing keywords, helping job seekers optimize their resumes for ATS screening.

The application is built using **Streamlit**, integrated with **Google Generative AI (Gemini)** for natural language understanding, and supports **PDF & DOCX** resume uploads.

---

## 📚 Libraries Used
The following libraries are used in this project:

| Library         | Purpose |
|----------------|--------------------------------------------------------|
| `streamlit`    | Frontend framework for interactive UI  |
| `google.generativeai` | To interact with Google Gemini AI |
| `PyPDF2`       | Extract text from PDF resumes |
| `docx2txt`     | Extract text from DOCX resumes |
| `requests`     | Make API requests to external services |
| `re`           | Regular expressions for cleaning text |
| `json`         | Parsing and formatting AI responses |
| `dotenv`       | Load environment variables securely |
| `streamlit_lottie` | Display animations |

---

## 🔑 How to Generate Google Gemini API Keys
To use Google Gemini AI, follow these steps to obtain an API key:

1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google account.
3. Navigate to **API Keys**.
4. Click **Create API Key** and copy it.
5. Save the key in a **.env file** like this:

   ```plaintext
   GOOGLE_API_KEY=your_api_key_here
   ```
6. Ensure the API key is correctly loaded into the project using:

   ```python
   from dotenv import load_dotenv
   load_dotenv()
   api_key = os.getenv("GOOGLE_API_KEY")
   ```

---

## ⚙️ Installation & Setup Guide


### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-repo/ats-resume-evaluator.git
cd ats-resume-evaluator
```

### **2️⃣ Create a Virtual Environment (Recommended)**

```bash
python -m venv env
source env/bin/activate  # Mac/Linux
env\Scripts\activate    # Windows
```

### **3️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**

Create a `.env` file in the root directory and add:
```plaintext
GOOGLE_API_KEY=your_api_key_here
```

### **5️⃣ Run the Streamlit Application**

```bash
streamlit run app.py
```

---

## 📽️ Video Demonstration

A video tutorial is available to guide you through the setup and usage of this project.

🎥 https://github.com/user-attachments/assets/cbdcf53d-5bc4-4d11-9ec9-d4af28328082

---

## 🎯 Features

✅ AI-powered Resume Evaluation  
✅ Google Gemini AI Integration  
✅ Streamlit Interactive UI  
✅ PDF & DOCX Resume Support  
✅ ATS Match Score & Missing Keywords  
✅ Easy-to-Use API Integration  

---

## 🛠️ How to Use

1. Upload your resume (**PDF or DOCX**).
2. Paste the job description.
3. Click **Evaluate Resume**.
4. Get an ATS Match Score, Missing Keywords, and AI-generated insights.

---

## 📌 Future Enhancements

- ✅ Add support for multiple resume evaluation.
- ✅ Improve AI response accuracy with prompt engineering.
- ✅ Enhance UI with more data visualization.

---

## 🤝 Contributing

We welcome contributions! To contribute:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a Pull Request

---

## 📄 License

This project is licensed under the MIT License. Feel free to modify and distribute!

🚀 **Happy Coding & Job Hunting!** 🚀

