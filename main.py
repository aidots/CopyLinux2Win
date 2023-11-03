import time
import requests
from PIL import Image
import io
import win32clipboard
from urllib.parse import urlparse
import subprocess

# 辅助函数：判断链接是否指向一个有效的图片
def is_valid_image_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme) and parsed.path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))

# 辅助函数：尝试用PIL打开以判断是否为图片
def is_image_file(filepath):
    try:
        Image.open(filepath)
        return True
    except IOError:
        return False

def download_image(url, local_path):
    # 下载图像并保存到本地路径
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(response.content)
    return local_path

# 将图片复制到剪贴板的函数
def image_to_clipboard(image_path):
    image = Image.open(image_path)
    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]  # 去掉位图文件头
    output.close()

    win32clipboard.OpenClipboard()  # 打开剪贴板
    win32clipboard.EmptyClipboard()  # 清空剪贴板
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)  # 设置剪贴板数据
    win32clipboard.CloseClipboard()  # 关闭剪贴板

# 从互联网下载图片并复制到剪贴板
def download_and_copy_image(url):
    # response = requests.get(url)
    # image = Image.open(io.BytesIO(response.content))
    local_image_path = download_image(url, 'local_temp_image')
    if local_image_path and is_image_file(local_image_path):
        image_to_clipboard(local_image_path)

# 检查并处理本地文件路径
def handle_local_file_path(clipboard_content, path_keyword, local_path_prefix):
    if path_keyword in clipboard_content:
        modified_content = clipboard_content.replace(path_keyword, "")
        src_path = local_path_prefix + modified_content

        ps_script_path = 'copy.ps1'

        # 使用subprocess.run来运行PowerShell脚本
        completed_process = subprocess.run(
            ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ps_script_path, "-FilePath", src_path],
            capture_output=True,
            text=True,
            check=True
        )
        # 打印输出结果，如果有的话
        print(completed_process.stdout)

        # 如果有错误，打印错误信息
        if completed_process.stderr:
            print("Error:", completed_process.stderr)

# 监控剪贴板内容的主循环
while True:
    time.sleep(1)  # 间隔1秒检查一次剪贴板内容
    try:
        win32clipboard.OpenClipboard()  # 打开剪贴板
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
            clipboard_content = win32clipboard.GetClipboardData()  # 读取剪贴板内容
        else:
            clipboard_content = None
        win32clipboard.CloseClipboard()  # 关闭剪贴板
    except Exception as e:
        print(f"Error: {e}")
        continue

    # 处理剪贴板内容
    if clipboard_content:
        if is_valid_image_url(clipboard_content):
            download_and_copy_image(clipboard_content)
        else:
            handle_local_file_path(clipboard_content, "/media/aigc/Linux/", "Z:/")
            handle_local_file_path(clipboard_content, "/home/aigc/", "Y:/")
