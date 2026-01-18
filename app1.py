import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="AI Content Writer", page_icon="✍️", layout="wide")

# Title and Description
st.title("✍️ AI Content Writer (Pro Version)")
st.markdown("Gemini ရဲ့ နောက်ဆုံးထွက် Model များကို အသုံးပြုထားပါတယ်")

# --- Sidebar for Settings ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key Input
    api_key = st.text_input("Gemini API Key", type="password", help="Get your key from Google AI Studio")
    
    # Setup Gemini if key is provided
    if api_key:
        genai.configure(api_key=api_key)
        st.success("API Key is set! ✅")
    else:
        st.warning("Please enter your API Key to start.")

    st.divider()
    
    # --- Model Selection (New Feature) ---
    st.subheader("🤖 AI Model")
    selected_model = st.selectbox(
        "Choose Model",
        ["gemini-1.5-pro", "gemini-2.5-flash", "gemini-2.0-flash-exp"],
        index=0, # Default to 1.5 Pro for best writing
        help="Pro is better for creative writing. Flash is faster."
    )

    st.divider()
    
    # Options
    tone = st.selectbox("Tone (လေသံ)", ["Professional", "Casual", "Witty", "Friendly", "Formal", "Emotional"])
    length = st.selectbox("Length (အရှည်)", ["Short", "Medium", "Long"])
    language = st.selectbox("Language", ["English", "Burmese", "Thai"])

# --- Main Content Area ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input")
    prompt_text = st.text_area("ဘာအကြောင်းရေးချင်လဲ? (Prompt)", height=250, placeholder="Write a facebook post about...")
    
    generate_btn = st.button("✨ Generate Content", type="primary", use_container_width=True)

with col2:
    st.subheader("Output")
    
    if generate_btn:
        if not api_key:
            st.error("API Key ထည့်သွင်းရန် လိုအပ်ပါသည်။ Sidebar မှာ ထည့်ပေးပါ။")
        elif not prompt_text:
            st.error("Please enter a prompt.")
        else:
            try:
                with st.spinner(f"{selected_model} ဖြင့် ရေးသားနေပါသည်... ⏳"):
                    # Construct the full prompt
                    full_prompt = f"""
                    You are an expert content writer.
                    Topic: {prompt_text}
                    Tone: {tone}
                    Length: {length}
                    Language: {language}
                    
                    Please write the content based on these requirements.
                    """
                    
                    # Call Selected Gemini Model
                    model = genai.GenerativeModel(selected_model)
                    response = model.generate_content(full_prompt)
                    
                    # Display Result
                    st.markdown(response.text)
                    st.success("ပြီးပါပြီ! 🎉")
            except Exception as e:
                st.error(f"Error occurred: {e}")
                st.info("Tip: If using 'gemini-2.0-flash-exp', ensure your API key has access to experimental models.")

# Footer
st.markdown("---")
st.caption(f"Running on {selected_model}")