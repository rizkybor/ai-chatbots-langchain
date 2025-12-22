# 🚀 FINAL PROJECT – LLM FOR DATA SCIENTIST

## 🔎 Search Engine Assistant  
**LLM-powered SEO Content Generator**

---

## 👤 Author
**Rizky Ajie Kurniawan | rizkyak994@gmail.com**

---

## 🎓 Project Category
**Final Project – LLM for Data Scientist**

---

## 🛠️ Technology Stack
- Python 3.10+
- Streamlit
- Large Language Model (LLM) via Groq API
- Custom HTML & CSS (Streamlit Styling)
- Prompt Engineering

---

## 📖 Project Description
This project is a web-based AI assistant designed to generate **Search Engine Optimization (SEO)**
content using a **Large Language Model (LLM)**.

The application allows users to input a short business or product description  
(e.g., *jasa renovasi rumah* or *produk skincare*) and instantly receive **structured marketing outputs**, including:

- SEO Title  
- Meta Description  
- Focus Keyword  
- Secondary Keywords  
- Hashtags  
- Call To Action (CTA)  
- Content Snippet  

The application is built using **Streamlit** and integrates an LLM through the **Groq API** to demonstrate
practical LLM usage for real-world, data-driven content generation.

This project emphasizes applied LLM usage, prompt structuring, output formatting, and
user-facing deployment rather than model training.

---

## 🎯 Project Objectives
1. Demonstrate practical integration of LLMs into a production-style application.
2. Apply prompt engineering techniques to generate structured marketing outputs.
3. Showcase UI/UX customization within Streamlit using HTML and CSS.
4. Build an end-to-end AI-powered tool relevant to data science and business use cases.
5. Illustrate how LLMs can augment decision-making and content workflows.

---

## ✨ Key Features
- Secure API Key input (Groq API)
- Password-masked API key field
- Controlled input width for sensitive data
- Chat-based user interaction
- Structured AI-generated SEO content
- Copy-to-clipboard functionality for each output section
- Clean UI with hidden default icons
- Responsive layout with fixed chat input positioning

---

## 🧠 LLM Usage Explanation
The Large Language Model is used as an inference engine to generate SEO-focused content
based on natural language input from the user.

Key aspects of LLM utilization:
- Zero-shot prompt execution
- Controlled output structure via prompt design
- Text post-processing and segmentation
- No model fine-tuning required  

The LLM acts as a semantic generator, transforming short business descriptors into
actionable marketing content.

---

## 📊 Why This Is a Data Scientist Project
Although this project does not involve training a model from scratch, it reflects
real-world responsibilities of a data scientist working with LLMs, including:

- Designing prompts for consistent, structured outputs
- Evaluating LLM-generated text quality
- Integrating AI services into data-driven applications
- Translating business needs into AI-assisted solutions
- Deploying AI models into user-facing tools

This aligns with modern data science roles, where LLM orchestration and application
development are core competencies.

---

## 🏗️ Project Architecture
1. User Interface (Streamlit)  
2. API Key Validation Layer  
3. Prompt Submission via Chat Input  
4. LLM Inference using Groq API  
5. Response Parsing and Formatting  
6. HTML-based Result Rendering  
7. Session State Management  

---

## 🔐 Security Considerations
- API key input is password-masked
- API key stored only in session environment variables
- No API key persistence to disk
- Application execution stops if API key is not provided

---

## ⚠️ Limitations
- No long-term conversation memory
- No database persistence
- Dependency on external LLM availability (Groq API)
- Output quality depends on prompt effectiveness

---

## 🚀 Future Enhancements
- Multi-language SEO content generation
- Keyword competitiveness analysis
- Prompt versioning and A/B testing
- Analytics on generated content
- Integration with SEO tools (e.g., Google Search Console)
- Export results to CSV or DOCX

---

## ▶️ How to Run

```bash
pip install streamlit
streamlit run app.py
Steps:
    Input your Groq API Key when prompted
    Enter a business or product description
    Generate SEO content instantly
```

---

📝 Final Notes

This project represents a complete, production-style LLM application suitable as a
Final Project for LLM for Data Scientist.

It demonstrates applied Large Language Model usage, thoughtful UI design, and
practical problem-solving using modern AI technologies.

---

Created At : Desember 2025