#!/usr/bin/env python3
"""
审核脚本 .review.py — 验证论文元数据完整性
用法：python3 .review.py <文件路径>
返回码：
  0 = 审核通过（移到原文库）
  1 = 审核失败（打回补充）
  2 = 参数错误
"""
import sys
import os
import shutil

def validate_paper(filepath):
    """检查论文元数据完整性"""
    if not os.path.exists(filepath):
        return False, "文件不存在"

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    required_fields = ['# 标题', '# 作者', '# 发表时间', '# 来源']
    missing = []
    for field in required_fields:
        if field not in content:
            missing.append(field)

    # 检查来源是否为白名单期刊/机构
    whitelist = [
        'Computers and Education', 'British Journal of Educational Technology',
        'Education and Information Technologies', 'Interactive Learning Environments',
        'Computer Assisted Language Learning', 'Educational Technology Research and Development',
        'International Journal of Instruction', 'International Journal of Educational Technology',
        'International Journal of Emerging Technologies in Learning',
        'et_R&D', 'ETR&D', 'Journal of Educational Computing Research',
        '开放教育研究', '电化教育研究', '中国电化教育', '课程·教材·教法',
        '中国教育学刊', '教育研究', '远程教育杂志', '现代教育技术',
        '中国远程教育', '教育发展研究', '外语电化教学',
        'Computers & Education', 'AI and Education',
        'arXiv', 'OECD', 'UNESCO', 'World Bank'
    ]

    has_source = any(kw in content for kw in whitelist)
    if not has_source:
        missing.append("# 来源（无白名单期刊或机构）")

    # 拒绝商业内容
    reject_keywords = ['艾瑞咨询', 'IDC', 'Gartner', '艾媒咨询', '前瞻产业研究院',
                       '36kr', '虎嗅', '钛媒体', '雷锋网', '市场研究', '行业白皮书']
    for kw in reject_keywords:
        if kw in content:
            return False, f"商业内容（{kw}）- 拒绝入库"

    if missing:
        return False, f"缺少字段：{'、'.join(missing)}"

    return True, "通过"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 .review.py <文件路径>")
        sys.exit(2)

    filepath = sys.argv[1]
    valid, msg = validate_paper(filepath)

    if valid:
        # 移到原文库（去掉 .pending）
        dest = filepath.replace('/.pending/', '/')
        try:
            shutil.move(filepath, dest)
            print(f"✅ 审核通过：{msg} → 已移到原文库")
        except Exception as e:
            print(f"✅ 审核通过：{msg}（移动失败：{e}）")
        sys.exit(0)
    else:
        print(f"❌ 审核失败：{msg}")
        sys.exit(1)
