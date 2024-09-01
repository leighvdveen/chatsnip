import sys
from extractor import extract_chat_from_json_stream  # Import from extractor.py

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_chat.py <html_file> <chat_name> [output_file]")
    else:
        html_file = sys.argv[1]
        chat_name = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None

        extracted_text = extract_chat_from_json_stream(html_file, chat_name)

        if extracted_text:
            extracted_text_str = "\n\n".join(extracted_text)
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as out_file:
                    out_file.write(extracted_text_str)
                print(f"Chat content saved to {output_file}")
            else:
                print(extracted_text_str)
        else:
            print(f"Chat named '{chat_name}' was not found in the JSON data.")