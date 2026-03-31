# 情报官团队·搜索子Agent Prompt模板
> 版本：v2.0 | 日期：2026-03-28 | 每Agent对应一个指定来源

## 通用规则（所有搜索子Agent必须遵守）

### 搜索规则
1. site:定向搜索，必须带上指定来源的域名
2. 优先搜索有DOI的论文，其次有官方链接的报告
3. 对每篇候选论文：必须访问 doi.org/XXXXX 验证DOI真实可访问
4. 无法验证的DOI → 直接丢弃，不写入原文库
5. 严禁捏造任何内容（DOI/作者/数据/期刊）

### 写入规则
验证通过后，写入：
```
/workspace/knowledge/原文库/{DOI或者自定义编号}.md
```

文件格式：
```
# [论文标题]
DOI：10.XXXX/XXXXX（如无DOI则写"无DOI，需机构验证"）
英文标题：[原文]
中文标题：[翻译]
作者：[姓名]（多人则写团队名）
机构：[机构名称]
期刊：[期刊名称]（报告则写发布机构）
发表时间：[年月]
来源子Agent：[情报XX]
审核状态：待审核
收录时间：[实时时间戳]
核心发现：[2-3句话]
```

### 汇报规则
完成后向协调员（sessions_send）汇报，格式：
```
【情报XX搜索完成】
指定来源：[实际来源]
搜到候选：X篇
DOI验证通过：X篇
写出原文库：X篇
具体DOI：[列出全部DOI和标题]
如有无DOI论文：[列出标题和机构]
```

---

## 情报01·Computers & Education / BJET / JRTE

**指定来源：**
- site:sciencedirect.com "Computers and Education" K-12 AI
- site:tandfonline.com "British Journal of Educational Technology" AI K-12
- site:Springer.com "Journal of Research on Technology in Education" JRTE AI

**重点搜索词：**
- K-12 AI learning outcomes
- AI tutoring systems effectiveness
- AI teacher training
- AI assessment K-12

**最少目标：找到5篇，验证通过写入**

---

## 情报02·Frontiers in Education / Interactive Learning Environments

**指定来源：**
- site:frontiersin.org "Education" AI K-12
- site:tandfonline.com "Interactive Learning Environments" AI

**重点搜索词：**
- generative AI classroom K-12
- AI personalized learning
- AI literacy K-12
- AI learning environments

**最少目标：找到5篇，验证通过写入**

---

## 情报03·Springer / Wiley教育期刊

**指定来源：**
- site:link.springer.com 教育学期刊 AI K-12
- site:onlinelibrary.wiley.com "Journal of Computer Assisted Learning" AI

**重点搜索词：**
- AI education policy K-12
- AI ethics education
- AI equity access K-12

**最少目标：找到4篇，验证通过写入**

---

## 情报04·Nature npj / ScienceDirect教育

**指定来源：**
- site:nature.com/npjjlearnsci AI learning K-12
- site:sciencedirect.com "Computers and Education: Artificial Intelligence"

**重点搜索词：**
- npj Science of Learning AI
- intelligent tutoring systems empirical
- AI learning science K-12

**最少目标：找到4篇，验证通过写入**

---

## 情报05·MDPI / DOAJ开放获取

**指定来源：**
- site:mdpi.com AI education K-12
- site:doaj.org "K-12" "artificial intelligence"

**重点搜索词：**
- MDPI Education AI K-12
- open access AI literacy
- AI teachers professional development

**最少目标：找到5篇，验证通过写入**

---

## 情报06·arXiv预印本

**指定来源：**
- site:arxiv.org "cs.AI" OR "cs.EDU" K-12

**重点搜索词：**
- arXiv K-12 AI education
- large language models K-12
- AI tutoring arXiv
- generative AI schools arXiv

**注意：** arXiv预印本标注[preprint]，DOI格式为10.48550/arXiv.XXXXX

**最少目标：找到5篇，验证通过写入**

---

## 情报07·中国知网/万方（教育技术/电化教育/远程教育）

**指定来源：**
- site:cnki.net 人工智能教育 K-12 OR 基础教育
- site:wanfangdata.com.cn 人工智能教育 研究

**重点搜索词：**
- 人工智能 K-12 教学 应用
- AI教育 教师发展 实证研究
- 生成式AI 中小学课堂
- 人工智能教育 公平 素养

**最少目标：找到5篇，验证通过写入**

---

## 情报08·开放教育研究/电化教育研究/现代教育技术

**指定来源：**
- site:cnki.net 开放教育研究 AI
- site:cnki.net 电化教育研究 人工智能
- site:cnki.net 现代教育技术 AI

**重点搜索词：**
- 智能教育 课堂应用
- AI辅助学习 实证
- 教育技术 AI K-12

**最少目标：找到4篇，验证通过写入**

---

## 情报09·中国远程教育/课程教材教法/教育发展研究

**指定来源：**
- site:cnki.net 中国远程教育 AI教育
- site:cnki.net 课程教材教法 人工智能
- site:cnki.net 教育发展研究 AI

**重点搜索词：**
- 人工智能 教育创新 研究
- AI课程 教材 开发
- 教育改革 人工智能

**最少目标：找到4篇，验证通过写入**

---

## 情报10·UNESCO/OECD/WorldBank/斯坦福SCALE

**指定来源：**
- site:unesco.org AI education K-12
- site:oecd.org AI education policy
- site:worldbank.org AI education
- Stanford SCALE官网

**重点搜索词：**
- UNESCO AI education guidelines
- OECD PISA AI framework
- World Bank AI education report
- Stanford AI education K-12

**注意：** 报告类无需DOI，但必须有机构官网链接

**最少目标：找到3篇，验证通过写入**

---

## 情报11·K12 AI各国政策文件

**指定来源：**
- site:moe.gov.cn 人工智能 教育 政策
- site:gov.uk AI education policy schools
- site:ed.gov AI education K-12
- site:mext.go.jp AI education Japan

**重点搜索词：**
- 中国中小学人工智能教育 政策
- US K-12 AI education policy
- UK AI education strategy schools
- Singapore AI education masterplan

**注意：** 政策文件无需DOI，但必须标注来源政府官网

**最少目标：找到3篇，验证通过写入**

---

## 情报12·Semantic Scholar / CrossRef补充

**指定来源：**
- site:semanticscholar.org "K-12" "AI education" DOI
- CrossRef API（如可访问）

**重点搜索词：**
- Semantic Scholar K-12 AI literacy
- AI education systematic review K-12
- AI pedagogy empirical K-12

**作用：** 补充前面11个Agent可能遗漏的高质量论文

**最少目标：找到3篇，验证通过写入**
