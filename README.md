# 🥗 MacroSnap — Your AI Nutrition Buddy

A modern, mobile-responsive nutrition chatbot with Groq 120B AI and direct WhatsApp click-to-chat integration. Built with Streamlit, Groq AI, and a high-end Sage Green Bento design system.

---

## ✨ Features

- **⚡ Groq 120B AI Engine**: Fast meal breakdown and intelligent nutrition insights.
- **🍱 3-Column Macro Bento Cards**: Real-time visualization for Calories, Protein, Carbs, and Healthy Fats.
- **📊 Macro Caloric Ratio Bar**: Dynamic segmented distribution bar (Protein / Carbs / Fats).
- **📲 Direct WhatsApp Integration**: 1-click WhatsApp summary generator without requiring Twilio or sandbox setup.
- **📱 Responsive UI**: Mobile-first single column and desktop 2-column split dashboard.
- **🔒 Privacy First**: Secrets and API keys are stored securely.

---

## 🚀 Quickstart Locally

1. **Clone repository:**
   ```bash
   git clone https://github.com/<your-username>/macrosnap.git
   cd macrosnap
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # Windows
   # source .venv/bin/activate  # macOS / Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API Key:**
   Create `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "your-groq-api-key"
   ```

5. **Run the app:**
   ```bash
   streamlit run app.py
   ```

---

## 🌐 Deploy to Streamlit Community Cloud (Free)

1. Push this repo to your GitHub.
2. Sign in at [share.streamlit.io](https://share.streamlit.io).
3. Click **"New app"** -> select this repository -> file: `app.py`.
4. In **Settings > Secrets**, add:
   ```toml
   GROQ_API_KEY = "your-groq-api-key"
   ```
5. Click **Deploy**!
