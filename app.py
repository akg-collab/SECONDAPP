import os
import streamlit as st

# --- LangChain imports with compatibility fallbacks ---
try:
    from langchain_core.prompts import PromptTemplate
except Exception:
    try:
        from langchain.prompts import PromptTemplate
    except Exception:
        from langchain import PromptTemplate

from langchain_openai import ChatOpenAI

st.set_page_config(page_title="AKG AI Mini Apps", page_icon="🧰")

# ====== Branded Header ======
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🧰 AKG AI Mini Apps</h1>", unsafe_allow_html=True)
st.caption("Made by Ajay 🚀")

# ====== Secrets / API Key ======
with st.expander("🔑 Secrets / API Key check"):
    st.write("OPENAI_API_KEY set:", "OPENAI_API_KEY" in st.secrets)

try:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
except Exception:
    st.error("Missing OPENAI_API_KEY in Streamlit Secrets. Add it in Advanced settings → Secrets.")
    st.stop()

# ====== Sidebar ======
st.sidebar.header("Settings")
preset_models = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4.1-mini",
    "gpt-4.1",
    "gpt-5",
    "gpt-5-mini",
]
model = st.sidebar.selectbox("OpenAI model (preset)", preset_models, index=0)

temperature = st.sidebar.slider("Temperature", 0.0, 1.2, 0.7, 0.1)

# Build LLM with diagnostics
def build_llm():
    try:
        llm = ChatOpenAI(model_name=use_model, temperature=temperature, timeout=60)
        return llm, None
    except Exception as e:
        return None, e

llm, llm_err = build_llm()

with st.expander("🔍 Health Check"):
    st.write(f"Selected model: {use_model}")
    if llm_err:
        st.error(f"LLM init error: {llm_err}")
    else:
        try:
            ping = llm.invoke("Reply exactly with: OK")
            st.success(f"Init OK • Test reply: {ping.content[:50]}")
        except Exception as e:
            st.error("Health check invoke() failed")
            st.exception(e)
            st.info("Tip: If you see 404 model not found, switch model or type the exact model id you have access to. If 401, check your API key / org access.")

# ====== Apps ======
st.sidebar.title("Apps")
app_choice = st.sidebar.radio("Choose", ["📧 Email Generator", "💡 Startup Idea Generator"], index=1)

def email_generator():
    st.subheader("📧 Email Generator")
    subject = st.text_input("Subject")
    sender = st.text_input("Sender")
    tone = st.selectbox("Tone", ["Professional", "Casual", "Polite", "Funny"], index=0)

    if st.button("Generate Email"):
        template = """
        You are an assistant that drafts professional emails.

        Subject: {subject}
        Sender: {sender}
        Tone: {tone}

        Write a complete email in the specified tone. Keep it concise and clear.
        """
        prompt = PromptTemplate(template=template, input_variables=["subject","sender","tone"])
        chain = prompt | llm
        try:
            resp = chain.invoke({"subject": subject, "sender": sender, "tone": tone})
            st.subheader("✉️ Generated Email")
            st.write(resp.content)
        except Exception as e:
            st.error("Generation failed")
            st.exception(e)

def idea_generator():
    st.subheader("💡 Startup Idea Generator")
    industry = st.text_input("🌍 Industry / Domain")
    audience = st.text_input("👥 Target Audience")
    budget = st.selectbox("💸 Budget", ["Low", "Medium", "High"], index=0)
    tone = st.selectbox("🎨 Tone", ["Professional", "Casual", "Investor Pitch"], index=0)

    if st.button("Generate Startup Ideas"):
        template = """
        You are a startup consultant. Generate 3 startup ideas.

        Industry: {industry}
        Target Audience: {audience}
        Budget Level: {budget}
        Tone: {tone}

        For each idea, provide:
        - Name
        - One-line pitch
        - Why it solves a problem
        - Revenue potential
        """
        prompt = PromptTemplate(template=template, input_variables=["industry","audience","budget","tone"])
        chain = prompt | llm
        try:
            resp = chain.invoke({"industry": industry, "audience": audience, "budget": budget, "tone": tone})
            st.subheader("🚀 Generated Ideas")
            st.write(resp.content)
        except Exception as e:
            st.error("Generation failed")
            st.exception(e)

if not llm:
    st.stop()

if app_choice.startswith("📧"):
    email_generator()
else:
    idea_generator()

st.caption("© 2025 AKG | All rights reserved")
