from __future__ import annotations

import re
from copy import deepcopy
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
INPUTS = {
    "SANY_America_External_Counsel_Strategic_Report_Bilingual_CP_Letterhead.docx": (
        "SANY_America_External_Counsel_Strategic_Report_Bilingual_Humanized_CP_Letterhead.docx",
        "report_a",
    ),
    "SANY_America_Two_Pillar_Compliance_Framework_CP_Letterhead.docx": (
        "SANY_America_Two_Pillar_Compliance_Framework_Humanized_CP_Letterhead.docx",
        "report_b",
    ),
}


REPORT_A = {
    "三一美国战略法律服务痛点与解决方案报告": "三一美国法律服务与风险治理建议",
    "SANY America Strategic Legal Pain Points & External Counsel Solutions": "SANY America legal priorities and proposed counsel support",
    "外部律师视角·中英文对照·内部交流稿\nExternal Counsel Perspective | Bilingual Internal Discussion Report": "供内部讨论使用，中英文对照\nBilingual internal discussion paper",
    "一、执行摘要  |  Executive Summary": "一、概览  |  Overview",
    "二、业务模式与风险形成机制  |  Business Model and Risk Formation": "二、业务概况及主要风险来源  |  Business profile and risk sources",
    "三、痛点一：法律服务碎片化  |  Pain Point 1: Fragmented Legal Service Delivery": "三、问题一：法律事项缺少统一管理  |  Issue 1: fragmented legal support",
    "四、痛点二：总部要求在美国的合法落地  |  Pain Point 2: Lawful Implementation of Headquarters Directives": "四、问题二：总部要求在美国的实施路径  |  Issue 2: implementing headquarters directives in the United States",
    "五、痛点三：经销商、质保与售后治理  |  Pain Point 3: Dealer, Warranty, and Service Governance": "五、问题三：经销商、质保及售后管理  |  Issue 3: dealer, warranty, and service management",
    "六、痛点四：产品安全与重大事故响应  |  Pain Point 4: Product Safety and Critical Incident Response": "六、问题四：产品安全与重大事故处理  |  Issue 4: product safety and serious incidents",
    "七、痛点五：举报、舞弊与内部调查  |  Pain Point 5: Reporting, Fraud, and Internal Investigations": "七、问题五：举报、舞弊与内部调查  |  Issue 5: reporting, misconduct, and investigations",
    "八、痛点六：劳动用工与OSHA制造业风险  |  Pain Point 6: Employment and OSHA Risks": "八、问题六：劳动用工与OSHA风险  |  Issue 6: employment and OSHA matters",
    "九、痛点七：设备数据、隐私与网络安全  |  Pain Point 7: Equipment Data, Privacy, and Cybersecurity": "九、问题七：设备数据、隐私与网络安全  |  Issue 7: equipment data, privacy, and cybersecurity",
    "十、痛点八：贸易、海关、出口管制与制裁  |  Pain Point 8: Trade, Customs, Export Controls, and Sanctions": "十、问题八：贸易、海关、出口管制与制裁  |  Issue 8: trade, customs, export controls, and sanctions",
    "十一、痛点九：CFIUS与国家安全敏感性  |  Pain Point 9: CFIUS and National Security Sensitivity": "十一、问题九：CFIUS与国家安全审查  |  Issue 9: CFIUS and national security review",
    "十二、建议的双支柱法律治理框架  |  Recommended Two-Pillar Legal Governance Framework": "十二、两类治理安排  |  A two-part governance structure",
    "十三、外部总法律顾问服务模式  |  Outside General Counsel Operating Model": "十三、外部牵头律师的工作方式  |  How lead outside counsel would work",
    "十四、Cathay Praxis与亚特兰大律师的协作分工  |  Cathay Praxis and Atlanta Counsel Allocation": "十四、Cathay Praxis与亚特兰大团队的分工  |  Team roles",
    "十五、第一阶段：30日法律健康诊断  |  Phase One: 30-Day Legal Health Check": "十五、第一阶段：30日风险梳理  |  Phase one: 30-day risk review",
    "十六、第二阶段：90日重点整改  |  Phase Two: 90-Day Priority Remediation": "十六、第二阶段：90日重点工作  |  Phase two: 90-day priority work",
    "十七、如何获得三一美国的信任与支持  |  How to Earn SANY America’s Trust and Support": "十七、与管理层开展工作的原则  |  Working with management",
    "十八、与管理层交流的关键问题  |  Key Management Discussion Questions": "十八、管理层访谈重点  |  Management discussion topics",
    "十九、结论与立即行动建议  |  Conclusion and Immediate Action": "十九、建议的起步安排  |  Suggested starting point",
    "三一美国的业务已经从单一设备销售扩展至美国本地制造、零部件配送、经销商网络、长期质保、售后维修、融资支持及设备数字化管理。法律风险由此从单项合同和诉讼问题，升级为贯穿公司治理、供应链、人员、产品、数据和监管关系的系统性经营风险。": "三一美国现已覆盖本地制造、零部件配送、经销商、长期质保、售后维修、融资支持及设备数字化管理。相应的法律事项也不再局限于合同或单一争议，而是涉及公司治理、供应链、用工、产品、数据及监管关系。",
    "SANY America’s business has evolved beyond equipment sales into U.S. manufacturing, parts distribution, dealer networks, long-term warranty support, service operations, financing support, and digital equipment management. Legal exposure has therefore moved from isolated contracts and disputes to enterprise-wide operational risk spanning governance, supply chain, workforce, products, data, and regulatory relationships.": "SANY America now operates across U.S. manufacturing, parts distribution, dealer networks, warranty and service operations, financing support, and digital equipment management. Its legal work therefore extends beyond individual contracts and disputes to governance, supply chain, employment, product, data, and regulatory matters.",
    "从外部律师角度看，最大的痛点不是缺少某一份制度，而是缺少一个统一的法律风险管理中枢：总部指令如何在美国合法落地、重大事项由谁判断和升级、不同专业律师如何协调、敏感调查如何保护特权，以及管理层如何获得可以直接决策的双语法律建议。": "目前欠缺的并非某一份制度，而是统一处理法律事项的机制。该机制需要明确总部指令在美国的审查和执行路径、重大事项的升级责任、专业律师的协调方式、敏感调查中的特权安排，以及向管理层提供双语建议的方式。",
    "From outside counsel’s perspective, the principal issue is not the absence of a single policy. It is the absence of a centralized legal-risk function that determines how headquarters’ directives are lawfully implemented in the United States, who assesses and escalates material issues, how specialists are coordinated, how privilege is protected in sensitive investigations, and how management receives decision-ready bilingual advice.": "The immediate need is not another standalone policy. It is a consistent process for reviewing headquarters directives in the United States, assigning and escalating material matters, coordinating specialists, protecting privilege in sensitive investigations, and giving management clear bilingual advice.",
    "传统的“有事再找律师”模式无法处理这种联动风险。外部律师应参与制度设计、风险分诊和危机预案，而不只是事后诉讼。": "在问题发生后再分别寻找律师，难以处理这些相互关联的事项。外部律师宜在制度设计、事项分流和重大事件预案阶段介入，并在争议发生后继续提供支持。",
    "A traditional “call counsel after a problem occurs” model is inadequate for interconnected risk. Outside counsel should participate in control design, risk triage, and crisis preparedness, not only post-event litigation.": "A matter-by-matter response after an issue arises does not work well where risks overlap. Outside counsel should be involved in control design, matter triage, and serious-incident planning, as well as disputes that follow.",
    "重型机械事故可能同时涉及产品责任、OSHA、保险、经销商责任、客户合同、证据保全和媒体风险。最危险的情况不是事故本身，而是重复故障信息分散在工程、售后、经销商和总部之间，没有统一升级和法律判断。": "重型机械事故往往同时涉及产品责任、OSHA、保险、经销商责任、客户合同、证据保全和对外沟通。更需要关注的是重复故障信息分散在工程、售后、经销商和总部之间，未能及时汇总并作出法律判断。",
    "A heavy-equipment incident may simultaneously implicate product liability, OSHA, insurance, dealer responsibility, customer contracts, evidence preservation, and media exposure. The most serious risk is often not the initial incident, but fragmented information about recurring failures across engineering, service, dealers, and headquarters without unified escalation or legal assessment.": "A heavy-equipment incident can involve product liability, OSHA, insurance, dealers, customer contracts, evidence preservation, and external communications. A recurring-failure pattern may be more serious than the initial event if engineering, service, dealer, and headquarters information is not brought together for prompt legal review.",
    "建议将所有法律服务归入两个互相联动的支柱。第一支柱保护企业对外持续经营能力；第二支柱确保内部问题能够被发现、调查、问责和整改。": "可将法律工作分为两类。第一类关注可能影响持续经营的外部风险。第二类关注内部问题的发现、调查、责任落实和整改。两类工作需要相互衔接。",
    "All legal services should be organized under two connected pillars. Pillar One protects the company’s external ability to continue operating; Pillar Two ensures internal issues are detected, investigated, addressed, and remediated.": "The legal work can be organized in two connected tracks. One addresses external risks that may affect continued operations. The other covers how internal issues are identified, investigated, assigned, and remediated.",
    "Outside General Counsel并不是替代所有专业律师，而是建立一个统一的法律项目管理层。牵头律师负责识别问题、选择专业团队、控制信息和特权、整合建议、管理预算并监督整改。": "Outside General Counsel不替代专项律师。牵头律师负责统一接收事项、确定所需专业支持、管理信息和特权安排、整合意见、跟踪预算及整改。",
    "Outside General Counsel does not replace all specialists. It creates a unified legal-management layer. Lead counsel identifies issues, selects specialist teams, controls information and privilege, integrates advice, manages budgets, and oversees remediation.": "Outside General Counsel does not replace specialists. Lead counsel receives and scopes matters, brings in the right specialists, manages information and privilege, consolidates advice, tracks budget, and follows remediation through completion.",
    "第一阶段不应以全面重建制度为目标，而应快速识别最重要风险、管理层真实痛点和可在90天内落地的改进项目。": "第一阶段宜先了解主要风险、管理层实际关注事项，以及可在90天内完成的改进工作，而不宜一开始全面重建制度。",
    "Phase One should not attempt to rebuild every policy. It should quickly identify the most material risks, management’s actual pain points, and improvements that can be implemented within 90 days.": "Phase One should focus on the material risks, management’s immediate concerns, and work that can realistically be completed within 90 days. It should not begin with a wholesale policy rebuild.",
    "90日项目应优先选择管理层能够看到业务价值的事项，而非只完成政策文本。每个工作流都应包括责任人、培训、抽样测试和整改复核。": "90日工作宜优先选择与业务直接相关、能够形成实际改进的事项。每项工作应明确责任人，并配合培训、抽样检查和整改复核。",
    "The 90-day program should prioritize workstreams that demonstrate business value, not merely produce policy documents. Each workstream should include ownership, training, sample testing, and remediation validation.": "The 90-day work should focus on operational improvements rather than policy documents alone. Each workstream should have an owner, appropriate training, sample testing, and a final remediation check.",
    "三一美国管理层可能担心合规项目成本过高、妨碍业务、暴露历史问题或导致总部与美国团队关系紧张。外部律师必须用务实方式降低这些顾虑。": "管理层可能担心项目成本、业务影响、历史事项暴露，以及总部与美国团队之间的协调压力。外部律师需要先了解这些顾虑，再把工作范围、节奏和费用安排讲清楚。",
    "SANY America management may be concerned that a compliance project will be expensive, slow the business, expose historical issues, or create tension between headquarters and the U.S. team. Outside counsel must address these concerns pragmatically.": "Management may be concerned about cost, disruption to operations, historical issues, and pressure between headquarters and the U.S. team. Counsel should address those concerns directly through a clear scope, timetable, and fee approach.",
    "三一美国当前最值得外部律师抓住的机会，是帮助其把分散的风险、律师和总部要求整合为一个可持续的美国法律治理体系。最有效的切入口不是大而全的制度建设，而是30日诊断，并围绕经销商与质保、内部调查与总部接口、产品事故与数据治理形成90日可见成果。": "外部律师可先帮助三一美国把分散的风险事项、外部律师资源和总部要求放入同一管理框架。建议先完成30日风险梳理，再围绕经销商与质保、内部调查与总部接口、产品事故及数据治理推进90日重点工作。",
    "The strongest opportunity for outside counsel is to integrate SANY America’s fragmented risks, legal providers, and headquarters expectations into a sustainable U.S. legal-governance system. The most effective entry point is not an oversized compliance buildout, but a 30-day diagnostic followed by visible 90-day results in dealer and warranty governance, investigations and headquarters interface, product incidents, and data governance.": "Outside counsel can begin by bringing SANY America’s risk matters, existing legal providers, and headquarters expectations into one workable framework. A 30-day review can then identify 90-day priorities in dealer and warranty management, investigations and headquarters coordination, product incidents, and data governance.",
    "核心定位：三一美国当前最需要的，不是更多零散律师，而是一套由外部牵头律师统一协调、能够把总部要求转化为美国合规行动的法律管理机制。": "工作重点：由外部牵头律师统一协调法律事项，并将总部要求转化为符合美国法的具体安排。",
    "Core position: SANY America’s greatest need is not more fragmented legal providers, but a coordinated legal-management mechanism led by outside counsel that converts headquarters’ objectives into compliant U.S. action.": "Working focus: lead outside counsel should coordinate legal matters and translate headquarters objectives into practical steps that comply with U.S. law.",
    "建议将服务目标定义为：帮助三一美国建立一套符合美国法律与商业实践、可以持续运行的合规经营系统。": "工作目标：协助三一美国形成符合美国法律和商业实践、能够长期执行的合规管理安排。",
    "Recommended objective: help SANY America build a sustainable operating and compliance system aligned with U.S. law and commercial practice.": "Working objective: help SANY America put in place compliance arrangements that fit U.S. law, commercial practice, and the company’s ongoing operations.",
    "解决方案：建立Outside General Counsel模式——单一入口、风险分级、专业调配、统一报告、预算和整改跟踪。": "建议：采用Outside General Counsel模式，统一接收事项，确定风险等级和专业支持，并持续跟踪报告、预算和整改。",
    "Solution: implement an Outside General Counsel model with single intake, risk classification, specialist allocation, unified reporting, budgeting, and remediation tracking.": "Suggested approach: use an Outside General Counsel model with a single intake channel, risk classification, specialist support, regular reporting, budget tracking, and remediation follow-up.",
}


