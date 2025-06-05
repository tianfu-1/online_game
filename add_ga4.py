import os
import glob

# GA4跟踪代码
ga4_code = '''    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-7085X13XLH"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-7085X13XLH');
    </script>
'''

def add_ga4_to_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经包含GA4代码
    if 'G-7085X13XLH' in content:
        print(f"跳过 {file_path} - 已包含GA4代码")
        return
    
    # 在<head>标签后插入GA4代码
    modified_content = content.replace('<head>', '<head>\n' + ga4_code)
    
    # 保存修改后的文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    print(f"已添加GA4代码到 {file_path}")

def main():
    # 处理根目录的index.html
    if os.path.exists('index.html'):
        add_ga4_to_file('index.html')
    
    # 处理games目录下的所有HTML文件
    games_path = os.path.join('onlinegames', 'games', '*.html')
    for file_path in glob.glob(games_path):
        add_ga4_to_file(file_path)

if __name__ == '__main__':
    main() 