# 🧰 AI Mini Apps (Streamlit)

This repo contains a **single Streamlit app** with a sidebar switcher for two tools:
- **📧 Email Generator**
- **💡 Startup Idea Generator**

## 🚀 Deploy on Streamlit Cloud
1. Push these files to a GitHub repo.
2. On Streamlit Cloud, create a new app and choose `app.py` as the script.
3. In **Advanced settings → Secrets**, add:
   ```toml
   OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"
   ```
4. Deploy!

## 📦 Files
- `app.py` – the Streamlit multi-tool app.
- `requirements.txt` – dependencies.
- `README.md` – this file.

## ✅ Local Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
