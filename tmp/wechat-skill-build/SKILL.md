---
name: wechat-official-article
description: Generate WeChat Official Account article HTML drafts using the user's established blue legal-insight template. Use when the user asks for 微信公众号推文, 公众号排版, 微信推文, 微信 HTML, 公众号 HTML, 可复制到微信公众号, 微信公众号排版稿, 推文排版稿, or asks to convert a DOCX/Word/article into content for posting on mp.weixin.qq.com.
---

# 微信公众号排版稿

## Purpose

Create a copy-paste-ready HTML article for WeChat Official Account publishing, using the user's established blue legal-insight template style instead of inventing a new visual system.

Use `assets/wechat-blue-legal-template.html` as the visual authority. It is based on the user's approved “出生公民权”公众号稿 and the later `微信公众号排版稿-Section301关税体系重构.html` result.

## Required workflow

1. Read the source article from the actual file or text supplied by the user.
   - For `.docx` / Word files, extract paragraphs and tables from the actual document. Preserve table structure where it matters.
   - Do not rely on screenshots as source text if a Word/HTML file is available.
2. Read or inspect `assets/wechat-blue-legal-template.html` before generating a new draft.
3. Generate a standalone local `.html` file with:
   - a sticky top toolbar containing “公众号标题建议” and a “复制正文” button;
   - a `<section id="wechat-article">` wrapper for the copied content;
   - inline styles only, because WeChat paste often strips external CSS;
   - the same blue legal-insight design language as the template:
     - dark blue gradient lead card;
     - `LEGAL INSIGHT · 法律评析` label unless the user asks for another label;
     - “正文” divider;
     - dark blue gradient section heading bars;
     - `PingFang SC` / `Microsoft YaHei` body typography;
     - 15px body text, approximately 2x line height, justified Chinese paragraphs;
     - restrained blue callout cards;
     - bottom disclaimer for general information only.
4. Adapt the content, not the template identity.
   - Do not create a new unrelated color system, card system, or brand style unless the user explicitly asks.
   - For legal/compliance/business articles, keep the tone professional and restrained.
   - Keep Chinese as the primary language. Preserve necessary legal English terms such as case names, statutes, `Section 301`, `Section 232`, `HTS`, `CBP`, etc.
5. Handle tables for WeChat readability.
   - Short 2-3 column tables may remain as compact inline-styled tables using the same dark blue header color.
   - Very wide tables may be converted into stacked cards only if needed for mobile readability, but keep the same blue template style.
   - Do not use a separate green, orange, or dashboard-like style unless requested.
6. Avoid duplicate summaries.
   - If the Word document has a lead sentence and a summary paragraph, place them in the lead card and remove duplicate repeats from the body.
7. Verify the output.
   - Check that the HTML has exactly one `id="wechat-article"`.
   - Check the copy button exists and copies `text/html`.
   - Open or render a preview when possible; inspect that the lead card, heading bars, paragraphs, and tables are readable.

## Output location

Unless the user specifies otherwise, save drafts under the current website workspace:

`/Users/mima0000/Documents/GitHub/cathay-law-website-/outputs/`

Name files as:

`微信公众号排版稿-<short-topic>.html`

## User handoff

In the final response, provide the local file link and concise instructions:

1. Open the HTML file.
2. Click “复制正文”.
3. Paste into the WeChat Official Account editor.
4. Preview on phone before publishing.

If copying fails, tell the user to select the article body manually from the rendered preview and copy/paste it into the WeChat editor.
