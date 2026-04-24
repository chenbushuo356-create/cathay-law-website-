// api/contact.js - Resend 邮件转发
const { Resend } = require('resend');

// 允许前端跨域调用
const allowCors = fn => async (req, res) => {
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  return await fn(req, res);
};

async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  try {
    const { name, email, phone, company, service, message, language } = req.body;

    // 必填检查
    if (!name || !email || !message) {
      return res.status(400).json({
        success: false,
        message: language === 'zh' ? '请填写姓名、邮箱和留言内容' : 'Name, email, and message are required.'
      });
    }

    // 邮箱格式检查
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({
        success: false,
        message: language === 'zh' ? '邮箱格式不正确' : 'Invalid email address.'
      });
    }

    const resend = new Resend(process.env.RESEND_API_KEY);

    const serviceLabels = {
      en: {
        'cross-border': 'Cross-Border Transactions',
        'regulatory': 'Regulatory & Compliance',
        'dispute': 'Dispute Resolution',
        'ip': 'IP Litigation',
        'immigration': 'Immigration Services',
        'general': 'General Inquiry',
        'other': 'Other'
      },
      zh: {
        'cross-border': '跨境交易',
        'regulatory': '监管合规',
        'dispute': '争议解决',
        'ip': '知识产权诉讼',
        'immigration': '移民服务',
        'general': '一般咨询',
        'other': '其他'
      }
    };

    const lang = language || 'en';
    const serviceName = service && serviceLabels[lang] && serviceLabels[lang][service]
      ? serviceLabels[lang][service]
      : (service || 'Not specified');

    const subject = lang === 'zh'
      ? `[网站咨询] ${name} - ${serviceName}`
      : `[Website Inquiry] ${name} - ${serviceName}`;

    const recipient = process.env.RECIPIENT_EMAIL || 'info@cathaypraxislaw.com';

    // 如果域名已验证，用你自己的域名；如果没验证，Resend 会报错，先用 onboarding@resend.dev 测试
    const fromEmail = process.env.FROM_EMAIL || 'onboarding@resend.dev';
    const fromName = 'Cathay Praxis Law Website';

    const { data, error } = await resend.emails.send({
      from: `${fromName} <${fromEmail}>`,
      to: [recipient],
      reply_to: email,
      subject: subject,
      text: `
New Website Inquiry
===================
Name: ${name}
Email: ${email}
Phone: ${phone || 'N/A'}
Company: ${company || 'N/A'}
Service: ${serviceName}
Language: ${lang}
Message:
${message}
Time: ${new Date().toISOString()}
      `.trim(),
      html: `
        <h2>${lang === 'zh' ? '新网站咨询' : 'New Website Inquiry'}</h2>
        <table style="border-collapse: collapse; width: 100%; max-width: 600px; font-family: Arial, sans-serif;">
          <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; background: #f5f5f5;">Name</td><td style="padding: 10px; border: 1px solid #ddd;">${name}</td></tr>
          <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; background: #f5f5f5;">Email</td><td style="padding: 10px; border: 1px solid #ddd;">${email}</td></tr>
          <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; background: #f5f5f5;">Phone</td><td style="padding: 10px; border: 1px solid #ddd;">${phone || 'N/A'}</td></tr>
          <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; background: #f5f5f5;">Company</td><td style="padding: 10px; border: 1px solid #ddd;">${company || 'N/A'}</td></tr>
          <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; background: #f5f5f5;">Service</td><td style="padding: 10px; border: 1px solid #ddd;">${serviceName}</td></tr>
          <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; background: #f5f5f5; vertical-align: top;">Message</td><td style="padding: 10px; border: 1px solid #ddd;">${message.replace(/\n/g, '<br>')}</td></tr>
          <tr><td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; background: #f5f5f5;">Time</td><td style="padding: 10px; border: 1px solid #ddd;">${new Date().toLocaleString()}</td></tr>
        </table>
        <hr style="margin-top: 20px;">
        <p style="color: #999; font-size: 12px;">${lang === 'zh' ? '本邮件由 Cathay Praxis Law 网站自动发送' : 'This email was automatically sent from the Cathay Praxis Law website'}</p>
      `
    });

    if (error) {
      console.error('Resend error:', error);
      return res.status(500).json({
        success: false,
        message: language === 'zh' ? '邮件发送失败，请稍后重试' : 'Failed to send email. Please try again.'
      });
    }

    return res.status(200).json({
      success: true,
      message: lang === 'zh' ? '提交成功，我们将尽快与您联系。' : 'Submitted successfully. We will contact you soon.'
    });

  } catch (error) {
    console.error('Server error:', error);
    return res.status(500).json({
      success: false,
      message: 'Server error. Please try again later.'
    });
  }
}

module.exports = allowCors(handler);
