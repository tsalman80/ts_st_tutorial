import streamlit as st
import streamlit_authenticator as stauth
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

if (
    "authentication_status" not in st.session_state
    or st.session_state["authentication_status"] is None
):
    st.switch_page("pages/login.py")

with st.sidebar:
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.write("")
    st.write("")
    st.write("")
    authenticator = st.session_state["authenticator"]

    if not authenticator:
        st.switch_page("pages/login.py")

    authenticator.logout(location="sidebar")


# Get your OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")  # Used in production
# api_key = 'sk-N……'
client = OpenAI(api_key=api_key)

# Cell 2: Title & Description
st.title("🤖 AI Content Assistant")
st.markdown("I was made to help you craft interesting Social media posts.")


# Cell 3: Function to generate text using OpenAI
def analyze_text(text):
    if not api_key:
        st.error(
            "OpenAI API key is not set. Please set it in your environment variables."
        )
        return

    client = OpenAI(api_key=api_key)
    model = "gpt-4o-mini"  # Using the GPT-3.5 model

    # Instructions for the AI (adjust if needed)
    messages = [
        {
            "role": "system",
            "content": "You are an assistant who helps craft social media posts.",
        },
        {
            "role": "user",
            "content": f"Please help me write a social media post based on the following:\n{text}",
        },
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,  # Lower temperature for less random responses
    )
    return response.choices[0].message.content


# Cell 4: Function to generate the image
def generate_image(text):
    if not api_key:
        st.error(
            "OpenAI API key is not set. Please set it in your environment variables."
        )
        return

    response = client.images.generate(
        model="gpt-4o-mini",
        prompt=text,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # Assuming the API returns an image URL; adjust based on actual response structure
    return response.data[0].url


# Cell 4: Streamlit UI
user_input = st.text_area(
    label="Enter a brief for your post:",
    placeholder="Ex: Cats running around in a field of flowers",
)


if st.button("Generate Post Content"):
    with st.spinner("Generating Text..."):
        post_text = analyze_text(user_input)
        st.write(post_text)

    with st.spinner("Generating Thumbnail..."):
        thumbnail_url = generate_image(
            user_input
        )  # Consider adjusting the prompt for image generation if needed
        st.image(thumbnail_url, caption="Generated Thumbnail")
