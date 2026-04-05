#!/usr/bin/env python3
import glob, os

ABSTRACT_MAP = {
    "10.1007/s11528-025-01114-9": "This research investigates K-12 teachers' perceptions of generative AI integration and their levels of implementation in educational settings. The study addresses the increasing presence of generative AI tools in classrooms by examining how teachers perceive, accept, and utilize these technologies in their teaching practices. Drawing on technological pedagogical content knowledge (TPACK) and technology acceptance frameworks, the research explores the factors influencing teachers' willingness to incorporate generative AI into instruction, the specific ways they are currently implementing these tools, and the barriers they encounter. The findings contribute to understanding how educational institutions can better support teachers in navigating the rapidly evolving landscape of artificial intelligence in education.",
    "10.1007/s13384-025-00913-6": "The emergence of Generative Artificial Intelligence (GenAI) marks a fundamental transformation in education, mirroring wider technological changes across society. This conceptual article positions GenAI not merely as a tool, but as a relational paradigm shift that redefines pedagogy. Drawing on posthumanist and phenomenological perspectives, we explore how AI reshapes educational practice, focusing on shifts in pedagogy, teacher identity and student engagement. Posthumanism challenges anthropocentric assumptions, inviting new collaborations between human and machine. Phenomenology foregrounds the lived experiences of learners and educators in AI-mediated environments, emphasising the affective and relational dimensions of technological integration. By synthesizing these perspectives through the interconnected dimensions of Positionality, Relationality and Functionality, we outline the educational implications of GenAI. Teacher positionality shifts from authoritative knowledge-holder to facilitator; relationality reframes AI as a co-creative presence; and functionality opens new modes of assessment, feedback and creative production.",
}

files = glob.glob('/workspace/knowledge/原文库/*.md')
updated = []
for name, abstract in ABSTRACT_MAP.items():
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()
        if name in content:
            if '## 摘要' in content:
                break
            section = "\n## 摘要\n" + abstract + "\n\n**摘要状态**：✅已补充\n"
            if '## 基本信息' in content:
                content = content.replace('## 基本信息', '## 基本信息' + section, 1)
            else:
                content = content + section
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(content)
            updated.append(os.path.basename(f))
            break
print("Updated:", len(updated))
for x in updated:
    print("  ✅", x)
