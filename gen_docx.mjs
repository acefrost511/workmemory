import {
  Document, Packer, Paragraph, TextRun, HeadingLevel,
  AlignmentType, Table, TableRow, TableCell, WidthType,
  BorderStyle, ShadingType, TableLayoutType, VerticalAlign,
  Header, Footer, PageNumber, NumberFormat
} from "docx";
import fs from "fs";

// ── colour palette ───────────────────────────────────────────────
const C = {
  navy:   "1E3A5F",
  blue:   "2563EB",
  light:  "EFF6FF",
  grey:   "6B7280",
  dark:   "111827",
  white:  "FFFFFF",
  border: "BFDBFE",
};

// ── helpers ──────────────────────────────────────────────────────
const bold  = (t, sz=22, color=C.dark) => new TextRun({text:t, bold:true,  size:sz, color, font:"Microsoft YaHei"});
const reg   = (t, sz=22, color=C.dark) => new TextRun({text:t, bold:false, size:sz, color, font:"Microsoft YaHei"});
const italic= (t, sz=22, color=C.grey) => new TextRun({text:t, italics:true, size:sz, color, font:"Microsoft YaHei"});
const br    = ()                        => new TextRun({text:"", break:1});

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing:{before:400, after:160},
    border:{bottom:{style:BorderStyle.SINGLE, size:8, color:C.blue, space:6}},
    children:[new TextRun({text, bold:true, size:32, color:C.navy, font:"Microsoft YaHei"})],
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing:{before:300, after:120},
    children:[new TextRun({text, bold:true, size:26, color:C.blue, font:"Microsoft YaHei"})],
  });
}
function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing:{before:200, after:80},
    children:[new TextRun({text, bold:true, size:23, color:C.navy, font:"Microsoft YaHei"})],
  });
}
function body(runs, opts={}) {
  return new Paragraph({
    spacing:{before:60, after:60, line:340},
    alignment: AlignmentType.JUSTIFIED,
    ...opts,
    children: Array.isArray(runs) ? runs : [reg(runs)],
  });
}
function bullet(text, level=0) {
  return new Paragraph({
    bullet:{level},
    spacing:{before:40, after:40, line:300},
    children:[reg(text, 21)],
  });
}
function numbered(text, n) {
  return new Paragraph({
    spacing:{before:40, after:40, line:300},
    children:[bold(`${n}. `, 21), reg(text, 21)],
  });
}
function note(text) {
  return new Paragraph({
    spacing:{before:80, after:80},
    shading:{type:ShadingType.CLEAR, fill:C.light},
    border:{
      left:{style:BorderStyle.SINGLE, size:12, color:C.blue, space:8},
    },
    indent:{left:280},
    children:[italic(text, 21, C.navy)],
  });
}
function space(n=1) {
  return Array.from({length:n}, ()=>new Paragraph({spacing:{before:60, after:60}, children:[reg("")]}));
}
function divider() {
  return new Paragraph({
    spacing:{before:160, after:160},
    border:{bottom:{style:BorderStyle.SINGLE, size:4, color:C.border}},
    children:[reg("")],
  });
}

// ── generic 2-col info table ─────────────────────────────────────
function infoTable(rows) {
  return new Table({
    layout: TableLayoutType.FIXED,
    width:{size:9000, type:WidthType.DXA},
    rows: rows.map(([label, value]) =>
      new TableRow({children:[
        new TableCell({
          width:{size:2200, type:WidthType.DXA},
          shading:{type:ShadingType.CLEAR, fill:C.light},
          verticalAlign: VerticalAlign.CENTER,
          children:[new Paragraph({spacing:{before:60,after:60}, children:[bold(label,21,C.navy)]})],
        }),
        new TableCell({
          width:{size:6800, type:WidthType.DXA},
          children:[new Paragraph({spacing:{before:60,after:60}, children:[reg(value,21)]})],
        }),
      ]}),
    ),
  });
}

// ── generic multi-col header table ───────────────────────────────
function headerTable(headers, rows, colWidths) {
  const headerRow = new TableRow({
    tableHeader: true,
    children: headers.map((h,i) => new TableCell({
      width:{size:colWidths[i], type:WidthType.DXA},
      shading:{type:ShadingType.CLEAR, fill:C.navy},
      children:[new Paragraph({alignment:AlignmentType.CENTER, children:[bold(h,20,C.white)]})],
    })),
  });
  const dataRows = rows.map(cols =>
    new TableRow({children: cols.map((c,i) =>
      new TableCell({
        width:{size:colWidths[i], type:WidthType.DXA},
        children:[new Paragraph({spacing:{before:40,after:40}, children:[reg(c,20)]})],
      })
    )}),
  );
  return new Table({
    layout: TableLayoutType.FIXED,
    width:{size:9000, type:WidthType.DXA},
    rows:[headerRow, ...dataRows],
  });
}