REPORT_B = {
    "三一美国双支柱合规体系建设与法律服务框架": "三一美国合规与法律服务工作框架",
    "SANY America Two-Pillar Compliance & Legal Services Framework": "SANY America compliance and legal services framework",
    "用于与亚特兰大合作律师团队的内部讨论\nInternal Working Paper for Discussion with Atlanta Co-Counsel": "供与亚特兰大合作律师团队讨论使用\nInternal paper for discussion with Atlanta co-counsel",
    "一  执行摘要  |  Executive Summary": "一  概览  |  Overview",
    "二  三一美国的业务特征与初步风险画像  |  Business Characteristics and Preliminary Risk Profile": "二  业务概况及风险来源  |  Business profile and risk sources",
    "四  第一支柱的建议交付成果  |  Recommended Pillar One Deliverables": "四  第一类工作的拟形成文件  |  Indicative first-track deliverables",
    "六  第二支柱的建议交付成果  |  Recommended Pillar Two Deliverables": "六  第二类工作的拟形成文件  |  Indicative second-track deliverables",
    "七  两大支柱的联动机制  |  How the Two Pillars Work Together": "七  两类工作的衔接  |  How the two tracks connect",
    "八  外部牵头律师的职责与服务模式  |  Role and Operating Model of Lead Outside Counsel": "八  外部牵头律师的职责  |  Role of lead outside counsel",
    "九  拟议合作分工：Cathay Praxis与亚特兰大律师团队  |  Proposed Team Allocation: Cathay Praxis and Atlanta Co-Counsel": "九  Cathay Praxis与亚特兰大团队的分工  |  Team roles",
    "十  7月28日客户会见的目标与讨论结构  |  Objectives and Structure for the July 28 Client Meeting": "十  7月28日客户会见的讨论重点  |  July 28 client meeting topics",
    "十一  如何获得三一美国的信任与支持  |  How to Earn SANY America’s Trust and Support": "十一  与管理层开展工作的原则  |  Working with management",
    "十二  建议的初步实施路线  |  Proposed Initial Implementation Roadmap": "十二  初步实施安排  |  Initial implementation plan",
    "十三  明日与亚特兰大律师团队的内部讨论提纲  |  Internal Discussion Agenda for Tomorrow’s Atlanta Counsel Call": "十三  与亚特兰大团队的内部讨论提纲  |  Internal discussion agenda with Atlanta counsel",
    "十四  7月28日建议向三一美国提出的关键问题  |  Key Questions for SANY America on July 28": "十四  7月28日拟向三一美国了解的事项  |  Matters to discuss with SANY America on July 28",
    "附录B  建议的下一步  |  Recommended Immediate Next Steps": "附录B  建议先做的事项  |  Suggested next steps",
    "三一美国作为中国跨国制造集团在美国的重要运营平台，其法律风险并非仅来自单项诉讼或合同纠纷，而是来自“跨境总部管理、美国本地制造与销售、经销商网络、产品安全、员工管理、技术与数据流动以及政府监管”相互交织的经营结构。因此，法律服务应当由零散、被动的事项处理，转向由外部总法律顾问牵头的系统化风险治理。": "三一美国的法律事项既包括合同和争议，也涉及跨境总部管理、本地制造和销售、经销商网络、产品安全、用工、技术和数据流动及监管要求。法律支持需要覆盖这些相互关联的事项，并由牵头律师统筹安排。",
    "As a major U.S. operating platform of a Chinese multinational manufacturer, SANY America’s legal exposure does not arise solely from isolated disputes or contracts. It is created by the interaction of headquarters-driven cross-border management, U.S. manufacturing and sales, dealer networks, product safety, workforce management, technology and data flows, and regulatory oversight. Legal services should therefore move from fragmented and reactive matter handling to a structured risk-governance model led by Outside General Counsel.": "SANY America’s legal work includes contracts and disputes, but it also involves cross-border headquarters management, U.S. manufacturing and sales, dealers, product safety, employment, technology and data, and regulatory matters. These issues overlap and should be coordinated by lead outside counsel.",
    "建议建立“双支柱”体系：第一支柱为对外经营与持续经营合规，重点防止公司触碰可能引发刑事调查、重大行政执法、交易禁止、市场准入受限、巨额罚款、产品召回或严重声誉损失的法律红线；第二支柱为内部治理与运营合规，通过权责分配、政策制度、举报调查、问责整改、培训监测和总部—美国子公司协调机制，把风险尽可能在公司内部发现并解决。": "可将工作分为两类。第一类关注可能影响持续经营的外部合规风险，例如刑事调查、重大行政执法、交易限制、市场准入问题、罚款或产品召回。第二类关注内部治理，包括权责、制度、举报和调查、整改、培训及总部与美国子公司的协调。",
    "The recommended model has two pillars. Pillar One addresses external business and enterprise-level compliance risks that may trigger criminal investigation, significant regulatory enforcement, transaction prohibitions, market-access restrictions, substantial penalties, product recalls, or major reputational harm. Pillar Two addresses internal governance and operational compliance through clear authority, policies, reporting and investigations, accountability and remediation, training and monitoring, and a workable headquarters–U.S. subsidiary coordination mechanism.": "The work can be divided into two tracks. The first addresses external compliance risks that may affect continued operations, including criminal investigations, material enforcement, transaction restrictions, market-access issues, penalties, or recalls. The second covers internal governance: authority, policies, reporting and investigations, remediation, training, monitoring, and headquarters-U.S. coordination.",
    "外部牵头律师的核心价值，不只是回答“美国法律是否允许”，而是把总部的管理目标、三一美国的业务现实和美国律师团队的专业服务转换为可执行的工作流：明确风险、确定优先级、组织专业分工、保护律师—客户特权、形成管理层可作出决定的法律建议，并持续监督整改。": "外部牵头律师需要把总部的管理目标、三一美国的业务情况和美国法律要求放在同一方案中处理。具体工作包括明确风险和优先级、协调专业律师、安排特权保护，并向管理层提供可执行的建议和后续整改安排。",
    "The lead outside counsel’s value is not limited to answering whether U.S. law permits a proposed action. The role is to translate headquarters’ objectives, SANY America’s operational realities, and the U.S. legal team’s specialized advice into executable workstreams: identify risks, set priorities, coordinate specialists, preserve attorney-client privilege, deliver decision-ready advice to management, and oversee remediation.": "Lead outside counsel should bring headquarters objectives, SANY America’s operations, and U.S. legal requirements into one workable plan. The work includes setting priorities, coordinating specialists, protecting privilege, advising management, and following remediation.",
    "本支柱关注公司与政府、市场、客户、经销商、供应商和公众之间的法律关系，目标是识别可能影响三一美国持续经营能力的重大风险。其特点是影响范围大、监管机关多、事件处理时间短、可能涉及刑事或强制执法，并常常需要在律师—客户特权下开展快速内部调查。": "这一类工作涉及公司与监管机关、客户、经销商、供应商和公众之间的法律关系。需要优先识别可能影响持续经营的事项。此类问题通常涉及多个监管机关、较短的响应期限，并可能需要在律师主导下迅速开展内部调查。",
    "This pillar addresses SANY America’s legal relationship with regulators, markets, customers, dealers, suppliers, and the public. The objective is to identify material risks that could affect the company’s ability to continue operating. These matters often involve multiple regulators, compressed response times, potential criminal or compulsory enforcement, and rapid internal investigations conducted under attorney-client privilege.": "This track covers the company’s legal relationship with regulators, customers, dealers, suppliers, and the public. It should identify matters that may affect continued operations. These matters can involve several regulators, short response deadlines, potential enforcement, and prompt internal investigations under privilege.",
    "本支柱解决公司内部“谁决定、谁审核、谁执行、谁监督、出现问题后谁调查和问责”的问题。其目标不是将总部制度机械翻译到美国，而是把总部的合理管理要求转化为符合美国公司法、劳动法、证据规则、律师职业规范和本地商业习惯的可执行体系。": "这一类工作需要明确公司内部的决策、审核、执行和监督责任，以及问题发生后的调查和问责安排。总部制度需要结合美国公司法、劳动法、证据规则、律师职业规范和当地商业实践作出调整后实施。",
    "This pillar addresses who decides, who reviews, who executes, who oversees, and who investigates and imposes accountability when problems arise. The objective is not to mechanically translate headquarters policies into English, but to convert legitimate management expectations into a workable U.S. system consistent with corporate law, employment law, evidentiary rules, legal ethics, and local business practices.": "This track clarifies decision-making, review, execution, oversight, and investigation responsibilities inside the company. Headquarters policies should be adapted for U.S. corporate and employment law, evidentiary rules, legal ethics, and local business practice before implementation.",
    "由牵头律师统一接收总部及三一美国的需求，识别真实法律问题，避免客户在不同律师之间重复解释或收到相互冲突的建议。": "牵头律师统一接收总部和三一美国的需求，先厘清事实和法律问题，再协调相应律师参与。这样可以减少重复沟通，也便于形成一致建议。",
    "The lead counsel receives requests from headquarters and SANY America, identifies the actual legal issue, and prevents duplicative explanations or conflicting advice from multiple lawyers.": "Lead counsel receives requests from headquarters and SANY America, clarifies the facts and legal issue, and coordinates the lawyers needed for the matter. This reduces repeated explanations and supports consistent advice.",
    "把总部目标转化为美国律师可处理的问题，也把美国法律意见转化为总部和美国管理层能够执行的方案。": "牵头律师应把总部目标拆分为美国法下可审查的问题，并把法律意见说明为总部和美国管理层能够执行的安排。",
    "Translate headquarters’ objectives into issues U.S. counsel can address, and translate U.S. legal advice into plans that headquarters and U.S. management can implement.": "Lead counsel should frame headquarters objectives as questions that U.S. counsel can assess, then explain the resulting advice in terms that headquarters and U.S. management can implement.",
    "不仅提出风险，也协助责任部门落实整改，并为CEO、董事会或总部提供可决策的定期报告。": "除提示风险外，牵头律师还应协助责任部门落实整改，并向CEO、董事会或总部提供定期报告，说明已完成事项、待决事项和需要决策的事项。",
    "Go beyond identifying risk by supporting remediation and providing decision-ready periodic reporting to the CEO, board, or headquarters.": "In addition to identifying risk, lead counsel should support remediation and provide periodic reports to the CEO, board, or headquarters that distinguish completed work, open items, and decisions required.",
    "获得信任的关键不是证明我们懂所有法律，而是证明我们理解三一的业务、总部逻辑和美国执行难点。": "建立信任取决于是否理解三一的业务、总部的管理目标以及美国执行中的实际限制。",
    "Trust will not come from claiming mastery of every law; it will come from demonstrating understanding of SANY’s business, headquarters logic, and U.S. implementation challenges.": "Trust depends on a practical understanding of SANY’s business, headquarters objectives, and the constraints that apply in the United States.",
    "建议向客户提出：先批准有限范围的第一阶段项目，以事实和成果建立信任，再逐步转入长期Outside General Counsel关系。": "可先由客户批准范围有限的第一阶段工作。在掌握事实并完成约定成果后，再根据实际需要讨论长期Outside General Counsel安排。",
    "Recommended client proposal: approve a limited Phase One project first, build trust through facts and results, and then transition into a long-term Outside General Counsel relationship.": "The client could begin with a limited Phase One engagement. After the facts are understood and the agreed work is completed, the parties can consider a longer-term Outside General Counsel arrangement if needed.",
    "三一美国外部总法律顾问与合规体系建设初步讨论稿": "三一美国外部总法律顾问及合规工作内部讨论稿",
    "Preliminary Outside General Counsel and Compliance Transformation Discussion Draft": "Internal discussion draft on outside counsel and compliance work",
    "对外经营与重大监管合规；内部治理与运营合规；合作分工与客户沟通": "对外经营和重大监管事项；内部治理和运营合规；团队分工及客户沟通",
    "External regulatory compliance; internal governance; team coordination and client strategy": "External regulatory matters; internal governance; team roles and client communication",
    "1. 先听取管理层对当前痛点、总部要求、既往事件和优先事项的说明，不急于推销完整产品。": "1. 先了解管理层目前关注的事项、总部要求、既往事件和工作优先级，再讨论适合的服务范围。",
    "1. Begin by listening to management’s current pain points, headquarters expectations, prior incidents, and priorities rather than immediately selling a complete program.": "1. Begin by understanding management’s current issues, headquarters expectations, prior incidents, and priorities, then discuss an appropriate scope of support.",
    "2. 以“双支柱”解释我们理解的需求：持续经营型重大风险与内部治理型日常风险。": "2. 可将需求区分为两类：可能影响持续经营的重大风险，以及内部治理和日常运营风险。",
    "2. Explain the client’s needs through the two-pillar model: enterprise-level external risks and internal governance risks.": "2. Discuss the work in two categories: external risks that may affect continued operations and internal governance risks.",
    "3. 展示团队组合而非单一律师能力：跨境牵头、美国本地深度、专项资源和制造业经验。": "3. 说明团队的协作方式，包括跨境协调、美国本地支持、专项律师资源和制造业经验。",
    "3. Present a coordinated team rather than individual lawyers: cross-border leadership, local U.S. depth, specialist resources, and manufacturing experience.": "3. Explain how the team would work together: cross-border coordination, U.S. local support, specialist resources, and manufacturing experience.",
    "4. 提出分阶段方案：先做风险评估与优先事项，再形成制度、调查、培训和长期顾问工作流。": "4. 建议先完成风险梳理和优先级排序，再根据需要推进制度、调查、培训和持续顾问工作。",
    "4. Propose a phased plan: risk assessment and prioritization first, followed by policies, investigations, training, and an ongoing counsel workflow.": "4. Start with risk review and prioritization, then develop policies, investigations, training, and ongoing counsel support as needed.",
    "5. 明确项目不等于机械照搬总部制度，而是把总部目标转化为美国合法、可执行、可审计的治理措施。": "5. 说明总部制度需要结合美国法和当地实际调整后实施，不能直接照搬。",
    "5. Clarify that the project is not a mechanical transplantation of headquarters policies, but a conversion of legitimate objectives into lawful, workable, and auditable U.S. controls.": "5. Explain that headquarters policies need to be adapted for U.S. law and local operations rather than adopted without adjustment.",
    "6. 会后形成30日行动清单、资料需求清单、建议范围和预算框架。": "6. 会后形成30日工作清单、资料需求、建议范围和预算框架。",
    "6. After the meeting, deliver a 30-day action list, document request, proposed scope, and budget framework.": "6. After the meeting, prepare a 30-day work list, document request, proposed scope, and budget framework.",
}


