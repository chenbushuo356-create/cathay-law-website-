# Cathay Praxis Law 网站内容维护指南

> 本文档记录网站各类内容对应的修改位置，便于日常维护和更新。
> 项目路径：`/Users/mima0000/Documents/CathayPraxisLaw/`

---

## 一、项目文件总览

```
CathayPraxisLaw/
├── index.html              # 首页（含所有板块结构 + 团队卡片数据）
├── news-detail.html        # 新闻详情页模板
├── insight-detail.html     # 评析详情页模板
├── team-detail.html        # 团队成员详情页
├── content.js              # 新闻/评析数据（主文件）
├── data/
│   └── content.js          # 新闻/评析数据（副本，必须与主文件同步）
├── js/
│   └── shared.js           # 中英双语翻译 + 共享功能
├── css/                    # 样式文件
└── images/                 # 图片资源
```

---

## 二、⚠️ 关键注意事项

### 1. 双文件同步（高频踩坑）
`content.js` 和 `data/content.js` **内容完全相同**。

> **规则：修改 `content.js` 后，必须同步修改 `data/content.js`。**

涉及内容：新闻（News）、评析（Insights）、分类标签定义。

### 2. 团队成员数据双源维护
团队成员信息在 **两处分别存放**，内容不同：

| 位置 | 用途 | 内容详尽程度 |
|------|------|------------|
| `index.html` 内联脚本 `teamData` | 首页团队卡片展示 | 精简（姓名、角色、头像、摘要） |
| `team-detail.html` 内联脚本 `teamMembers` | 成员详情页展示 | 完整（履历、执业领域、代表业绩、教育背景等） |

> **规则：新增/修改成员时，两处必须同步更新。**

---

## 三、按内容类型 → 文件映射

### 网站名称 / 品牌 / 版权
| 修改内容 | 目标文件 |
|---------|---------|
| 浏览器标签页标题 | `index.html`、`news-detail.html`、`insight-detail.html` 的 `<title>` 标签 |
| 首页 Hero 描述 | `index.html`（硬编码）+ `js/shared.js` 中 `hero_desc` 翻译键 |
| 页脚版权信息 | 所有 `.html` 文件的 footer 段落 |
| 动态标题（JS 生成）| `news-detail.html`、`insight-detail.html` 的 `document.title` 脚本 |
| 业绩展示中的律所名称 | `content.js` + `data/content.js` 中相关条目 |

### 业务领域（Practice Areas）
| 修改内容 | 目标文件 |
|---------|---------|
| 5 个业务卡片（标题 + 描述）| `index.html` Practice 板块（硬编码 HTML）|
| 中英翻译 | `js/shared.js` 中 `practice_1_title` ~ `practice_5_desc` |

### 客户与行业（Clients & Industries）
| 修改内容 | 目标文件 |
|---------|---------|
| 4 类客户描述 | `index.html` Clients 板块（硬编码 HTML）|
| 4 个行业领域（标题 + 描述）| `index.html` Clients 板块（硬编码 HTML）|
| 中英翻译 | `js/shared.js` 中 `client_1` ~ `industry_4_desc` |

### 新闻（News）
| 修改内容 | 目标文件 |
|---------|---------|
| 添加 / 修改 / 删除新闻 | `content.js` + `data/content.js` 中 `newsData` 数组 |
| 分类标签名称 | `content.js` + `data/content.js` 中 `categoryDefinitions.news` |
| 详情页样式 | `news-detail.html` |

**单条新闻数据结构：**
```javascript
{
    id: 'news-001',
    slug: 'bis-entity-list-update-april-2026',  // URL 参数，必须唯一
    date: '2026-04-10',
    category: 'policy',  // 可选：policy / industry / achievement / case
    image: '...',
    title: { en: '...', zh: '...' },
    excerpt: { en: '...', zh: '...' },
    content: { en: 'HTML...', zh: 'HTML...' }  // 完整正文
}
```

