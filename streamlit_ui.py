import streamlit as st
import ijson
import os
from io import StringIO

# Set the page configuration
st.set_page_config(page_title="ChatSnip", page_icon="📝")

def extract_chat_from_json_stream(html_content, chat_name):
    json_data_str = ''
    capturing = False

    for line in html_content.splitlines():  # Split into lines
        if 'var jsonData =' in line:
            capturing = True
            json_data_start = line.split('var jsonData =', 1)[1].strip()
            json_data_str += json_data_start
        elif capturing:
            json_data_str += line.strip()
            if line.strip().endswith('];'):
                json_data_str = json_data_str[:-2] + ']'
                break

    if not json_data_str:
        st.error("No JSON data found or failed to extract JSON data.")
        return None

    try:
        chat_data = ijson.items(StringIO(json_data_str), 'item')
        for item in chat_data:
            if isinstance(item, dict) and item.get("title") == chat_name:
                return extract_text_content_with_author(item)
    except Exception as e:
        st.error(f"Failed to decode JSON: {e}")
        return None

def extract_text_content_with_author(chat_item):
    extracted_text = []

    def recursive_extract(mapping):
        if isinstance(mapping, dict):
            for key, value in mapping.items():
                if key == 'message':
                    if isinstance(value, dict):
                        author_role = value.get('author', {}).get('role', 'unknown')
                        content = value.get('content')
                        if isinstance(content, dict) and 'parts' in content:
                            for part in content['parts']:
                                extracted_text.append(f"{author_role.capitalize()}: {part}")
                        else:
                            st.warning(f"Skipping message with missing or malformed content: {value}")
                    else:
                        st.warning(f"Skipping non-dict message value: {type(value)}")
                elif isinstance(value, (dict, list)):
                    recursive_extract(value)
                else:
                    st.warning(f"Unexpected data type for key '{key}': {type(value)}")
        elif isinstance(mapping, list):
            for item in mapping:
                if isinstance(item, (dict, list)):
                    recursive_extract(item)
                else:
                    st.warning(f"Skipping non-dict/list item in list: {type(item)}")
        else:
            st.warning(f"Unexpected data type at top level: {type(mapping)}")

    if isinstance(chat_item.get('mapping'), dict):
        recursive_extract(chat_item['mapping'])
    else:
        st.error("No valid 'mapping' found in the chat item.")

    return "\n\n".join(extracted_text)

# Streamlit app
st.title("ChatSnip - Chat Extractor")

uploaded_file = st.file_uploader("Upload a ChatGPT history/archive file:", type="html")
chat_name = st.text_input("Enter the chat name you want to snip out of the archive file:")

if st.button("Extract Chat"):
    if uploaded_file is not None and chat_name:
        html_content = uploaded_file.getvalue().decode("utf-8")  # Get the HTML content as a string
        chat_content = extract_chat_from_json_stream(html_content, chat_name)
        
        if chat_content:
            st.success("Chat extracted successfully!")
            st.text_area("Chat Content", chat_content, height=400)
            
            st.download_button("Download Chat", data=chat_content, file_name=f"{chat_name}.txt", mime="text/plain")
        else:
            st.error("Chat not found or content could not be extracted.")
    else:
        st.error("Please upload a file and enter a chat name.")