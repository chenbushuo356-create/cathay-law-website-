from __future__ import annotations

import re
from copy import deepcopy
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
DELIVERABLES = ROOT / "deliverables"


REPORT_A = {
    "三一美国法律服务与风险治理建议": "三一美国法律风险治理及外部法律顾问服务建议",
    "SANY America legal priorities and proposed counsel support": "SANY America Legal Risk Management and Proposed Outside Counsel Support",
    "一、概览 | Overview": "一、执行摘要 | Executive Summary",
    "三、问题一：法律事项缺少统一管理 | Issue 1: fragmented legal support": "三、问题一：法律事项缺少统一管理 | Issue 1: Fragmented Legal Support",
    "四、问题二：总部要求在美国的实施路径 | Issue 2: implementing headquarters directives in the United States": "四、问题二：总部要求在美国的实施路径 | Issue 2: Implementation of Headquarters Directives in the United States",
    "五、问题三：经销商、质保及售后管理 | Issue 3: dealer, warranty, and service management": "五、问题三：经销商、质保及售后管理 | Issue 3: Dealer, Warranty, and Service Management",
    "六、问题四：产品安全与重大事故处理 | Issue 4: product safety and serious incidents": "六、问题四：产品安全与重大事故处理 | Issue 4: Product Safety and Serious-Incident Response",
    "七、问题五：举报、舞弊与内部调查 | Issue 5: reporting, misconduct, and investigations": "七、问题五：举报、舞弊与内部调查 | Issue 5: Reporting, Misconduct, and Internal Investigations",
    "八、问题六：劳动用工与OSHA风险 | Issue 6: employment and OSHA matters": "八、问题六：劳动用工与OSHA风险 | Issue 6: Employment and OSHA Matters",
    "九、问题七：设备数据、隐私与网络安全 | Issue 7: equipment data, privacy, and cybersecurity": "九、问题七：设备数据、隐私与网络安全 | Issue 7: Equipment Data, Privacy, and Cybersecurity",
    "十、问题八：贸易、海关、出口管制与制裁 | Issue 8: trade, customs, export controls, and sanctions": "十、问题八：贸易、海关、出口管制与制裁 | Issue 8: Trade, Customs, Export Controls, and Economic Sanctions",
    "十一、问题九：CFIUS与国家安全审查 | Issue 9: CFIUS and national security review": "十一、问题九：CFIUS与国家安全审查 | Issue 9: CFIUS and National-Security Review",
    "十三、外部牵头律师的工作方式 | How lead outside counsel would work": "十三、外部牵头律师的工作方式 | Role of Lead Outside Counsel",
    "十四、Cathay Praxis与亚特兰大团队的分工 | Team roles": "十四、Cathay Praxis与亚特兰大团队的分工 | Allocation of Responsibilities",
    "十五、第一阶段：30日风险梳理 | Phase one: 30-day risk review": "十五、第一阶段：30日风险梳理 | Phase One: 30-Day Risk Review",
    "十六、第二阶段：90日重点工作 | Phase two: 90-day priority work": "十六、第二阶段：90日重点工作 | Phase Two: 90-Day Priority Work",
    "十七、与管理层开展工作的原则 | Working with management": "十七、与管理层开展工作的原则 | Principles for Engagement with Management",
    "十八、管理层访谈重点 | Management discussion topics": "十八、管理层访谈重点 | Management Interview Topics",
    "十九、建议的起步安排 | Suggested starting point": "十九、建议的起步安排 | Proposed Initial Scope of Work",
    "Legal Hold：在诉讼、调查或索赔可合理预见时暂停删除并保存相关资料。": "Legal Hold：在诉讼、政府调查或索赔可合理预见时，暂停删除并保存相关资料。",
    "Legal Hold: preservation instruction suspending deletion when litigation, investigation, or claims are reasonably anticipated.": "Legal Hold: written preservation instruction suspending deletion of relevant materials when litigation, a government investigation, or claims are reasonably anticipated.",
    "Upjohn Warning：公司律师访谈员工时说明律师代表公司，公司控制特权。": "Upjohn Warning：公司律师访谈员工时，应明确说明律师代表公司而非受访员工个人；相关特权属于公司，并由公司决定是否主张或放弃。",
    "Upjohn Warning: notice that company counsel represents the company and the company controls privilege.": "Upjohn Warning: notice in an employee interview that company counsel represents the company, not the employee; the privilege belongs to and may be waived by the company.",
    "OSHA：美国职业安全与健康管理局，负责工作场所安全执法。": "OSHA：美国职业安全与健康管理局，隶属美国劳工部，负责工作场所安全与健康执法。",
    "OSHA: the U.S. workplace safety and health enforcement agency.": "OSHA: the U.S. Department of Labor agency responsible for workplace safety and health enforcement.",
    "CFIUS：审查特定外国投资和房地产交易国家安全风险的跨部门委员会。": "CFIUS：审查特定外国在美投资及特定外国人不动产交易国家安全影响的跨部门委员会。",
    "CFIUS: the interagency committee reviewing national-security risks of certain foreign investments and real-estate transactions.": "CFIUS: the interagency committee authorized to review certain transactions involving foreign investment in the United States and certain real-estate transactions by foreign persons for national-security purposes.",
}


