from bs4 import BeautifulSoup
import sys
import os

def extract_chat_from_html(html_file, chat_name, output_file=None):
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
        
        chat = soup.find('div', {'class': 'chat-name'}, string=chat_name)
        
        if chat:
            chat_content = chat.find_parent('div', {'class': 'chat-history'})
            if chat_content:
                chat_text = chat_content.get_text(separator='\n').strip()
                
                if output_file:
                    with open(output_file, 'w', encoding='utf-8') as out_file:
                        out_file.write(chat_text)
                    print(f"Chat content saved to {output_file}")
                else:
                    print(chat_text)
            else:
                print(f"Chat named '{chat_name}' was found, but no content could be extracted.")
        else:
            print(f"Chat named '{chat_name}' was not found in the HTML file.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_chat.py <html_file> <chat_name> [output_file]")
    else:
        html_file = sys.argv[1]
        chat_name = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        extract_chat_from_html(html_file, chat_name, output_file)