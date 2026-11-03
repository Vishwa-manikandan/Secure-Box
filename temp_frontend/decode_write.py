import base64
import sys

def write_file(filename, b64_content):
    content = base64.b64decode(b64_content).decode('utf-8')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    write_file(sys.argv[1], sys.argv[2])