REPORT_B = {
    "SANY America compliance and legal services framework": "SANY America Compliance and Legal Services Framework",
    "一 概览 | Overview": "一 执行摘要 | Executive Summary",
    "三 第一支柱：对外经营与持续经营合规 | Pillar One: External Business and Enterprise Compliance": "三 第一支柱：对外经营风险与监管合规 | Pillar One: External Business Risk and Regulatory Compliance",
    "6. OSHA职业安全与重大事故 | OSHA, Workplace Safety, and Serious Incidents": "6. 职业安全与健康（OSHA）及重大事故 | Occupational Safety and Health (OSHA) and Serious Incidents",
    "10. 企业犯罪、政府调查与危机响应 | Corporate Crime, Government Investigations, and Crisis Response": "10. 企业刑事风险、政府调查与危机应对 | Corporate Criminal Exposure, Government Investigations, and Crisis Response",
    "四 第一类工作的拟形成文件 | Indicative first-track deliverables": "四 第一支柱拟交付成果 | Indicative Pillar One Deliverables",
    "六 第二类工作的拟形成文件 | Indicative second-track deliverables": "六 第二支柱拟交付成果 | Indicative Pillar Two Deliverables",
    "八 外部牵头律师的职责 | Role of lead outside counsel": "八 外部牵头律师的职责 | Role of Lead Outside Counsel",
    "九 Cathay Praxis与亚特兰大团队的分工 | Team roles": "九 Cathay Praxis与亚特兰大团队的分工 | Allocation of Responsibilities",
    "十 7月28日客户会见的讨论重点 | July 28 client meeting topics": "十 7月28日客户会见的讨论重点 | Topics for Discussion at the July 28 Client Meeting",
    "十一 与管理层开展工作的原则 | Working with management": "十一 与管理层开展工作的原则 | Principles for Engagement with Management",
    "十二 初步实施安排 | Initial implementation plan": "十二 初步实施安排 | Initial Work Plan",
    "十三 与亚特兰大团队的内部讨论提纲 | Internal discussion agenda with Atlanta counsel": "十三 与亚特兰大团队的内部讨论提纲 | Internal Discussion Agenda with Atlanta Co-Counsel",
    "C. 如何展示经验与优势 | How to Present Experience and Advantages": "C. 相关经验与能力 | Relevant Experience and Capabilities",
    "十四 7月28日拟向三一美国了解的事项 | Matters to discuss with SANY America on July 28": "十四 7月28日拟向三一美国了解的事项 | Matters to Discuss with SANY America on July 28",
    "附录A 三一Ralls案与CFIUS的治理启示 | The Ralls–CFIUS Matter and Governance Lessons": "附录A Ralls Corporation案与CFIUS审查要点 | Appendix A: The Ralls Corporation Matter and CFIUS Review",
    "2012年，三一关联公司Ralls Corporation收购俄勒冈州风电项目。由于项目靠近美国海军训练设施，CFIUS认为交易可能产生国家安全风险。奥巴马总统随后依据相关法律发布命令，要求停止交易、拆除相关设备并处置项目资产。Ralls对CFIUS及总统命令提起诉讼，主张政府在未充分披露非保密依据并给予回应机会的情况下剥夺其财产权，违反宪法正当程序。": "2012年，三一关联公司Ralls Corporation收购了开发俄勒冈州风电项目的四家美国有限责任公司。由于项目靠近美国海军武器系统训练设施，CFIUS就该交易提出国家安全关切。奥巴马总统随后发布命令，禁止该交易继续进行，并要求Ralls处置项目公司、拆除风机及相关设备。Ralls就CFIUS和总统命令提起诉讼，主张政府未向其提供相关非保密材料并给予有意义的回应机会，因而违反宪法正当程序。",
    "In 2012, SANY-affiliated Ralls Corporation acquired wind-farm projects in Oregon. Because the projects were located near a U.S. Navy training facility, CFIUS concluded that the transaction could present national-security risks. President Obama issued an order requiring the transaction to cease, equipment to be removed, and the project assets to be divested. Ralls challenged CFIUS and the presidential order, arguing that the government deprived it of property without providing the unclassified basis and a meaningful opportunity to respond, in violation of constitutional due process.": "In 2012, SANY-affiliated Ralls Corporation acquired four U.S. limited liability companies developing wind-farm projects in Oregon. Because the projects were located near a U.S. Navy weapons-systems training facility, CFIUS raised national-security concerns. President Obama subsequently issued an order prohibiting the transaction and requiring Ralls to divest the project companies and remove the turbines and related equipment. Ralls challenged the CFIUS and presidential orders, alleging that the government violated constitutional due process by failing to provide the relevant unclassified materials and a meaningful opportunity to respond.",
    "2014年，美国哥伦比亚特区联邦巡回上诉法院认可Ralls对已取得财产权享有基本正当程序保护，要求政府向其提供足够的非保密依据并给予回应机会。但法院并未替代总统作出国家安全实体判断，项目最终也未恢复。该案的重要意义在于：总统和CFIUS在国家安全领域拥有极大裁量权，但程序并非完全不受司法审查。": "2014年，美国哥伦比亚特区联邦巡回上诉法院认为，Ralls就其已取得的财产权享有正当程序保障，并应获得足以说明决定依据的非保密材料及合理回应机会。法院未审查或取代总统的国家安全实体判断。该案表明，总统和CFIUS在国家安全领域拥有广泛裁量，但相关程序并非当然排除司法审查。",
    "In 2014, the U.S. Court of Appeals for the D.C. Circuit recognized that Ralls was entitled to basic due-process protection regarding property it had acquired, including sufficient disclosure of the unclassified basis and an opportunity to respond. The court did not substitute its judgment for the President’s national-security determination, and the project was not restored. The case is significant because it confirms that the President and CFIUS possess broad national-security discretion, but the process is not wholly immune from judicial review.": "In 2014, the U.S. Court of Appeals for the D.C. Circuit held that Ralls was entitled to due-process protection for property interests it had acquired, including sufficient disclosure of the unclassified basis for the action and an opportunity to respond. The court did not review or substitute its judgment for the President’s national-security determination. The case shows that the President and CFIUS have broad national-security discretion, but the related process is not categorically insulated from judicial review.",
    "对三一美国今天的直接启示是：CFIUS不是日常经营许可证，而是重大投资与国家安全敏感交易的前置风险审查。任何涉及并购、关键技术、敏感数据、基础设施或军事设施周边房地产的项目，应在签署、付款和公开宣布前由外部律师完成筛查，并在必要时设计申报、治理限制或缓解措施。": "对三一美国的直接启示是：CFIUS并非日常经营许可要求；其主要审查特定外国在美投资和特定外国人不动产交易的国家安全影响。涉及并购、关键技术、关键基础设施、敏感个人数据或军事设施周边不动产的交易，应在签署具有约束力的交易文件前完成前置筛查，并根据交易性质进一步评估是否存在申报义务、是否适宜自愿申报，以及是否需要调整交易结构、治理权利或缓解措施。",
    "The direct lesson for SANY America today is that CFIUS is not a daily operating license; it is a pre-transaction national-security review for major and sensitive investments. Any acquisition or project involving critical technology, sensitive data, infrastructure, or real estate near military facilities should be screened by outside counsel before signing, payment, or public announcement, with filings, governance limitations, or mitigation measures designed where necessary.": "The direct lesson for SANY America is that CFIUS is not a day-to-day operating-license requirement; it reviews the national-security effects of certain foreign investments in the United States and certain real-estate transactions by foreign persons. Transactions involving acquisitions, critical technologies, critical infrastructure, sensitive personal data, or real estate near military facilities should be screened before binding transaction documents are signed. The review should then assess whether a filing is mandatory, a voluntary filing is appropriate, or the transaction structure, governance rights, or mitigation measures should be considered.",
    "确认冲突检查、engagement letter、共同代理或分包安排、账单和客户信息共享方式。": "确认冲突检查、engagement letter、合作律师或分包安排、账单和客户信息共享方式。",
    "Confirm conflicts, engagement letters, joint-representation or subcontracting structure, billing, and information-sharing arrangements.": "Confirm conflicts, engagement letters, co-counsel or subcontracting arrangements, billing, and information-sharing arrangements.",
    "• 确认冲突检查、engagement letter、共同代理或分包安排、账单和客户信息共享方式。": "• 确认冲突检查、engagement letter、合作律师或分包安排、账单和客户信息共享方式。",
    "– Confirm conflicts, engagement letters, joint-representation or subcontracting structure, billing, and information-sharing arrangements.": "– Confirm conflicts, engagement letters, co-counsel or subcontracting arrangements, billing, and information-sharing arrangements.",
    "2. 总部, 美国子公司治理接口 | Headquarters–U.S. Subsidiary Governance Interface": "2. 总部—美国子公司治理接口 | Headquarters–U.S. Subsidiary Governance Interface",
    "5. 内部调查与律师, 客户特权 | Internal Investigations and Attorney-Client Privilege": "5. 内部调查与律师—客户特权 | Internal Investigations and Attorney-Client Privilege",
    "OSHA": "OSHA",
    "Occupational Safety and Health Administration": "Occupational Safety and Health Administration",
    "美国职业安全与健康管理局，隶属美国劳工部，负责工作场所安全与健康执法。": "美国职业安全与健康管理局，隶属美国劳工部，负责工作场所安全与健康执法。",
    "A U.S. Department of Labor agency responsible for workplace safety and health enforcement.": "A U.S. Department of Labor agency responsible for workplace safety and health enforcement.",
    "美国司法部，负责联邦刑事执法、企业犯罪、FCPA等事项。": "美国司法部，负责联邦刑事执法，包括企业犯罪和FCPA相关执法。",
    "The federal department responsible for criminal enforcement, including corporate crime and FCPA matters.": "The federal department responsible for federal criminal enforcement, including corporate-crime and FCPA matters.",
    "Securities and Exchange Commission": "U.S. Securities and Exchange Commission",
    "美国证券交易委员会，负责证券监管，并与DOJ共同执法FCPA会计条款等事项。": "美国证券交易委员会，负责证券监管，并对发行人的FCPA会计条款承担民事执法职责。",
    "The U.S. securities regulator, which also enforces FCPA accounting provisions with DOJ.": "The U.S. securities regulator, with civil enforcement authority over the FCPA accounting provisions applicable to issuers.",
    "美国商务部工业与安全局，负责EAR出口管制、许可、实体清单及执法。": "美国商务部工业与安全局，负责实施和执法《出口管理条例》，并管理出口许可及特定限制性名单。",
    "The Commerce Department bureau administering and enforcing the EAR, licensing, and restricted-party lists.": "The Commerce Department bureau that administers and enforces the EAR and administers export licensing and certain restricted-party lists.",
    "美国出口管理条例，监管受美国管辖的商品、软件和技术的出口、再出口及境内转移。": "美国《出口管理条例》，监管受其管辖的物项、软件和技术的出口、再出口及境内转移。",
    "U.S. regulations governing exports, reexports, and in-country transfers of covered items, software, and technology.": "U.S. regulations governing exports, reexports, and in-country transfers of items, software, and technology subject to the EAR.",
    "美国财政部海外资产控制办公室，负责经济制裁及受制裁主体清单。": "美国财政部海外资产控制办公室，负责实施和执法美国经济与贸易制裁措施，并维护相关制裁名单。",
    "The Treasury office administering U.S. economic sanctions and sanctions lists.": "The Treasury office that administers and enforces U.S. economic and trade sanctions and maintains related sanctions lists.",
    "美国《反海外腐败法》，禁止以不当利益影响外国官员，并要求特定发行人维持准确账簿和内部控制。": "美国《反海外腐败法》：其反贿赂条款禁止为获取或维持业务而向外国官员提供、承诺或授权提供不正当利益；会计条款要求发行人保持准确账簿记录并建立合理的内部会计控制制度。",
    "The U.S. anti-bribery statute prohibiting improper benefits to foreign officials and imposing books-and-records/internal-controls obligations on covered issuers.": "The U.S. statute whose anti-bribery provisions prohibit corrupt offers, payments, or authorizations to foreign officials for the purpose of obtaining or retaining business; its accounting provisions require issuers to keep accurate books and records and maintain internal accounting controls.",
    "美国外国投资委员会，审查特定外国投资、房地产和控制交易是否构成国家安全风险。": "美国外国投资委员会，审查特定外国在美投资及特定外国人不动产交易对美国国家安全的影响。",
    "An interagency committee reviewing certain foreign investments, real estate, and control transactions for national-security risk.": "An interagency committee authorized to review certain transactions involving foreign investment in the United States and certain real-estate transactions by foreign persons for national-security purposes.",
    "2018年扩大CFIUS权限的法律，覆盖部分非控制性投资和特定房地产交易。": "2018年通过、扩展CFIUS审查权限和程序的法律，覆盖部分非控制性投资及特定不动产交易。",
    "The 2018 law expanding CFIUS jurisdiction to certain non-controlling investments and real-estate transactions.": "The 2018 law that expanded CFIUS authorities and procedures, including with respect to certain non-controlling investments and real-estate transactions.",
    "Federal Trade Commission": "U.S. Federal Trade Commission",
    "美国联邦贸易委员会，涉及消费者保护、数据安全和部分竞争执法。": "美国联邦贸易委员会，负责消费者保护和竞争执法，并具有特定数据安全与隐私执法权限。",
    "The federal agency involved in consumer protection, data security, and certain competition enforcement.": "The federal agency responsible for consumer protection and competition enforcement, with certain data-security and privacy enforcement authority.",
    "Competition Law": "U.S. Antitrust Law",
    "美国反垄断法体系，主要防止固定价格、市场分割、串标和反竞争并购或排他行为。": "美国反垄断法体系，主要规制价格固定、市场分割、串通投标、反竞争并购及排他性行为。",
    "U.S. competition law addressing price fixing, market allocation, bid rigging, anticompetitive mergers, and exclusionary conduct.": "U.S. antitrust law addressing price fixing, market allocation, bid rigging, anticompetitive mergers, and exclusionary conduct.",
    "Corporate Interview Warning": "Upjohn Warning (Corporate Interview Warning)",
    "公司律师访谈员工时说明律师代表公司而非员工个人，公司决定是否放弃特权。": "公司律师访谈员工时，应明确说明律师代表公司而非受访员工个人；相关特权属于公司，并由公司决定是否主张或放弃。",
    "A warning in employee interviews that counsel represents the company, not the individual, and the company controls privilege.": "A warning in an employee interview that counsel represents the company, not the employee; the privilege belongs to and may be waived by the company.",
    "Litigation / Investigation Preservation Hold": "Legal Hold (Litigation Hold)",
    "当诉讼、调查或索赔可以合理预见时，暂停删除并保存相关纸质和电子资料。": "当诉讼、政府调查或索赔可以合理预见时，暂停删除并保存相关纸质和电子资料。",
    "A preservation instruction suspending deletion of relevant paper and electronic information when litigation, investigation, or claims are reasonably anticipated.": "A written preservation instruction suspending deletion of relevant paper and electronic information when litigation, a government investigation, or claims are reasonably anticipated.",
    "Legal Advice Privilege": "Attorney-Client Privilege",
    "Protection for confidential communications seeking or providing legal advice, subject to careful scope and waiver management.": "Protection for confidential communications between a client and counsel made for the purpose of seeking or providing legal advice, subject to applicable law and waiver principles.",
    "Attorney Work-Product Doctrine": "Attorney Work-Product Doctrine",
    "保护律师或其代理人为预期诉讼而准备的材料和分析。": "保护律师或其代理人为预期诉讼或审判而准备的材料和分析。",
    "Protection for materials and analysis prepared by or for counsel in anticipation of litigation.": "Protection for materials and analysis prepared by or for counsel in anticipation of litigation or for trial.",
    "Reporter / Informant": "Whistleblower",
    "举报涉嫌违法、欺诈、安全或其他不当行为的员工或第三方；美国法律常提供反报复保护。": "举报涉嫌违法、欺诈、安全或其他不当行为的员工或第三方；适用法律通常会提供一定的反报复保护。",
    "An employee or third party reporting suspected illegality, fraud, safety issues, or misconduct; U.S. law often provides anti-retaliation protection.": "An employee or third party reporting suspected illegality, fraud, safety issues, or misconduct; applicable law may provide anti-retaliation protection.",
    "External Lead Counsel": "Outside General Counsel",
    "以外部律师身份承担类似公司总法律顾问的持续协调、分诊、监督和管理层支持职能。": "由外部律师持续提供事项分诊、协调、监督和管理层支持的服务安排；其具体职责以委托范围为准。",
    "External counsel providing ongoing coordination, triage, oversight, and management support similar to an in-house general counsel.": "External counsel providing ongoing coordination, triage, oversight, and management support; the scope of the role depends on the engagement.",
    "Management Compliance Committee": "Compliance Steering Committee",
    "由法务、HR、财务、审计、IT和业务负责人组成的合规协调与决策机制。": "由法务、HR、财务、审计、IT和业务负责人组成的管理层合规协调与决策机制。",
    "A management committee of legal, HR, finance, audit, IT, and business leaders coordinating compliance decisions.": "A management-level committee of legal, HR, finance, audit, IT, and business leaders that coordinates compliance decisions.",
    "RCA": "Root Cause Analysis (RCA)",
}


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def iter_paragraphs(document: Document):
    for paragraph in document.paragraphs:
        yield paragraph

    def visit_table(table):
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    yield paragraph
                for nested in cell.tables:
                    yield from visit_table(nested)

    for table in document.tables:
        yield from visit_table(table)


