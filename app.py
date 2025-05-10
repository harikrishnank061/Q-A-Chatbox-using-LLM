import streamlit as st
import cohere
from langchain.prompts import PromptTemplate

# Set your Cohere API key
COHERE_API_KEY = "vzSUUNFPnI6IBHil4qwn0rQxVDegkZaHL9cZNNiR"  # Replace with your actual key

# Function to get response from Cohere
def get_cohere_response(input_text, no_words, blog_style):
    co = cohere.Client(COHERE_API_KEY)

    # Define a well-structured prompt
    template = """
    You are a professional blog writer. Write an informative and engaging blog post for a {blog_style} audience.
    Topic: {input_text}
    Word count: approximately {no_words} words.
    The tone should be clear and informative.
    """
    
    prompt = PromptTemplate(
        input_variables=["blog_style", "input_text", "no_words"],
        template=template
    )

    formatted_prompt = prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words)

    response = co.generate(
        model='command-r',  # You can also use 'command-r+', 'command-xlarge-nightly', etc.
        prompt=formatted_prompt,
        max_tokens=300,
        temperature=0.5
    )

    return response.generations[0].text.strip()

# Streamlit UI
st.set_page_config(page_title="Generate Blogs",
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Blogs 🤖")

input_text = st.text_input("Enter the Blog Topic")

col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')
with col2:
    blog_style = st.selectbox(
        'Writing the blog for',
        ('Researchers', 'Data Scientist', 'Common People'),
        index=0
    )

submit = st.button("Generate")

if submit:
    if not input_text or not no_words:
        st.warning("Please fill out all fields.")
    else:
        try:
            no_words_int = int(no_words)
            with st.spinner("Generating your blog..."):
                response = get_cohere_response(input_text, no_words_int, blog_style)
                st.markdown(response)
        except ValueError:
            st.error("Please enter a valid number for 'No of Words'")
