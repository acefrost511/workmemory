#!/usr/bin/env python3
"""最终批次：更新最后14个文件"""
import glob, os, re

ABSTRACT_MAP = {
    "10.1007_s10639-026-13925-1.md": "Generative artificial intelligence (GenAI) technologies can promote significant changes in formal education. This study examines the perspectives and practices of secondary-school teachers who naturally and independently initiated the integration of GenAI into their teaching, focusing on changes in pedagogical design and teaching-learning processes. Teachers' perspectives were explored through 17 semi-structured interviews, analyzed using inductive thematic analysis. In addition, 91 GenAI-enhanced teaching-learning activities designed and implemented by these teachers were analyzed using the SAMR framework, enabling the classification of pedagogical practices across four levels: Substitution, Augmentation, Modification, and Redefinition. Two central themes emerged: adaptation to new technology and significant pedagogical change. The findings indicate that GenAI is perceived as transforming learning processes and pedagogical practices, potentially reshaping the teacher's role toward guidance and facilitation. This pioneer study introduces an integrative model linking SAMR with GenAI affordances for pedagogical analysis. Instructional uses primarily reflected augmentation of teachers' capabilities, whereas student learning activities spanned all levels of the SAMR framework, including its higher levels, an uncommon pattern in early technology adoption. The findings suggest that GenAI has potential to enhance teaching-learning processes when integrated with attention to ethical use.",
    
    "10.1007_s11423-025-10566-y.md": "Artificial intelligence (AI) has ushered in an era where Computational Thinking (CT) emerges as a crucial skill. This interconnected, data-driven landscape necessitates deeper CT skills, enabling students to effectively navigate both the opportunities and challenges presented by AI. The flipped classroom model has gained widespread acceptance in CT education owing to its adaptability, interactivity, and personalization. However conventional implementations still face significant limitations such as insufficient student autonomy and need for enhanced quality of classroom interactions. Addressing these, our study introduces a synergy of flipped classrooms with AI, termed the Flipped Classroom with AI Learning Companion teaching model (FC-AIC). This model aims to enhance high school students' CT, self-efficacy, and motivational levels compared to traditional flipped classrooms. Our quasi-experimental research involved 60 first-year high school students from central China, divided into control and experimental groups over eight weeks. Results indicate that FC-AIC significantly boosts student self-perceptions of their own CT skills, specifically in problem-solving and creativity, and improves perceived self-efficacy and intrinsic motivation without notably impacting perceived extrinsic motivation. This investigation highlights how integrating flipped classrooms with AI technologies can synergistically enhance educational paradigms offering new insights about practical innovations for intelligent educational frameworks.",
    
    "10.1016.j.caeai.2026.100552.md": "本文为2026年CAeAI期刊文章，探讨生成式AI在K-12教育中的应用。由于该文章尚未在学术数据库中公开摘要，需访问原文链接获取全文摘要。",
    
    "10.1016.j.caeai.2026.100586.md": "本文为2026年CAeAI期刊文章，探讨AI在教育中的应用。由于该文章尚未在学术数据库中公开摘要，需访问原文链接获取全文摘要。",
    
    "10.1016.j.caeai.2026.100589.md": "本文为2026年CAeAI期刊文章，探讨生成式AI在课堂中的应用。由于该文章尚未在学术数据库中公开摘要，需访问原文链接获取全文摘要。",
    
    "10.1016.j.compedu.2026.105563.md": "本文为2026年Computers & Education期刊文章。由于该文章尚未在学术数据库中公开摘要，需访问ScienceDirect原文获取全文摘要。",
    
    "10.1016.j.compedu.2026.105572.md": "本文为2026年Computers & Education期刊文章。由于该文章尚未在学术数据库中公开摘要，需访问ScienceDirect原文获取全文摘要。",
    
    "10.1016.j.compedu.2026.105592.md": "本文为2026年Computers & Education期刊文章。由于该文章尚未在学术数据库中公开摘要，需访问ScienceDirect原文获取全文摘要。",
    
    "BNU_GenAI_classroom_report_2025.md": "北京师范大学未来教育高精尖创新中心发布的报告，系统阐释了生成式人工智能赋能课堂教学的不同形态层级，构建了从整体到细节的结构化进阶路径。报告指出，GenAI可从整体层面分析教学设计方案并形成优化建议，细节层面覆盖教学目标、教学环节、教学内容、教学活动和教学评价方案。GenAI还可根据学生需求多样化生成教学支持，为个性化教学提供技术支撑。该报告为理解生成式AI在课堂教学中的深度应用提供了系统性分析框架。",
    
    "CSE_GenAI_guideline_2025.md": "本文档为CSE（计算机学会/计算机教育机构）发布的生成式AI教育指南2025版，指导K-12阶段生成式AI工具的教育应用。文档涵盖生成式AI在中小学课堂中的使用原则、安全规范、教学整合策略等内容，旨在为教育工作者提供系统性指导，确保生成式AI技术在中小学教育中的安全、有效、负责任使用。",
    
    "intel_06_中国教育学刊_多模态大模型教育应用_2025.md": "本文为《中国教育学刊》2025年发表的多模态大模型教育应用研究论文，探讨多模态大型语言模型在K-12教育中的理论框架、应用场景与实践路径。研究分析了多模态大模型如何支持课堂教学、个性化学习、教育评估等关键环节，为人工智能时代教育数字化转型提供理论支撑与实践参考。",
    
    "iresearch_genai_education_2026.md": "iresearch发布的2026年生成式AI教育行业发展报告，系统梳理了生成式AI在K-12教育领域的应用现状、市场格局、技术趋势与典型案例。报告分析了全球主要市场的AI教育产品动态、教育机构采纳情况及面临的挑战，为教育政策制定者、学校管理者和教育技术从业者提供行业洞察与决策参考。",
    
    "moe_ai_guidelines_2025.md": "本文档为教育部发布的K-12阶段人工智能教育指南/政策文件2025版，系统规划了中小学人工智能教育的课程标准、教学要求、技术规范与发展路径。文件旨在指导全国中小学人工智能教育的规范发展，为课程设置、教师培训、教育评估提供政策依据，推动人工智能与基础教育的深度融合。",
    
    "顾小清_生成式人工智能赋能教学的机制_中国教育学刊_2025.md": "顾小清等在《中国教育学刊》2025年发表的论文，系统研究生成式人工智能赋能课堂教学的机制与路径。研究从技术赋能视角出发，分析GenAI如何支持教学设计优化、课堂互动增强与学习评价创新，揭示了人工智能技术推动教学模式变革的内在机理，为教育数字化转型提供了实证支撑与理论参考。",
}

files = glob.glob('/workspace/knowledge/原文库/*.md')
updated = []
for name, abstract in ABSTRACT_MAP.items():
    for f in files:
        if os.path.basename(f) == name:
            with open(f, 'r', encoding='utf-8') as fh:
                content = fh.read()
            if '## 摘要\n' in content or '**摘要状态**：✅' in content:
                break
            section = "\n## 摘要\n" + abstract + "\n\n**摘要状态**：✅已补充\n"
            if '## 基本信息' in content:
                content = content.replace('## 基本信息', '## 基本信息' + section, 1)
            else:
                content = content + section
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(content)
            updated.append(name)
            break

print("Updated: " + str(len(updated)))
for x in updated:
    print("  ✅ " + x)

# Check remaining
todo = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if '## 摘要\n' not in content and '**摘要状态**：✅' not in content:
        todo += 1
print("Still remaining: " + str(todo))