def set_paragraph_text(paragraph, value: str) -> None:
    run_properties = deepcopy(paragraph.runs[0]._r.rPr) if paragraph.runs else None
    paragraph._p.clear_content()
    run = paragraph.add_run(value)
    if run_properties is not None:
        run._r.insert(0, run_properties)


def update(source: Path, target: Path, replacements: dict[str, str]) -> int:
    lookup = {normalized(key): value for key, value in replacements.items()}
    document = Document(source)
    changes = 0
    for paragraph in iter_paragraphs(document):
        original = paragraph.text
        revised = lookup.get(normalized(original))
        if revised is not None and revised != original:
            set_paragraph_text(paragraph, revised)
            changes += 1
    document.save(target)
    return changes


def main() -> None:
    pairs = [
        (
            "SANY_America_External_Counsel_Strategic_Report_Bilingual_Humanized_CP_Letterhead.docx",
            "SANY_America_External_Counsel_Strategic_Report_Bilingual_Legal_Terminology_Reviewed_CP_Letterhead.docx",
            REPORT_A,
        ),
        (
            "SANY_America_Two_Pillar_Compliance_Framework_Humanized_CP_Letterhead.docx",
            "SANY_America_Two_Pillar_Compliance_Framework_Legal_Terminology_Reviewed_CP_Letterhead.docx",
            REPORT_B,
        ),
    ]
    for source_name, target_name, replacements in pairs:
        count = update(DELIVERABLES / source_name, DELIVERABLES / target_name, replacements)
        if count < 5:
            raise RuntimeError(f"Too few changes in {target_name}: {count}")
        print(f"{target_name}: {count} edits")


if __name__ == "__main__":
    main()
