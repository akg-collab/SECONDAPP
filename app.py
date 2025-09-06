import os
import streamlit as st
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI

st.set_page_config(page_title="AI Mini Apps", page_icon="🧰")

# ====== Health Check ======
with st.expander("🔍 Health Check"):
    st.write("Python:", os.sys.version)
    st.write("OPENAI_API_KEY set:", "OPENAI_API_KEY" in st.secrets)

# ====== Secrets / API Key ======
try:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
except Exception:
    st.error("Missing OPENAI_API_KEY in Streamlit Secrets. Add it in Advanced settings → Secrets.")
    st.stop()

# ====== Sidebar Navigation ======
st.sidebar.title("🧰 AI Mini Apps")
app_choice = st.sidebar.radio("Choose a tool:", ["📧 Email Generator", "💡 Startup Idea Generator"])

# ====== Common LLM ======
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

# ====== Email Generator ======
def email_generator():
    st.title("📧 Email Generator")
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
        prompt = PromptTemplate(
            template=template,
            input_variables=["subject", "sender", "tone"]
        )
        chain = prompt | llm
        response = chain.invoke({"subject": subject, "sender": sender, "tone": tone})
        st.subheader("✉️ Generated Email:")
        st.write(response.content)

# ====== Startup Idea Generator ======
def idea_generator():
    st.title("💡 Startup Idea Generator")
    industry = st.text_input("🌍 Industry / Domain (e.g., Healthcare, Education, Fintech)")
    audience = st.text_input("👥 Target Audience (e.g., Students, SMEs, Doctors)")
    budget = st.selectbox("💸 Budget Level", ["Low", "Medium", "High"])
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
        prompt = PromptTemplate(
            template=template,
            input_variables=["industry", "audience", "budget", "tone"]
        )
        chain = prompt | llm
        response = chain.invoke({
            "industry": industry,
            "audience": audience,
            "budget": budget,
            "tone": tone
        })
        st.subheader("🚀 Generated Ideas:")
        st.write(response.content)

# ====== Router ======
if app_choice.startswith("📧"):
    email_generator()
else:
    idea_generator()

st.caption("Ready ✅  •  Switch apps from the sidebar")