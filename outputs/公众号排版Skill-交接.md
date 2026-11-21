# 公众号排版 Skill 交接

## 目的与适用范围

本交接适用于将客户提供的法律文章制作成可复制到微信公众号编辑器的 HTML 排版稿。执行时使用公众号发布 Skill：

`/Users/mima0000/.codex/skills/wechat-official-article/SKILL.md`

## 已固化的要求

1. 如用户要求“仅调整排版”，不得改写、删减、增补、翻译原文；标题、正文、表格、PS、来源、免责声明及限定语均须原样保留。
2. 生成独立 HTML，正文仅有一个 `id="wechat-article"`，并保留“复制正文”功能，复制格式须包含 `text/html`。
3. 宽表格应优先改为便于手机阅读的纵向字段组，而不是密集小卡片。字段标签使用加粗与中文冒号，例如“主管机关：”；标签后的说明保持常规字重。字段间距使用内联样式，避免依赖外部 CSS。
4. 每篇文章正文和来源之后，固定按以下顺序插入两张尾图，不再另加生成式文字尾注：
   - 免责声明图；
   - 康达周争平律师团队介绍图。

## 固定素材与使用地址

Skill 内的原始固定素材：

- `/Users/mima0000/.codex/skills/wechat-official-article/assets/wechat-footer-disclaimer.png`
- `/Users/mima0000/.codex/skills/wechat-official-article/assets/wechat-footer-kangda-team.png`

公众号 HTML 应使用下列公开 HTTPS 地址，而非临时文件路径：

- `https://www.cathaypraxislaw.com/images/wechat-footer-disclaimer.png`
- `https://www.cathaypraxislaw.com/images/wechat-footer-kangda-team.png`

站点仓库对应文件：

- `images/wechat-footer-disclaimer.png`
- `images/wechat-footer-kangda-team.png`

建议的图片标签为全宽内联样式，例如：

```html
<img src="https://www.cathaypraxislaw.com/images/wechat-footer-disclaimer.png" alt="免责声明" style="display:block;width:100%;height:auto;margin:0 0 12px;border:0;">
<img src="https://www.cathaypraxislaw.com/images/wechat-footer-kangda-team.png" alt="康达周争平律师团队" style="display:block;width:100%;height:auto;margin:0;border:0;">
```

## 当前状态（必须先核验）

- 包含两张站点图片和当前公众号稿尾图的本地提交为 `6b53e5e Add stable WeChat footer assets`。
- 当前本地分支状态为 `main...origin/main [ahead 1]`；该提交尚未推送到远端。
- 在推送并完成 Vercel 部署前，上述两个公开图片地址不应被视为可用。不得仅凭本地预览声称公众号可稳定加载图片。
- 本机之前的 `git push origin main` 因 GitHub 凭据不可用失败。若仍无法推送，应请用户完成 GitHub 登录后再推送；不得把凭据写入文件或聊天内容。

## 后续 agent 操作清单

1. 阅读公众号发布 Skill，并确认两张 Skill 素材存在且尺寸正确。
2. 检查工作区；保留任何与任务无关的用户改动，不要清理或覆盖。
3. 生成或更新公众号稿时，确认原文内容逐项保留，且两张尾图位于 `#wechat-article` 内、来源之后。
4. 核对 HTML：`id="wechat-article"` 恰好一次，复制按钮可复制 `text/html`，两张 HTTPS 图片地址各恰好一次且顺序正确。
5. 如已具备 GitHub 授权，推送 `main` 并等待 Vercel 部署；以 HTTP 200 核验两张公开图片地址后，才可以称图片稳定可用。
6. 如授权缺失，保留本地提交并向用户说明只差 GitHub 登录/推送；不要伪称已上线。

## 当前成稿

- `outputs/微信公众号排版稿-美国涉军企业清单合规风险与司法救济.html`

