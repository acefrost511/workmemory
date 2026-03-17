
import os
import json
from pathlib import Path

def read_file(file_path):
    """读取单个文件的内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"[ERROR] Could not read file: {str(e)}"

def is_text_file(file_path):
    """判断是否为文本文件"""
    text_extensions = {
        '.md', '.txt', '.json', '.py', '.js', '.html', '.css', 
        '.mjs', '.yaml', '.yml', '.xml', '.csv', '.rst', '.mdx',
        '.sh', '.bash', '.zsh', '.fish', '.bat', '.cmd',
        '.java', '.c', '.cpp', '.h', '.hpp', '.go', '.rs',
        '.ts', '.tsx', '.jsx', '.vue', '.svelte',
        '.sql', '.graphql', '.gql',
        '.dockerfile', '.env', '.gitignore',
        '.toml', '.ini', '.cfg', '.conf'
    }
    
    ext = Path(file_path).suffix.lower()
    if ext in text_extensions:
        return True
    
    # 无扩展名的文件，尝试读取判断
    if not ext:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(1024)
                return True
        except:
            return False
    
    return False

def traverse_directory(root_dir, output_file):
    """递归遍历目录并读取所有文件"""
    all_content = []
    
    for root, dirs, files in os.walk(root_dir):
        # 跳过 .git 目录
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, root_dir)
            
            # 跳过一些不需要的文件
            if file.startswith('.') and not file == '.gitignore':
                continue
            
            if is_text_file(file_path):
                print(f"Reading: {relative_path}")
                content = read_file(file_path)
                
                all_content.append(f"\n{'='*80}")
                all_content.append(f"FILE: {relative_path}")
                all_content.append(f"{'='*80}\n")
                all_content.append(content)
                all_content.append("\n")
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_content))
    
    print(f"\nDone! All content written to {output_file}")

if __name__ == "__main__":
    repo_dir = "/root/.openclaw/workspace/workmemory"
    output_file = "/root/.openclaw/workspace/workmemory_all_content.txt"
    
    traverse_directory(repo_dir, output_file)

