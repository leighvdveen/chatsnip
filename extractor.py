import ijson
from decimal import Decimal

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def extract_chat_from_json_stream(html_file, chat_name):
    json_data_str = ''
    capturing = False

    with open(html_file, 'r', encoding='utf-8') as file:
        for line in file:
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
        print("No JSON data found or failed to extract JSON data.")
        return None

    try:
        chat_data = ijson.items(json_data_str, 'item')
        for item in chat_data:
            if isinstance(item, dict) and item.get("title") == chat_name:
                return extract_text_content_with_author(item)
    except Exception as e:
        print("Failed to decode JSON:", e)
        return None

def extract_text_content_with_author(chat_item):
    extracted_text = []
    debug_messages = []  # List to collect debug messages

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
                            debug_messages.append(f"Skipping message with missing or malformed content: {value}")
                    else:
                        debug_messages.append(f"Skipping non-dict message value: {type(value)}")
                elif isinstance(value, (dict, list)):
                    recursive_extract(value)
                else:
                    debug_messages.append(f"Unexpected data type for key '{key}': {type(value)}")
        elif isinstance(mapping, list):
            for item in mapping:
                if isinstance(item, (dict, list)):
                    recursive_extract(item)
                else:
                    debug_messages.append(f"Skipping non-dict/list item in list: {type(item)}")
        else:
            debug_messages.append(f"Unexpected data type at top level: {type(mapping)}")

    if isinstance(chat_item.get('mapping'), dict):
        recursive_extract(chat_item['mapping'])
    else:
        debug_messages.append("No valid 'mapping' found in the chat item.")

    # Optionally display the debug messages if needed
    # Uncomment the following line if you want to display them:
    # st.warning("\n".join(debug_messages))

    return "\n\n".join(extracted_text)