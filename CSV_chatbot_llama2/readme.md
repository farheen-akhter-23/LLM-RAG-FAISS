# 📄 CSV Chatbot with LLaMA-2

## 🚀 Project Overview

This project is an **AI-powered chatbot** that allows users to interact with **CSV data** using a **LLaMA-2** model. The chatbot is built using **Streamlit**, **LangChain**, **FAISS**, and **Hugging Face models**, enabling users to upload a CSV file and ask queries about its contents.

The chatbot utilizes **Conversational Retrieval Chains** to fetch relevant answers based on user queries.

---

## 📚 Libraries Used

The following libraries are required for this project:

| Library              | Purpose |
|----------------------|--------------------------------------------------------|
| `streamlit`         | Frontend framework for interactive UI  |
| `streamlit_chat`    | Enables chat message styling in Streamlit |
| `tempfile`          | Handles temporary file storage for uploaded CSVs |
| `huggingface_hub`   | Downloads LLaMA-2 GGML models from Hugging Face |
| `langchain`         | Framework for AI-based retrieval chains |
| `sentence-transformers` | Provides Hugging Face embeddings for text retrieval |
| `faiss-cpu`         | Vector database for storing and retrieving embeddings |
| `ctransformers`     | Loads LLaMA-2 GGML models locally |
| `PyPDF2`            | Handles PDF parsing (if additional document support is needed) |

---

## 🔑 How to Get LLaMA-2 GGML Model

To use the **LLaMA-2 GGML model**, follow these steps:

1. **Visit TheBloke’s Hugging Face repository**:
   - [LLaMA-2 GGML Models - TheBloke](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML)
2. **Download the Required Model File**:
   - `llama-2-7b-chat.ggmlv3.q8_0.bin`
3. **Place it in the `./models/` directory** in your project folder.
4. **Ensure the file path is correct in `load_llm()`** function.

Alternatively, you can download the model programmatically:
```python
from huggingface_hub import hf_hub_download
hf_hub_download(repo_id="TheBloke/Llama-2-7B-Chat-GGML", filename="llama-2-7b-chat.ggmlv3.q8_0.bin", local_dir="./models")
```

---

## ⚙️ Installation & Setup Guide

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-repo/csv-chatbot-llama2.git
cd csv-chatbot-llama2
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

### **4️⃣ Run the Streamlit Application**
```bash
streamlit run app.py
```

---


## 🎯 Features

✅ AI-powered CSV-based Conversational Chatbot  
✅ Uses LLaMA-2 GGML Model  
✅ FAISS-powered Vector Search  
✅ Supports Large CSV Files  
✅ Interactive UI with Streamlit  
✅ Handles Long Queries with Token Chunking  

---

## 🛠️ How to Use

1. **Upload a CSV file** via the Streamlit interface.
2. **Ask questions** about the data inside the file.
3. The **LLaMA-2 model** processes the query and retrieves relevant information.
4. **View the conversation** history for reference.

---

## 📌 Future Enhancements

- ✅ Support for multiple file types (PDF, JSON, Excel)
- ✅ Optimize memory usage for large datasets
- ✅ Improve query handling with advanced tokenization

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

🚀 **Happy Coding!** 🚀
