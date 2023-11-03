import time
import requests
from PIL import Image
import io
import win32clipboard
from urllib.parse import urlparse
import subprocess

# Helper function: Check if the link points to a valid image
def is_valid_image_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme) and parsed.path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))

# Helper function: Attempt to open with PIL to check if it's an image
def is_image_file(filepath):
    try:
        Image.open(filepath)
        return True
    except IOError:
        return False

# Download an image and save it to a local path
def download_image(url, local_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(response.content)
    return local_path

# Function to copy an image to the clipboard
def image_to_clipboard(image_path):
    image = Image.open(image_path)
    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]  # Remove the bitmap file header
    output.close()

    win32clipboard.OpenClipboard()  # Open the clipboard
    win32clipboard.EmptyClipboard()  # Clear the clipboard
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)  # Set clipboard data
    win32clipboard.CloseClipboard()  # Close the clipboard

# Download an image from the internet and copy it to the clipboard
def download_and_copy_image(url):
    local_image_path = download_image(url, 'local_temp_image')
    if local_image_path and is_image_file(local_image_path):
        image_to_clipboard(local_image_path)

# Check and process local file paths
def handle_local_file_path(clipboard_content, path_keyword, local_path_prefix):
    if clipboard_content.startswith(path_keyword) and path_keyword in clipboard_content:
        modified_content = clipboard_content.replace(path_keyword, "")
        src_path = local_path_prefix + modified_content

        ps_script_path = 'copy.ps1'

        # Use subprocess.run to execute PowerShell script
        completed_process = subprocess.run(
            ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ps_script_path, "-FilePath", src_path],
            capture_output=True,
            text=True,
            check=True
        )
        # Print the output result if any
        print(completed_process.stdout)

        # Print error if there is one
        if completed_process.stderr:
            print("Error:", completed_process.stderr)

# Main loop to monitor clipboard content
while True:
    time.sleep(1)  # Check clipboard content every 1 second
    try:
        win32clipboard.OpenClipboard()  # Open the clipboard
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
            clipboard_content = win32clipboard.GetClipboardData()  # Read clipboard content
        else:
            clipboard_content = None
        win32clipboard.CloseClipboard()  # Close the clipboard
    except Exception as e:
        print(f"Error: {e}")
        continue

    # Process clipboard content
    if clipboard_content:
        if is_valid_image_url(clipboard_content):
            download_and_copy_image(clipboard_content)
        else:
            handle_local_file_path(clipboard_content, "/media/aigc/Linux/", "Z:/")
            handle_local_file_path(clipboard_content, "/home/aigc/", "Y:/")