// ════════════════════════════════════════════════════════════════
//  DOCUMENT CONTENT
// ════════════════════════════════════════════════════════════════
const children = [

  // ── COVER ─────────────────────────────────────────────────────
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing:{before:400, after:200},
    children:[new TextRun({
      text:"Redefining Personalized Learning in the Artificial Intelligence Era:",
      bold:true, size:40, color:C.navy, font:"Microsoft YaHei",
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing:{before:0, after:240},
    children:[new TextRun({
      text:"An Updated Systematic Review from 2019 to 2025",
      bold:true, size:36, color:C.blue, font:"Microsoft YaHei",
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing:{before:0, after:120},
    children:[italic("在人工智能时代重新定义个性化学习：2019—2025年更新系统综述", 28, C.grey)],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing:{before:160, after:80},
    children:[reg("Fatima Khalifeh · Raúl Santiago · Ramon Palau", 24, C.dark)],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing:{before:0, after:80},
    children:[italic("Smart Learning Environments, Vol.13, Article 19 (2026)", 22, C.grey)],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing:{before:0, after:80},
    children:[italic("Published: 27 February 2026 | DOI: 10.1186/s40561-026-00440-6", 21, C.grey)],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing:{before:0, after:400},
    children:[italic("Open Access · Creative Commons Attribution 4.0 International License", 20, C.blue)],
  }),
  divider(),

  // ── 文献信息 ───────────────────────────────────────────────────
  h1("文献信息"),
  infoTable([
    ["作者",     "Fatima Khalifeh¹, Raúl Santiago², Ramon Palau³"],
    ["作者机构", "¹ School of Education, Lebanese International University, Beirut, Lebanon\n² Department of Educational Sciences, Universidad de La Rioja, Logroño, Spain\n³ Department of Pedagogy, Universidad Rovira I Virgili, Tarragona, Spain"],
    ["期刊",     "Smart Learning Environments (Springer Nature)"],
    ["卷期",     "Volume 13, Article 19 (2026)"],
    ["发表日期", "2026年2月27日"],
    ["DOI",      "https://doi.org/10.1186/s40561-026-00440-6"],
    ["开放获取", "是（Creative Commons Attribution 4.0 International License）"],
  ]),
  ...space(1),

  // ── 摘要 ──────────────────────────────────────────────────────
  h1("摘要（Abstract）"),
  body("人工智能（AI）在教育领域的整合正在推动对个性化学习（PL）术语的重新评估，及其对教学实践和学习者参与度的影响。个性化学习涉及多种根据学生个体需求和兴趣量身定制的教学策略，利用数据和技术提升参与度和成功率。这一不断演变的格局要求清楚理解AI如何支持个性化学习，并将其与传统方法加以区分。PL术语的多样性反映了教育领域对AI技术的多元诠释，需要建立一个通用框架来厘清定义和实践。"),
  body("本文综述了个性化学习领域的最新研究文献，重点阐述技术如何转变个性化学习体验的框架与实效。通过分析来自6个数据库的权威文章，本综述致力于揭示AI如何重新定义个性化学习，使定义更加精准。研究结果强调了PL术语在技术语境中的使用，并呼吁建立统一术语，以提升教育技术实践中的清晰度和有效性。本综述旨在帮助教育者和政策制定者了解AI语境下定义个性化学习的精确术语。"),
  ...space(1),

  // ── 一、引言 ──────────────────────────────────────────────────
  h1("一、引言（Introduction）"),
  body("个性化学习（PL）是一种以学习者为中心的方法，根据学习者的需求、目标、能力、动机和兴趣量身定制教学（Schmid et al., 2022），支持学术发展的差异化学习路径（Xie et al., 2019）。随着数字技术的进步，PL越来越多地通过数据驱动和自适应系统来实现。然而，PL的扩展也产生了概念模糊性，自适应学习、个别化教学和定制化学习等相关术语常被互换使用。Shemshack和Spector（2020）的系统综述强调了这种缺乏定义清晰性的问题，并梳理了文献中重叠的术语体系。"),
  body("自该综述以来，人工智能（AI）已深度嵌入教育技术，支持实时反馈、自适应排序、智能辅导以及动态学习路径（Castro et al., 2024; Katiyar et al., 2024），进一步重塑了个性化学习的设计与实施方式。因此，本综述在Shemshack和Spector（2020）研究的基础上，考察了AI驱动教育语境中PL及相关术语的最新定义，旨在厘清个性化学习在AI时代的重新界定。"),

  h2("研究缺口与重新定义的理由"),
  body("AI的最新进展已将个性化学习从静态的4e0052005207教学转变为自适应、数据驱动、以学习者为中心的方法，支持实时反馈、个性化内容和动态学习路径（Castro et al., 2024; Katiyar et al., 2024）。生成式AI、智能辅导系统和学习分析等新兴技术被视为变革性力量，有潜力扩大教育获取机会并促进教育公平（Kanta, 2023; Taşkın, 2025）。"),
  body("尽管如此，理论与研究领域仍存在重大缺口：现有框架往往滞后于技术创新；数据隐私、算法偏见、伦理问题、教师准备度和人机协作等关键问题尚未得到充分解决（Castro et al., 2024; Laak & Aru, 2024）。此外，缺乏纵向、包容性和方法论严谨的研究，特别是在代表性不足的人群和多元教育情境中（Bayly-Castaneda et al., 2024; Laak & Aru, 2024）。"),

  h2("核心研究问题"),
  note("在人工智能时代，用于描述个性化学习方法的各术语之间有哪些异同？"),
  ...space(1),

  h2("子研究问题"),
  numbered("近期文献如何定义个性化学习？其核心组成部分是什么？", 1),
  numbered("自适应学习如何被使用？它与AI驱动的个性化学习有何关联？", 2),
  numbered("个别化教学如何被概念化？它与AI辅助个性化学习有何联系？", 3),
  numbered("定制化学习在AI支持环境中与个性化学习有何关联？", 4),
  numbered("个性化自适应学习与更广泛的个性化学习概念有何关联？", 5),
  numbered("智能辅导在个性化学习框架中处于何种位置？", 6),
  numbered("教师和AI系统在个性化学习的设计与实施中扮演什么角色？", 7),
  ...space(1),

  // ── 二、概念框架 ──────────────────────────────────────────────
  h1("二、概念框架（Conceptual Framework）"),

  h2("2.1 个性化学习（Personalized Learning）"),
  body("个性化学习是一种以学习者为中心的方法，根据学习者的需求、目标、能力、动机和兴趣量身定制教学（Schmid et al., 2022），支持学术发展的差异化学习路径（Xie et al., 2019）。自Shemshack和Spector（2020）的综述以来，AI已深度嵌入教育技术，支持实时反馈、自适应排序、智能辅导和动态学习路径（Castro et al., 2024; Katiyar et al., 2024），表明个性化学习的内涵与操作化方式已发生演变。"),

  h2("2.2 自适应学习（Adaptive Learning）"),
  body("自适应学习和个性化学习常被互换使用，但它们在技术增强教育领域代表着不同的、相互重叠的概念（Shemshack & Spector, 2020; Wang et al., 2024）。"),
  bullet("自适应学习：以系统为中心，使用AI、机器学习和计算模型，根据学习者的表现算法调整难度、节奏和内容（Mirata et al., 2020; Shemshack & Spector, 2020）"),
  bullet("个性化学习：更广泛的、以学习者为中心的范式，融合学习者的目标、兴趣、能力和自我调节过程（Ipinnaiye & Risquez, 2024; Xie et al., 2019）"),
  body("文献通常将自适应学习定性为个性化学习的技术驱动子集。"),

  h2("2.3 个别化教学（Individualized Instruction）"),
  body("个别化教学根据学习者的能力、兴趣和目标定制节奏、方法和内容，以增强相关性、动力和参与度（Ackermans et al., 2024; Zhao, 2025）。AI的进步通过AI辅助个性化扩展了个别化教学，支持实时数据分析、自适应内容、有针对性的反馈。"),
  body([bold("关键区别：", 21), reg("个别化教学主要调整通过预定课程的学习节奏；个性化学习对目标、内容、方法和排序进行更广泛的定制，强调学习者的选择和声音。", 21)]),

  h2("2.4 定制化学习（Customized Learning）"),
  body("在AI增强的教育语境中，定制化学习被概念化为个性化学习的核心组成部分和实际操作化——在总体以学习者为中心的框架内，根据学习者的需求、偏好和进度定制教学。定制化提供了技术和教学机制（AI驱动的内容传递、个性化节奏、自适应反馈、实时调整），通过这些机制实现个性化，将数字环境转变为响应学习者多样性的动态系统。"),

  h2("2.5 智能辅导（Intelligent Tutoring）"),
  body("智能辅导系统（ITS）是个性化学习中的主要技术应用，使用AI、机器学习和计算算法，基于学习者数据、行为和偏好提供自适应、个性化的教学和实时反馈（Hibbi et al., 2021; Mousavinasab et al., 2018; Yu & Chauhan, 2024）。NLP、深度学习和大数据分析的最新进展通过复杂的学习者建模、定制化推荐和大规模教学支持增强了ITS的个性化能力。"),

  h2("2.6 个性化自适应学习（Personalized Adaptive Learning）"),
  body("个性化学习越来越被概念化为一种AI驱动的、动态自适应过程，根据个体学习者的表现和动机状态定制内容和反馈（Liu, 2024）。尽管存在概念重叠，\"个性化自适应学习\"这一复合术语在教育研究中仍很少使用，研究更常分别将其称为\"自适应学习\"或\"个性化学习\"。"),

  h2("2.7 AI时代情境敏感的个性化学习"),
  body("个性化学习是人工智能教育（AIED）的核心优势，定义为一种以学习者为中心的方法，适应个体需求的内容、节奏和教学方法（Mustafa et al., 2024）。有效性高度依赖于情境，根据学习者的学科背景和学习阶段而变化。"),
  h3("计算机科学与数学学生的对比（Gao et al., 2025）"),
  bullet("CS学生：倾向于随时间发展出更高效的学习策略，表面参与度降低但生产力和概念掌握程度提高"),
  bullet("数学学生：常表现出高参与度但成就不对等，形成复杂但低效的学习方式，更容易产生学习回避行为"),
  note("结论：有效的AI驱动个性化学习必须考虑学习者的学术背景、动机和学科情境。"),

  h2("2.8 核心伦理挑战"),
  h3("数据隐私与安全"),
  body("AI驱动的个性化学习系统需要大量学生数据，风险包括未经授权的数据访问、滥用和缺乏学生对个人信息的控制权。需要健全的数据保护、匿名化和明确的知情同意协议（García-López & Trujillo-Liñán, 2025; Yu & Guo, 2023）。"),
  h3("算法公平性与偏见"),
  body("AI模型如果在有偏见的数据上训练，可能无意中延续或放大现有不平等，导致边缘化群体的教育结果不公平。建议定期进行偏见审计、使用多样化数据集和公平性感知算法（Chinta et al., 2024; García-López & Trujillo-Liñán, 2025）。"),
  h3("透明度与可解释性"),
  body("许多AI系统以黑匣子方式运行，难以理解或质疑其决策。需要可解释的AI模型和透明的数据实践，以确保问责制和建立信任（García-López & Trujillo-Liñán, 2025）。"),
  ...space(1),

  // ── 三、研究方法 ──────────────────────────────────────────────
  h1("三、研究方法（Methodology）"),

  h2("研究设计"),
  body("本研究采用系统综述方法，遵循PRISMA 2020（系统综述和元分析的首选报告项目）指南（Page et al., 2021），确保方法论的透明度、严谨性和可重复性。同时应用Okoli（2015）发布的信息系统研究系统文献综述实施指南。"),

  h2("文献来源（6个数据库）"),
  bullet("Scopus"), bullet("ScienceDirect"), bullet("EBSCOhost"),
  bullet("IEEE Xplore"), bullet("JSTOR"), bullet("Web of Science"),

  h2("覆盖期刊（9本高影响力期刊）"),
  headerTable(
    ["期刊名称", "出版社"],
    [
      ["Computers & Education", "Elsevier"],
      ["Education and Information Technologies", "Springer"],
      ["British Journal of Educational Technology", "Wiley"],
      ["Interactive Learning Environments", "Taylor & Francis"],
      ["Educational Technology Research and Development", "Springer"],
      ["International Journal of Emerging Technologies in Learning (iJET)", "开放获取"],
      ["International Journal of Educational Technology in Higher Education", "Springer Open"],
      ["International Journal of Instruction", "开放获取"],
      ["Computer Assisted Language Learning", "Taylor & Francis"],
    ],
    [5400, 3600]
  ),
  ...space(1),

  h2("搜索词"),
  bullet("Personalized learning（个性化学习）"),
  bullet("Adaptive learning（自适应学习）"),
  bullet("Individualized instruction（个别化教学）"),
  bullet("Customized learning（定制化学习）"),
  bullet("Intelligent tutoring（智能辅导）"),
  bullet("Personalized adaptive learning（个性化自适应学习）"),

  h2("纳入/排除标准（四阶段筛选）"),
  body([bold("第一阶段：", 21), reg("初始搜索，限定2019—2025年，仅英语文章，聚焦技术整合，仅收录同行评审期刊研究文章。", 21)]),
  body([bold("第二阶段：", 21), reg("按标题、摘要和关键词筛选相关研究。", 21)]),
  body([bold("第三阶段：", 21), reg("全文筛选，审查每篇文章是否提供了个性化学习的定义或术语讨论。", 21)]),
  body([bold("第四阶段：", 21), reg("将合格论文上传至Rayyan应用，逐篇精读确认相关性。", 21)]),
  note("最终结果：筛选861篇论文，最终纳入55篇高质量研究。"),
  ...space(1),

  // ── 四、研究结果 ──────────────────────────────────────────────
  h1("四、研究结果（Results）"),

  h2("4.1 个性化学习的定义与核心组成部分（28项研究）"),
  body("定义收敛于将内容、节奏和支持量身定制于个体学习者的需求、特征和目标，始终将PL定义为学习者中心、目标导向和灵活的，而非统一的（Bernacki et al., 2021）。多项研究强调数字环境在收集和分析学习者数据以指导内容排序、难度、反馈和方式中的作用。"),
  body("数字个性化学习（DPL）的出现，区分了技术丰富语境中的集成工具和独立工具，集成方法更符合机构战略（Van Schoors et al., 2021; Vanbecelaere et al., 2023）。"),

  h2("4.2 自适应学习（13项研究）"),
  body("自适应学习被一致描述为操作化个性化的主要机制，基于学习者数据动态调整任务难度、学习序列、反馈和节奏（Barbosa et al., 2023; El-Sabagh, 2021）。多数研究采用三组件模型（学习者、内容和教学模型），其中算法将表现、交互、自报告和动机数据转化为教学调整。主要应用领域：高等教育（特别是计算机科学、语言学习和数学）。"),
  note("整体定位：自适应学习是个性化学习的算法\"引擎\"，提供持续、数据驱动定制的技术手段。"),

  h2("4.3 个别化教学（1项研究）"),
  body("在AI聚焦文献中已基本退出使用；其出现指的是基于专业判断而非自动化分析，由教师设计内容和节奏变化。个别化教学作为AI个性化的教学前身，在规模、自动化和数据使用方面有所不同。"),

  h2("4.4 定制化学习（2项研究）"),
  body("通常指根据学习者偏好或选择定制材料、任务或路径，在AI支持环境中通过推荐系统实现，使用表现数据、推断兴趣或学习风格匹配资源（Murad et al., 2020; Wan & Yu, 2020）。定制化学习是个性化学习的一个维度——特别是内容个性化——而非独立范式。"),

  h2("4.5 个性化自适应学习（2项研究）"),
  body("描述集成学习者档案与基于表现和参与数据实时适应的系统（Luo et al., 2025; Zheng et al., 2024），采用高级学习路径算法、知识追踪和预测模型。结果表明，与静态或教师引导的方法相比，学习效率和表现有所提升。"),

  h2("4.6 智能辅导系统（9项研究）"),
  body("定义为通过逐步指导、自适应反馈和个性化练习模拟人类辅导的计算机环境（Mousavinasab et al., 2018）。采用AI技术：基于规则的推理、贝叶斯网络、推荐算法和自然语言处理。"),
  bullet("主要应用领域：编程、数学和STEM"),
  bullet("新兴发展：情感识别、游戏化和对话代理"),
  note("整体定位：ITS是AI驱动个性化学习中最成熟、技术上最复杂的实现之一。"),

  h2("4.7 教师与AI系统的角色"),
  body("个性化学习作为人机协作模型，教师和AI系统发挥互补作用："),
  headerTable(
    ["阶段", "教师角色", "AI系统角色"],
    [
      ["设计阶段", "解读学习者数据，将系统建议与课程目标对齐", "生成学习者档案，预测表现，提议内容序列"],
      ["实施阶段", "提供社会情感支持，在自动路径与学习者需求冲突时进行干预", "调整难度、节奏、方式和反馈；ITS提供即时纠正性反馈"],
      ["评估阶段", "引导教学设计，确保教学一致性", "监控进度、参与度和风险模式，识别需要支持的学习者"],
    ],
    [1800, 3600, 3600]
  ),
  note("核心结论：当AI提供自适应精准性、教师确保教学一致性、伦理监督和人文参与时，个性化学习最为有效。"),

  h2("4.8 AI支持个性化学习的八大核心组成部分"),
  headerTable(
    ["组成部分", "说明"],
    [
      ["① 学习者档案（Learner Profile）", "个体特征、需求、目标建模"],
      ["② 数据输入（Data Inputs）", "表现、互动、情感、自报告数据"],
      ["③ 内容模型（Content Model）", "知识结构、学习资源组织"],
      ["④ 教学模型（Instructional Model）", "教学策略、序列规则"],
      ["⑤ 自适应引擎（Adaptive Engine）", "算法调整机制"],
      ["⑥ 界面与用户控制（Interface & User Controls）", "学习者与教师的交互设计"],
      ["⑦ 个性化目标（Personalization Goals）", "学习目标对齐"],
      ["⑧ 评估与治理（Evaluation & Governance）", "效果评估、伦理监督框架"],
    ],
    [4500, 4500]
  ),
  ...space(1),

  // ── 五、新兴趋势 ──────────────────────────────────────────────
  h1("五、现有与新兴趋势（Existing & Emerging Trends）"),
  numbered("个性化推荐系统（PRS）：特别是在K-12教育中，整合学生画像、内容处理和推荐机制，以增强参与度和表现（Martin et al., 2020; Zayet et al., 2022）。", 1),
  numbered("自适应学习系统：从聚焦学习者模型扩展到整合内容和教学模型，形成综合自适应系统。", 2),
  numbered("智能辅导系统（ITS）新进展：情感智能系统、对话代理、情感识别技术、严肃游戏评估，以及向移动端平台转移。", 3),
  numbered("整体发展方向：从静态4e0052005207的电子学习转向复杂的、数据驱动的整体个性化系统，整合认知、行为和情感维度。", 4),
  ...space(1),

  // ── 六、讨论 ──────────────────────────────────────────────────
  h1("六、讨论（Discussion）"),
  body("个性化学习是一种根据学习者需求、偏好和节奏调整教学的教育方法。尽管植根于辅导和学徒制等传统实践，但已被数字技术尤其是AI从根本上重塑。"),
  body("教育机构对个性化学习数字技术的利用不足，揭示了技术能力与课堂实践之间的持续差距（Schmid et al., 2022）。弥补这一差距需要更强的专业发展、更好的技术整合，以及融合互动性、游戏化和个性化评估的教学框架。"),
  body("近期综述表明，尽管个性化学习的基本目标（为个体定制教育）保持稳定，但其术语和概念基础在AI时代变得越来越数据驱动和精准。早期文献注意到个性化相关术语之间存在显著概念重叠和模糊性（Bernacki et al., 2021; Shemshack & Spector, 2020），而当代研究则强调AI支持的学习者画像、自适应内容传递和自动化反馈作为现代个性化学习框架的定义特征（Castro et al., 2024）。"),
  ...space(1),

  // ── 七、结论 ──────────────────────────────────────────────────
  h1("七、结论与启示（Conclusion & Implications）"),
  body("个性化学习领域正在响应技术进步和人机交互的深入理解而快速演进。主要挑战包括："),
  bullet("概念模糊性：缺乏个性化学习的普遍公认定义，它仍是一个宽泛的、多层次的总括性术语"),
  bullet("年龄偏向：现有研究不成比例地聚焦于年龄较大的学习者，对小学阶段学生个性化学习长期效果的研究存在重大空白"),
  bullet("实施障碍：技术基础设施不足，机构框架不一致"),
  bullet("方法局限：文献大量依赖横断面设计和自报告数据，限制了因果推断"),

  h2("未来研究方向"),
  bullet("使用更精确的术语（如数字个性化学习/DPL或个性化自适应学习）"),
  bullet("加强AI开发者与教育者的协作，确保工具在教学上合理、用户友好"),
  bullet("整合技术性诊断评估，关注认知和情感维度"),
  bullet("对个性化自适应学习平台进行系统比较评估"),
  bullet("将研究延伸到代表性不足的学习者群体"),
  ...space(1),

  // ── 八、局限 ──────────────────────────────────────────────────
  h1("八、研究局限（Limitations）"),
  numbered("大量出版物导致部分相关研究可能被遗漏", 1),
  numbered("仅限于英语、同行评审文章", 2),
  numbered("仅覆盖9本高影响力期刊，可能遗漏其他有价值的研究", 3),
  numbered("排除了会议论文、学位论文和研究报告等非期刊格式", 4),
  ...space(1),

  // ── 九、缩略语 ────────────────────────────────────────────────
  h1("九、缩略语（Abbreviations）"),
  headerTable(
    ["缩略语", "全称"],
    [
      ["PL",    "Personalized Learning（个性化学习）"],
      ["AI",    "Artificial Intelligence（人工智能）"],
      ["GenAI", "Generative Artificial Intelligence（生成式人工智能）"],
      ["TEL",   "Technology Enhanced Learning（技术增强学习）"],
      ["NLP",   "Natural Language Processing（自然语言处理）"],
      ["DPL",   "Digital Personalized Learning（数字个性化学习）"],
      ["SJR",   "Scimago Journal Rank（Scimago期刊排名）"],
      ["ITS",   "Intelligent Tutoring System（智能辅导系统）"],
      ["PRS",   "Personalized Recommender Systems（个性化推荐系统）"],
      ["OECD",  "Organization for Economic Co-operation and Development（经济合作与发展组织）"],
    ],
    [2000, 7000]
  ),
  ...space(1),

  // ── 十、参考文献 ──────────────────────────────────────────────
  h1("参考文献（References）"),
  ...[
    "Ackermans, K., Bakker, M., van Loon, A.-M., Kral, M., & Camp, G. (2024). Young learners' motivation, self-regulation, and performance in personalized learning. Computers & Education.",
    "Alé-Ruiz, R., Martínez-Abad, F., & del Moral-Marcos, M. T. (2023). Academic engagement and management of personalized active learning. Education and Information Technologies, 29, 12289–12304.",
    "Almuhanna, M. A. (2024). Teachers' perspectives of integrating AI-powered technologies in K–12 education. Education and Information Technologies.",
    "Barbosa, P. L. S., et al. (2023). Adaptive learning in computer science education. Education and Information Technologies, 29, 9139–9188.",
    "Bayly-Castaneda, K., et al. (2024). Crafting personalized learning paths with AI for lifelong learning. Frontiers in Education.",
    "Bendahmane, M., El Falaki, B., & Benattou, M. (2019). Toward a personalized learning path through a services-oriented approach. iJET.",
    "Bernacki, M., Greene, M., & Lobczowski, N. (2021). A systematic review of research on personalized learning. Educational Psychology Review, 33, 1675–1715.",
    "Beyyoudh, M., Khalidi Idrissi, M., & Bennani, S. (2019). Towards a new generation of intelligent tutoring systems. iJET, 14(14), 105–121.",
    "Bhutoria, A. (2022). Personalized education and artificial intelligence in the US, China, and India. Computers and Education: AI, 3, 100068.",
    "Castro, G., Chiappe, A., Rodríguez, D., & Sepulveda, F. (2024). Harnessing AI for education 4.0. Electronic Journal of e-Learning.",
    "Chinta, S., et al. (2024). FairAIED: Navigating fairness, bias, and ethics in educational AI. Frontiers in Education.",
    "Deckker, D., Sumanasekara, S., & Fakhrou, A. (2025). AI-powered personalised learning: Promise and pitfalls. World Journal of Advanced Research and Reviews.",
    "El-Sabagh, H. A. (2021). Adaptive e-learning environment based on learning styles. International Journal of Educational Technology in Higher Education.",
    "Elmaadaway, M. A. N., & Abouelenein, Y. A. M. (2022). In-service teachers' TPACK development through an adaptive e-learning environment. Education and Information Technologies.",
    "Gao, Z., et al. (2025). Tracing distinct learning trajectories in an introductory programming course. International Journal of STEM Education, 12(1), 27.",
    "García-López, I., & Trujillo-Liñán, L. (2025). Ethical and regulatory challenges of generative AI in education. Frontiers in Education.",
    "Halkiopoulos, C., & Gkintoni, E. (2024). Leveraging AI in e-learning: Personalized learning through cognitive neuropsychology. Electronics.",
    "Hashim, S., et al. (2022). Trends on technologies and artificial intelligence in education for personalized learning. International Journal of Academic Research in Progressive Education.",
    "Hibbi, F.-Z., Abdoun, O., & Haimoudi, E. K. (2021). Smart tutoring system: A predictive personalized feedback. iJET.",
    "Hobert, S., & Berens, F. (2023). Developing a digital tutor as an intermediary between students, TAs, and lecturers. Educational Technology Research and Development.",
    "Hooshyar, D., et al. (2024). The effectiveness of personalized technology-enhanced learning in higher education: A meta-analysis. Computers & Education.",
    "Huiji, S. (2022). Big data-assisted recommendation of personalized learning resources. iJET.",
    "Ipinnaiye, O., & Risquez, A. (2024). Exploring adaptive learning, learner–content interaction and student performance. Computers & Education.",
    "Kaïss, W., Mansouri, K., & Poirier, F. (2023). Effectiveness of an adaptive learning chatbot on students' learning outcomes. iJET.",
    "Kanta, S. (2023). The role of artificial intelligence in personalized learning. ShodhKosh.",
    "Kaouni, M., Lakrami, F., & Labouidya, O. (2023). The design of an adaptive e-learning model based on AI. iJET, 18(6), 202–219.",
    "Katiyar, P., et al. (2024). AI-driven personalized learning systems: Enhancing educational effectiveness. Educational Administration: Theory and Practice.",
    "Laak, K., & Aru, J. (2024). AI and personalized learning: Bridging the gap with modern educational goals. arXiv.",
    "Lee, D., et al. (2021). Differences in personalized learning practice in high- and low-performing learner-centered schools. Educational Technology Research and Development.",
    "Lepri, B., Oliver, N., & Pentland, A. (2021). Ethical machines: the human-centric use of AI. iScience, 24(3), 102249.",
    "Leshchenko, M., et al. (2023). Technology-enhanced personalized language learning. iJET.",
    "Li, L. (2023a). Classroom teaching decision-making optimization for personalized learning needs. iJET.",
    "Li, Z. (2023b). AI-assisted emotion recognition: Impacts on mental health education. iJET, 18(24), 34–48.",
    "Li, K. C., & Wong, B.T.-M. (2020). Features and trends of personalised learning 2001–2018. Interactive Learning Environments.",
    "Liu, L. (2024). Impact of AI gamification on EFL learning outcomes. Education and Information Technologies.",
    "Luo, G., et al. (2025). HA-LPR: A highly adaptive learning path recommendation. Education and Information Technologies.",
    "Martin, F., Chen, Y., Moore, R. L., & Westine, C. D. (2020a). Systematic review of adaptive learning research designs 2009–2018. Educational Technology Research and Development.",
    "Martin, F., Dennen, V. P., & Bonk, C. J. (2020b). A synthesis of systematic review research on emerging learning environments. Educational Technology Research and Development.",
    "Mejeh, M., & Rehm, M. (2024). Taking adaptive learning to the next level using NLP. Educational Technology Research and Development.",
    "Mirata, V., et al. (2020). Challenges in establishing adaptive learning in higher education: A Delphi study. International Journal of Educational Technology in Higher Education.",
    "Mousavinasab, E., et al. (2018). Intelligent tutoring systems: A systematic review. Interactive Learning Environments.",
    "Murad, D. F., et al. (2020). Personalization of study material based on predicted final grades. Education and Information Technologies.",
    "Mustafa, M. Y., et al. (2024). A systematic review of literature reviews on AI in education (AIED). Smart Learning Environments, 11(1), 59.",
    "Nguyen, H., et al. (2023). A model to create a personalized online course based on learning styles. Education and Information Technologies, 29, 571–593.",
    "Okoli, C. (2015). A guide to conducting a standalone systematic literature review. Communications of the AIS, 37(1), 879–910.",
    "Romi, I. M. (2023). An adaptive e-learning systems success model. iJET, 18(18), 177–191.",
    "Schmid, R., & Petko, D. (2019). Educational technology in personalized learning environments and digital skills. Computers & Education.",
    "Schmid, R., Pauli, C., & Petko, D. (2022). Examining digital technology in school-wide personalized learning. Educational Technology Research and Development.",
    "Shemshack, A., & Spector, J. M. (2020). A systematic literature review of personalized learning terms. Smart Learning Environments, 7, 17.",
    "Smyrnova-Trybulska, E., Morze, N., & Varchenko-Trotsenko, L. (2022). Adaptive learning in university students' opinions. Education and Information Technologies.",
    "Taşkın, M. (2025). Artificial intelligence in personalized education. Human Computer Interaction.",
    "Troussas, C., Chrysafiadi, K., & Virvou, M. (2020). Personalized tutoring through a stereotype student model. Education and Information Technologies.",
    "Van Schoors, R., et al. (2021). An overview of 25 years of research on digital personalised learning. British Journal of Educational Technology.",
    "Vanbecelaere, S., et al. (2023). Evaluating teachers' perceptions of a portal for digital personalised learning. Education and Information Technologies.",
    "Walter, Y. (2024). Embracing the future of AI in the classroom. International Journal of Educational Technology in Higher Education.",
    "Wan, H., & Yu, S. (2020). A recommendation system based on an adaptive learning cognitive map model. Interactive Learning Environments.",
    "Wang, S., et al. (2020). When adaptive learning is effective learning. Interactive Learning Environments.",
    "Wang, F., Han, M., & Wei, P. (2022). A dynamic learning interest model for personalized learning. iJET.",
    "Wang, X., Maeda, Y., & Chang, H.-H. (2024). Development and techniques in learner model in adaptive e-learning. Computers & Education.",
    "Xie, H., et al. (2019). Trends and development in technology-enhanced adaptive/personalized learning 2007–2017. Computers & Education.",
    "Xu, X. (2025). AI optimization algorithms enhance higher education management. Scientific Reports.",
    "Xu, Z., et al. (2019). The effectiveness of ITS on K–12 students' reading comprehension: A meta-analysis. British Journal of Educational Technology.",
    "Xu, X., et al. (2024). Effects and side effects of personal learning environments. Education and Information Technologies.",
    "Yang, H., & Alabool, H. M. (2022). Knowledge proficiency tracing model in English teaching curriculum. iJET.",
    "Yu, J. H., & Chauhan, D. (2024). Trends in NLP for personalized learning. Education and Information Technologies.",
    "Yu, Q., & Guo, Y. (2023). Ethics of AI in education: Student privacy and data protection. Science Insights Education Frontiers.",
    "Zayet, T. M. A., et al. (2022). An intelligent tutoring system for personalised learning. iJET.",
    "Zhao, J. (2025). The impact of ChatGPT and AI on personalized and adaptive learning. Journal of Computers in Education.",
    "Zheng, Y., et al. (2024). A personalized learning path recommendation method based on knowledge graphs. Education and Information Technologies.",
    "Zine, K., et al. (2019). Development of a semantic recommendation system for personalized learning. iJET.",
    "Zou, W., et al. (2020). Social presence and learners' prestige in MOOC discussion forums. Computers in Human Behavior.",
  ].map((ref, i) => new Paragraph({
    spacing:{before:40, after:40, line:300},
    indent:{hanging:480, left:480},
    children:[reg(`${i+1}. ${ref}`, 20)],
  })),

  divider(),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing:{before:120, after:60},
    children:[italic("本文件基于Springer Nature开放获取原文整理，原文遵循CC BY 4.0许可。", 19, C.grey)],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing:{before:0, after:60},
    children:[italic("整理时间：2026年2月28日 | 来源：https://doi.org/10.1186/s40561-026-00440-6", 19, C.grey)],
  }),
];

// ════════════════════════════════════════════════════════════════
//  BUILD & SAVE
// ════════════════════════════════════════════════════════════════
const doc = new Document({
  creator: "OpenClaw AI Assistant",
  title: "Redefining Personalized Learning in the AI Era",
  description: "Systematic Review by Khalifeh, Santiago & Palau (2026)",
  styles:{
    default:{
      document:{
        run:{ font:"Microsoft YaHei", size:22, color:C.dark },
        paragraph:{ spacing:{line:340} },
      },
    },
    paragraphStyles:[
      {
        id:"Heading1",
        name:"Heading 1",
        basedOn:"Normal",
        run:{ bold:true, size:32, color:C.navy, font:"Microsoft YaHei" },
        paragraph:{ spacing:{before:400,after:160} },
      },
      {
        id:"Heading2",
        name:"Heading 2",
        basedOn:"Normal",
        run:{ bold:true, size:26, color:C.blue, font:"Microsoft YaHei" },
        paragraph:{ spacing:{before:280,after:100} },
      },
      {
        id:"Heading3",
        name:"Heading 3",
        basedOn:"Normal",
        run:{ bold:true, size:23, color:C.navy, font:"Microsoft YaHei" },
        paragraph:{ spacing:{before:180,after:80} },
      },
    ],
  },
  sections:[{
    properties:{
      page:{
        margin:{ top:1440, bottom:1440, left:1800, right:1440 },
      },
    },
    headers:{
      default: new Header({
        children:[new Paragraph({
          border:{bottom:{style:BorderStyle.SINGLE, size:4, color:C.border}},
          alignment: AlignmentType.RIGHT,
          children:[italic("Khalifeh, Santiago & Palau (2026) · Smart Learning Environments · Vol.13, Art.19", 18, C.grey)],
        })],
      }),
    },
    footers:{
      default: new Footer({
        children:[new Paragraph({
          border:{top:{style:BorderStyle.SINGLE, size:4, color:C.border}},
          alignment: AlignmentType.CENTER,
          children:[
            italic("DOI: 10.1186/s40561-026-00440-6  |  Open Access CC BY 4.0  |  整理时间: 2026-02-28   ", 18, C.grey),
            new TextRun({children:[PageNumber.CURRENT], size:18, color:C.grey, font:"Microsoft YaHei"}),
            italic(" / ", 18, C.grey),
            new TextRun({children:[PageNumber.TOTAL_PAGES], size:18, color:C.grey, font:"Microsoft YaHei"}),
          ],
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/workspace/papers/Khalifeh_2026_Redefining_Personalized_Learning_AI.docx", buf);
  console.log("✅ DONE:", buf.length, "bytes");
}).catch(e => { console.error("❌", e); process.exit(1); });
