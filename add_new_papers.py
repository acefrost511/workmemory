#!/usr/bin/env python3
"""Final master document update: add all new research from 9 agents"""
import re
from datetime import datetime

CUTOFF = datetime(2025, 9, 25)

# All new unique papers from 9 sub-agents (sorted by date, oldest first)
NEW_PAPERS = [
    # 2025-01
    {
        "section": "## 🛡️ 六、AI学术诚信与检测",
        "num": 81,
        "title_en": "Detecting AI-Generated Text in Educational Content: Leveraging Machine Learning and Explainable AI for Academic Integrity",
        "title_cn": "教育内容中AI生成文本检测：利用机器学习与可解释AI维护学术诚信",
        "source": "arXiv预印本（arXiv:2501.03203）",
        "date": "2025-01",
        "doi": "10.48550/arXiv.2501.03203",
        "url": "https://arxiv.org/abs/2501.03203",
        "oa": "是（arXiv完全开放获取）",
        "tags": "AI生成文本检测、机器学习、可解释AI（XAI）、CyberHumanAI数据集、教育场景"
    },
    # 2025-04
    {
        "section": "## 🎓 四、教师AI专业发展与课堂工具",
        "num": 82,
        "title_en": "Empowering educational leaders for AI integration in rural STEM education: Challenges and strategies",
        "title_cn": "赋能教育领导者推进农村STEM教育中的AI整合：挑战与策略",
        "source": "Frontiers in Education",
        "date": "2025-04",
        "doi": "10.3389/feduc.2025.1567698",
        "url": "https://doi.org/10.3389/feduc.2025.1567698",
        "oa": "是（CC BY许可）",
        "tags": "AI整合、农村STEM教育、教育领导力、专业发展"
    },
    # 2025-05
    {
        "section": "## 🌐 二、AI驱动智能辅导系统（ITS）",
        "num": 83,
        "title_en": "A systematic review of AI-driven intelligent tutoring systems (ITS) in K-12 education",
        "title_cn": "人工智能驱动智能辅导系统（ITS）在K-12教育中的系统综述",
        "source": "npj Science of Learning（Nature Partner Journals）",
        "date": "2025-05",
        "doi": "10.1038/s41539-025-00320-7",
        "url": "https://doi.org/10.1038/s41539-025-00320-7",
        "oa": "是（CC BY 4.0）",
        "tags": "智能辅导系统（ITS）、K-12教育、人工智能教育（AIEd）、机器学习、自适应学习"
    },
    {
        "section": "## 📝 七、评估与智能反馈",
        "num": 84,
        "title_en": "A Practical Guide for Supporting Formative Assessment and Feedback Using Generative AI",
        "title_cn": "生成式AI支持形成性评价与反馈实践指南",
        "source": "arXiv预印本（arXiv:2505.23405）",
        "date": "2025-05",
        "doi": "10.48550/arXiv.2505.23405",
        "url": "https://arxiv.org/abs/2505.23405",
        "oa": "是（arXiv开放获取）",
        "tags": "形成性评价、生成式AI、大语言模型（LLM）、课堂反馈策略、自调节学习"
    },
    {
        "section": "## ⚖️ 八、AI教育伦理、政策与治理",
        "num": 85,
        "title_en": "Pragmatic AI in education and its role in mathematics learning and teaching",
        "title_cn": "教育中的务实AI及其在数学教与学中的作用",
        "source": "npj Science of Learning（Nature）",
        "date": "2025-05",
        "doi": "10.1038/s41539-025-00315-4",
        "url": "https://doi.org/10.1038/s41539-025-00315-4",
        "oa": "是（CC BY-NC-ND 4.0）",
        "tags": "AI教育应用、数学学习、数学焦虑、师生互动、情感计算"
    },
    # 2025-06
    {
        "section": "## ⚖️ 八、AI教育伦理、政策与治理",
        "num": 86,
        "title_en": "Ethical and regulatory challenges of Generative AI in education: a systematic review",
        "title_cn": "生成式AI在教育中的伦理与监管挑战：系统综述",
        "source": "Frontiers in Education",
        "date": "2025-06",
        "doi": "10.3389/feduc.2025.1565938",
        "url": "https://doi.org/10.3389/feduc.2025.1565938",
        "oa": "是（CC BY 4.0）",
        "tags": "生成式AI伦理、监管框架、教育公平、数据隐私、系统综述"
    },
    # 2025-07
    {
        "section": "## 🌟 九、AI素养与批判性思维",
        "num": 87,
        "title_en": "Do AI Tutors Empower or Enslave Learners? Toward a Critical Use of AI in Education",
        "title_cn": "AI导师赋能还是奴役学习者？走向批判性使用AI教育",
        "source": "arXiv预印本（arXiv:2507.06878）· AIED 2025",
        "date": "2025-07",
        "doi": "10.48550/arXiv.2507.06878",
        "url": "https://arxiv.org/abs/2507.06878",
        "oa": "是（CC BY 4.0）",
        "tags": "AI导师、批判性思维、AI素养、学习者自主权、教育伦理"
    },
    # 2025-08
    {
        "section": "## 🎓 四、教师AI专业发展与课堂工具",
        "num": 88,
        "title_en": "Teaching and learning with AI: a qualitative study on K-12 teachers' use and engagement with artificial intelligence",
        "title_cn": "与AI共教：K-12教师使用与参与人工智能的质性研究",
        "source": "Frontiers in Education",
        "date": "2025-08",
        "doi": "10.3389/feduc.2025.1651217",
        "url": "https://doi.org/10.3389/feduc.2025.1651217",
        "oa": "是（CC BY许可）",
        "tags": "人工智能、教师能动性、数字教育、教育技术、教师培训"
    },
    {
        "section": "## 🌐 二、生成式AI（GenAI）在K12教育中的应用",
        "num": 89,
        "title_en": "Adopting generative AI in K-12 teaching and learning: Australian teachers' actions through the lens of innovation theory",
        "title_cn": "在K-12教学中采用生成式AI：基于创新理论视角的澳大利亚教师行动研究",
        "source": "Education and Information Technologies（Springer）",
        "date": "2025-08",
        "doi": "10.1007/s10639-025-13699-y",
        "url": "https://doi.org/10.1007/s10639-025-13699-y",
        "oa": "是（CC BY 4.0）",
        "tags": "生成式AI（GenAI）、K-12教师采纳、创新扩散理论、教育实践"
    },
    # 2025-09
    {
        "section": "## 📝 七、评估与智能反馈",
        "num": 90,
        "title_en": "A comprehensive review of AI-powered grading and tailored feedback in universities",
        "title_cn": "大学AI评分与定制化反馈系统综合综述",
        "source": "Discover Artificial Intelligence（Springer Nature）",
        "date": "2025-09",
        "doi": "10.1007/s44163-025-00517-0",
        "url": "https://doi.org/10.1007/s44163-025-00517-0",
        "oa": "是（CC BY 4.0）",
        "tags": "AI评分系统、教育评估、个性化反馈、机器学习与NLP自动化"
    },
    {
        "section": "## 🌐 二、生成式AI（GenAI）在K12教育中的应用",
        "num": 91,
        "title_en": "Generative AI use in K-12 education: a systematic review",
        "title_cn": "生成式AI在K-12教育中的应用：系统综述",
        "source": "Frontiers in Education",
        "date": "2025-09",
        "doi": "10.3389/feduc.2025.1647573",
        "url": "https://doi.org/10.3389/feduc.2025.1647573",
        "oa": "是（CC BY许可）",
        "tags": "生成式AI、ChatGPT、K-12教育、STEM、系统综述"
    },
    {
        "section": "## 🛡️ 六、AI学术诚信与检测",
        "num": 92,
        "title_en": "Online exam cheating detection and blockchain trusted deposit based on YOLOv12",
        "title_cn": "基于YOLOv12的在线考试作弊检测与区块链可信存证",
        "source": "Scientific Reports（Nature）",
        "date": "2025-09",
        "doi": "10.1038/s41598-025-18412-0",
        "url": "https://doi.org/10.1038/s41598-025-18412-0",
        "oa": "是（CC BY-NC-ND 4.0）",
        "tags": "在线考试作弊检测、YOLOv12、深度学习、区块链存证"
    },
    # 2025-10
    {
        "section": "## 🌟 九、AI素养与批判性思维",
        "num": 93,
        "title_en": "Integration of AI in STEM Education, Addressing Ethical Challenges in K-12 Settings",
        "title_cn": "AI融入STEM教育：应对K-12场景中的伦理挑战",
        "source": "arXiv预印本（arXiv:2510.19196）",
        "date": "2025-10",
        "doi": "10.48550/arXiv.2510.19196",
        "url": "https://arxiv.org/abs/2510.19196",
        "oa": "是（全平台开放获取）",
        "tags": "AI素养、K-12教育、STEM教学、算法伦理、教育公平"
    },
    {
        "section": "## 🎓 四、教师AI专业发展与课堂工具",
        "num": 94,
        "title_en": "Fostering AI literacy in pre-service teachers: impact of a training intervention on awareness, attitude and trust in AI",
        "title_cn": "培养职前教师AI素养：培训干预对AI认知、态度与信任的影响",
        "source": "Frontiers in Education",
        "date": "2025-10",
        "doi": "10.3389/feduc.2025.1668078",
        "url": "https://doi.org/10.3389/feduc.2025.1668078",
        "oa": "是（CC BY 4.0）",
        "tags": "AI素养、职前教师培训、AI认知与态度、教师培训"
    },
    # 2025-11
    {
        "section": "## 🛡️ 六、AI学术诚信与检测",
        "num": 95,
        "title_en": "Addressing student use of generative AI in schools and universities through academic integrity reporting",
        "title_cn": "通过学术诚信报告机制应对学生在校使用生成式AI问题",
        "source": "Frontiers in Education",
        "date": "2025-11",
        "doi": "10.3389/feduc.2025.1610836",
        "url": "https://doi.org/10.3389/feduc.2025.1610836",
        "oa": "是（CC BY许可）",
        "tags": "生成式AI、学术诚信报告框架（AIR六域）、K-12、高等教育"
    },
    # 2025-12
    {
        "section": "## 🌟 九、AI素养与批判性思维",
        "num": 96,
        "title_en": "Artificial Intelligence for All? Brazilian Teachers on Ethics, Equity, and the Everyday Challenges of AI in Education",
        "title_cn": "AI真的普惠所有人吗？巴西教师谈教育中的伦理、公平与AI日常挑战",
        "source": "arXiv预印本（arXiv:2512.23834）",
        "date": "2025-12",
        "doi": "10.48550/arXiv.2512.23834",
        "url": "https://arxiv.org/abs/2512.23834",
        "oa": "是（全平台开放获取）",
        "tags": "AI素养、教师培训、教育公平、伦理教育、K-12"
    },
    {
        "section": "## 🌟 九、AI素养与批判性思维",
        "num": 97,
        "title_en": "Learning Factors in AI-Augmented Education: A Comparative Study of Middle and High School Students",
        "title_cn": "AI增强教育中的学习因素：初中生与高中生比较研究",
        "source": "arXiv预印本（arXiv:2512.21246）",
        "date": "2025-12",
        "doi": "10.48550/arXiv.2512.21246",
        "url": "https://arxiv.org/abs/2512.21246",
        "oa": "是（arXiv预印本）",
        "tags": "AI教育工具、中学教育、学习动机、编程学习、认知发展"
    },
    {
        "section": "## 🌟 九、AI素养与批判性思维",
        "num": 98,
        "title_en": "Learning to Use AI for Learning: Teaching Responsible Use of AI Chatbot to K-12 Students Through an AI Literacy Module",
        "title_cn": "学会用AI学习：通过AI素养模块向K-12学生教授负责任的AI聊天机器人使用方法",
        "source": "arXiv预印本（arXiv:2508.13962）· AAAI 2026接收",
        "date": "2025-12",
        "doi": "10.48550/arXiv.2508.13962",
        "url": "https://arxiv.org/abs/2508.13962",
        "oa": "是（arXiv开放获取）",
        "tags": "AI素养、Prompt Literacy、K-12学生、大语言模型、课堂部署"
    },
    # 2026-01
    {
        "section": "## ⚖️ 八、AI教育伦理、政策与治理",
        "num": 99,
        "title_en": "Ethics and governance of generative AI in education: a systematic review on responsible adoption",
        "title_cn": "教育中生成式AI的伦理与治理：负责任采纳系统综述",
        "source": "Discover Education（Springer Nature）",
        "date": "2026-01",
        "doi": "10.1007/s44217-025-01051-y",
        "url": "https://doi.org/10.1007/s44217-025-01051-y",
        "oa": "是（CC BY-NC-ND 4.0）",
        "tags": "GenAI伦理、AI治理、负责任采纳、隐私保护、算法公平"
    },
    {
        "section": "## 🎓 四、教师AI专业发展与课堂工具",
        "num": 100,
        "title_en": "Teacher training in the age of AI: impact on AI literacy and teachers' attitudes",
        "title_cn": "AI时代教师培训：对AI素养与教师态度的影响",
        "source": "Frontiers in Education",
        "date": "2026-01",
        "doi": "10.3389/feduc.2025.1671306",
        "url": "https://doi.org/10.3389/feduc.2025.1671306",
        "oa": "是（CC BY 4.0）",
        "tags": "AI素养、教师在线培训、教师态度、教育技术整合"
    },
    {
        "section": "## 📝 七、评估与智能反馈",
        "num": 101,
        "title_en": "Stop perfecting the feedback, start supporting the uptake: rethinking AI in writing instruction",
        "title_cn": "停止追求完美的反馈，转而支持反馈的采纳——重新思考AI在写作教学中的应用",
        "source": "Frontiers in Education",
        "date": "2026-01",
        "doi": "10.3389/feduc.2026.1737037",
        "url": "https://doi.org/10.3389/feduc.2026.1737037",
        "oa": "是（CC BY 4.0）",
        "tags": "AI生成反馈、自动化写作评价（AWE）、反馈教学法、学习者采纳率"
    },
    # 2026-02
    {
        "section": "## ⚖️ 八、AI教育伦理、政策与治理",
        "num": 102,
        "title_en": "Rethinking Education Governance in the Age of AI",
        "title_cn": "AI时代教育治理的重新思考",
        "source": "Frontiers of Digital Education（Springer Nature）",
        "date": "2026-02",
        "doi": "10.1007/s44366-026-0085-z",
        "url": "https://doi.org/10.1007/s44366-026-0085-z",
        "oa": "是（CC BY 4.0）",
        "tags": "AI教育治理、混合治理模式、问责机制、数字教育政策"
    },
    {
        "section": "## 🛡️ 六、AI学术诚信与检测",
        "num": 103,
        "title_en": "Evaluating the accuracy and reliability of AI content detectors in academic contexts",
        "title_cn": "评估AI内容检测器在学术场景中的准确性与可靠性",
        "source": "International Journal for Educational Integrity（Springer）",
        "date": "2026-02",
        "doi": "10.1007/s40979-026-00213-1",
        "url": "https://doi.org/10.1007/s40979-026-00213-1",
        "oa": "是（CC BY-NC-ND 4.0）",
        "tags": "Turnitin、Originality、AI检测工具准确性、EFL学习者、公平性"
    },
    # 2026-03
    {
        "section": "## 🌐 二、生成式AI（GenAI）在K12教育中的应用",
        "num": 104,
        "title_en": "Classroom AI: large language models as grade-specific teachers",
        "title_cn": "课堂AI：大语言模型作为分级教师",
        "source": "npj Artificial Intelligence（Nature Portfolio）",
        "date": "2026-03",
        "doi": "10.1038/s44387-026-00081-7",
        "url": "https://doi.org/10.1038/s44387-026-00081-7",
        "oa": "是（CC BY-NC-ND 4.0）",
        "tags": "大语言模型（LLM）、K-12分级教学、个性化学习、教师短缺"
    },
]

with open('/workspace/knowledge/master_k12_ai_research.md', 'r') as f:
    content = f.read()

# Update date
content = content.replace('最后更新：2026-03-26', '最后更新：2026-03-26')

# Add new papers at end
new_content = content.rstrip()

# Group by section
sections_map = {}
for paper in NEW_PAPERS:
    sec = paper['section']
    if sec not in sections_map:
        sections_map[sec] = []
    sections_map[sec].append(paper)

# Add sections at the end
for sec, papers in sections_map.items():
    new_content += f'\n\n{sec}'
    for paper in papers:
        new_content += f'''
**{paper['num']}. {paper['title_en']}**
（{paper['title_cn']}）
- 来源：{paper['source']}
- 发布：{paper['date']}
- DOI：{paper['doi']}
- 链接：{paper['url']}
- 开放获取：{paper['oa']}
- 标签：{paper['tags']}
'''

# Count
entries = len(re.findall(r'^\*\*[0-9]+\.', new_content, re.MULTILINE))
print(f"Total entries after update: {entries}")

with open('/workspace/knowledge/master_k12_ai_research.md', 'w') as f:
    f.write(new_content)

print(f"✅ Master document updated! Total entries: {entries}")