### 评析 / Insights
| 修改内容 | 目标文件 |
|---------|---------|
| 添加 / 修改 / 删除评析 | `content.js` + `data/content.js` 中 `insightsData` 数组 |
| 分类标签名称 | `content.js` + `data/content.js` 中 `categoryDefinitions.insights` |
| 详情页样式 | `insight-detail.html` |

> 数据结构与新闻相同。

### 团队成员
| 修改内容 | 目标文件 |
|---------|---------|
| 首页卡片（姓名、角色、头像、摘要）| `index.html` 内联脚本 `teamData`（约第 939 行起）|
| 详情页完整履历 | `team-detail.html` 内联脚本 `teamMembers`（约第 264 行起）|
| 团队板块描述 | `js/shared.js` 中 `team_desc` 翻译键 |

### 关于我们（About）
| 修改内容 | 目标文件 |
|---------|---------|
| 标题和描述 | `index.html` About 板块（硬编码）|
| 三个价值观卡片 | `index.html` About 板块（硬编码）|
| 中英翻译 | `js/shared.js` 中 `about_title`、`value_X_title` 等 |

### 联系我们（Contact）
| 修改内容 | 目标文件 |
|---------|---------|
| 联系描述 | `index.html` Contact 板块（硬编码）|
| 办公地址 | `index.html` Contact 板块（硬编码）|
| 电话 / 邮箱 | `index.html` top-contact-bar + Contact 板块（两处）|
| 中英翻译 | `js/shared.js` 中 `contact_desc`、`office_ca` 等 |

### 导航与通用 UI
| 修改内容 | 目标文件 |
|---------|---------|
| 导航菜单项 | `js/shared.js` 中 `nav_home`、`nav_about` 等（影响桌面端 + 移动端）|
| 按钮文字 | `js/shared.js` 中对应翻译键 |
| Hero 轮播标题 | `js/shared.js` 中 `hero_title_1`、`hero_title_2_prefix` 等 |

---

## 四、常见操作速查

### 添加一篇新闻
1. 在 `content.js` 的 `newsData` 数组末尾添加新条目
2. 在 `data/content.js` 的 `newsData` 数组末尾**同步添加相同内容**
3. 确保 `slug` 字段唯一，用作详情页 URL 参数

### 修改团队成员信息
1. 修改 `index.html` 内联脚本中 `teamData` 对应成员字段
2. 修改 `team-detail.html` 内联脚本中 `teamMembers` 对应成员字段
3. 如更换头像，更新 `image` 路径并将新图片放入 `images/` 目录

### 修改业务领域描述
1. 修改 `index.html` Practice 板块中的硬编码 HTML
2. 修改 `js/shared.js` 中对应的翻译键

### 修改网站名称（如 LLP → PC）
1. 修改所有 `.html` 文件的 `<title>`、footer 版权
2. 修改 `news-detail.html` 和 `insight-detail.html` 的 `document.title` 脚本
3. 修改 `content.js` + `data/content.js` 中涉及律所名称的内容
4. 修改 `js/shared.js` 中的 `hero_desc`

---

## 五、文件职责速查表

| 文件 | 核心职责 | 修改时特别注意 |
|------|---------|--------------|
| `index.html` | 首页结构、所有板块、内联 teamData | 成员信息需与 `team-detail.html` 同步 |
| `news-detail.html` | 新闻详情页模板、版权 | — |
| `insight-detail.html` | 评析详情页模板、版权 | — |
| `team-detail.html` | 成员详情页、teamMembers 完整数据 | 成员信息需与 `index.html` 同步 |
| `content.js` | 新闻/评析数据、分类定义 | **必须与 `data/content.js` 同步** |
| `data/content.js` | content.js 的副本 | **必须与 `content.js` 同步** |
| `js/shared.js` | 所有中英翻译、共享功能 | 一处修改影响全站 |

---

*本文档由 Claude 生成，基于对项目代码的实际分析。如有结构变更，请同步更新。*