GLOBAL_REPLACEMENTS = {
    "Pain Point": "Key Issue",
    "pain points": "current issues",
    "Top Pain Points": "Priority Issues",
    "Two-Pillar": "Two-Part",
    "two-pillar": "two-part",
    "two pillars": "two tracks",
    "痛点": "重点问题",
    "解决方案：": "建议：",
    "Solution:": "Recommended approach:",
    "建议成果": "拟形成文件",
    "Recommended Deliverable": "Indicative deliverable",
    "Immediate Action": "Suggested next steps",
    "Proposed Allocation": "Team roles",
    "Client Meeting Strategy": "Meeting approach",
    "Recommended Model": "Working model",
    "Initial Horizon": "Initial timetable",
    "Recommended Process": "Suggested process",
    "Recommended Action": "Suggested action",
    "Recommended Project": "Suggested project",
}


def iter_paragraphs(document):
    for paragraph in document.paragraphs:
        yield paragraph

    def visit_table(table):
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    yield paragraph
                for nested_table in cell.tables:
                    yield from visit_table(nested_table)

    for table in document.tables:
        yield from visit_table(table)


def set_paragraph_text(paragraph, value: str) -> None:
    """Replace paragraph text while retaining paragraph properties and run style."""
    run_properties = deepcopy(paragraph.runs[0]._r.rPr) if paragraph.runs else None
    paragraph._p.clear_content()
    run = paragraph.add_run(value)
    if run_properties is not None:
        run._r.insert(0, run_properties)


def normalize_humanizer_patterns(text: str) -> str:
    """Apply only the humanizer rules compatible with formal legal writing."""
    for old, new in GLOBAL_REPLACEMENTS.items():
        text = text.replace(old, new)
    text = text.replace("——", "：")
    text = text.replace("—", ", ")
    text = re.sub(r"（([^（）]+)）", r"，\1", text)
    text = re.sub(r"\(([^()]+)\)", r", \1", text)
    text = text.replace("？", "。")
    text = text.replace("?", ".")
    return re.sub(r"\s{2,}", " ", text).strip()


def humanize(source: Path, target: Path, replacements: dict[str, str]) -> int:
    document = Document(source)
    changes = 0
    for paragraph in iter_paragraphs(document):
        original = paragraph.text
        if not original:
            continue
        revised = replacements.get(original, original)
        revised = normalize_humanizer_patterns(revised)
        if revised != original:
            set_paragraph_text(paragraph, revised)
            changes += 1
    document.save(target)
    return changes


def main() -> None:
    deliverables = ROOT / "deliverables"
    results = []
    for source_name, output_info in INPUTS.items():
        output_name, key = output_info
        changes = humanize(
            deliverables / source_name,
            deliverables / output_name,
            REPORT_A if key == "report_a" else REPORT_B,
        )
        if changes < 25:
            raise RuntimeError(f"Too few humanizing edits in {output_name}: {changes}")
        results.append((output_name, changes))
    for output_name, changes in results:
        print(f"Created {output_name} with {changes} revised text blocks")


if __name__ == "__main__":
    main()
