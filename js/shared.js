/**
 * Cathay Praxis Law - Shared JavaScript
 * 统一功能模块 - 确保所有页面一致性
 */

// ============================================
// Language Module
// ============================================
const LanguageModule = (function() {
    let currentLang = localStorage.getItem('cathay-lang') || 'en';
    
    const translations = {
        en: {
            // Navigation
            'nav_home': 'Home',
            'nav_about': 'About',
            'nav_practices': 'Practices',
            'nav_clients': 'Clients',
            'nav_news': 'News',
            'nav_insights': 'Insights',
            'nav_team': 'Team',
            'nav_contact': 'Contact',
            'lang_btn': 'EN',
            
            // Hero Section
            'hero_title_1': 'Where Cross-Border Strategy',
            'hero_title_2': 'Meets U.S. Execution',
            'hero_subtitle': 'We provide strategic counsel for complex U.S. matters, including transactions, compliance, and dispute resolution.',
            'hero_desc': 'Cathay Praxis Law P.C. is a U.S.-based law firm focused on helping businesses operate confidently across borders.',
            'contact_us': 'Contact Us',
            'our_services': 'Our Services',
            'scroll': 'Scroll',
            
            // About Section
            'about_title': 'Where Cross-Border Strategy Meets U.S. Execution',
            'about_desc': 'We advise companies operating across jurisdictions on complex U.S.-related transactions, regulatory compliance, and dispute matters. Our practice focuses on translating cross-border complexity into clear, executable legal strategies.',
            'value_1_title': 'Practical Judgment',
            'value_1_desc': 'Legal solutions that work in real-world business contexts.',
            'value_2_title': 'Cross-Border Precision',
            'value_2_desc': 'Translating complex regulatory frameworks into executable strategies.',
            'value_3_title': 'Integrity in Execution',
            'value_3_desc': 'Clear counsel, honest assessment, and sound strategic judgment.',
            'about_quote': 'Bridging Legal Systems with Practical Judgment.',
            
            // Practice Areas
            'services': 'Services',
            'practice_areas': 'Practice Areas',
            'practice_1_title': 'Cross-Border Transactions & U.S. Market Entry',
            'practice_1_desc': 'Advising international companies on strategic investments, acquisitions, and market entry into the United States. We provide end-to-end support across the transaction lifecycle, including structuring, due diligence, negotiation, and post-closing integration, with a focus on managing cross-border legal and regulatory risks.',
            'practice_2_title': 'Regulatory, Compliance & Risk Management',
            'practice_2_desc': 'Counseling clients on U.S. regulatory frameworks and global compliance obligations, including export controls, economic sanctions, and supply chain risk. We help companies design and implement compliance systems that align with U.S. enforcement standards and evolving international regulations.',
            'practice_3_title': 'Dispute Resolution & Cross-Border Enforcement',
            'practice_3_desc': 'Representing clients in complex commercial disputes across jurisdictions, including U.S. litigation, international arbitration, and cross-border enforcement. We focus on high-stakes disputes arising from transactions, shareholder conflicts, and international business operations.',
            'practice_4_title': 'U.S. Local Counsel & Cross-Border Coordination',
            'practice_4_desc': 'Acting as U.S. counsel or coordinating with local counsel in multi-jurisdictional matters involving foreign clients. We bridge legal, cultural, and procedural gaps to ensure effective representation in U.S. legal proceedings and transactions.',
            'practice_5_title': 'Intellectual Property & Technology Disputes',
            'practice_5_desc': 'Advising on intellectual property disputes, including patent litigation, trade secret protection, and Section 337 investigations before the U.S. International Trade Commission (ITC). We assist clients in managing IP risks in highly competitive and regulated markets.',
            
            // Clients Section
            'who_we_serve': 'WHO WE SERVE',
            'clients': 'Clients',
            'clients_desc': 'We advise companies, investors, and institutions navigating complex legal and regulatory challenges in the United States.',
            'clients_include': 'Our clients include:',
            'client_1': 'International companies entering or expanding in the U.S. market',
            'client_2': 'Growth-stage and multinational enterprises with cross-border operations',
            'client_3': 'Private equity and investment funds executing U.S.-related transactions',
            'client_4': 'U.S. companies engaged in international business and cross-border disputes',
            
            // Industries Section
            'sectors_label': 'FOCUS AREAS',
            'industries_title': 'Industries',
            'industries_desc': 'We focus on industries where cross-border regulatory, transactional, and dispute risks are most significant:',
            'industry_1_title': 'Technology & Innovation',
            'industry_1_desc': '(AI, software, semiconductors, cross-border data)',
            'industry_2_title': 'Advanced Manufacturing & Industrial',
            'industry_2_desc': '(equipment, automotive, supply chain)',
            'industry_3_title': 'Energy & Infrastructure',
            'industry_3_desc': '(renewables, EPC projects, global investments)',
            'industry_4_title': 'International Trade & Supply Chain',
            'industry_4_desc': '(export controls, sanctions, trade remedies)',
            
            // News Section
            'updates': 'UPDATES',
            'view_all_news': 'View All News',
            
            // Insights Section
            'latest': 'LATEST',
            'view_all_insights': 'View All Insights',
            
            // Team Section
            'our_people': 'OUR PEOPLE',
            'team_desc': 'Team members have experience across international law firms and institutional environments',
            
            // Contact Section
            'get_in_touch': 'GET IN TOUCH',
            'contact_desc': 'Whether you are navigating a complex regulatory inquiry or planning a cross-border transaction, our team is ready to provide strategic counsel.',
            'office_ca': 'Mailing Address',
            'office_phone': 'Phone',
            'office_email': 'Email',
            
            // Common
            'view_all': 'View All',
            'read_more': 'Read More',
            'load_more': 'Load More',
            'search': 'Search',
            'filter_by': 'Filter by',
            'all': 'All',
            'back': 'Back',
            'share': 'Share',
            'print': 'Print',
            'learn_more': 'Learn More',
            
            // News Categories
            'category_policy': 'Policy Alert',
            'category_regulation': 'Regulation',
            'category_case': 'Case Study',
            'category_industry': 'Industry',
            
            // Insight Topics
            'topic_export': 'Export Controls',
            'topic_cfius': 'CFIUS',
            'topic_ip': 'Intellectual Property',
            'topic_compliance': 'Compliance',
            'topic_litigation': 'Litigation',
            'topic_transaction': 'Transaction',
            
            // Footer
            'privacy_policy': 'Privacy Policy',
            'disclaimer': 'Disclaimer',
            'footer_tagline': 'Bridging Legal Systems with Practical Judgment',
            'attorney_advertising_label': 'Attorney Advertising',
            'attorney_advertising_text': 'ATTORNEY ADVERTISING. Prior results do not guarantee a similar outcome. This website may be considered attorney advertising under applicable state laws. Information does not constitute legal advice. Contacting us does not create an attorney-client relationship.',
            
            // Page Titles
            'page_news_title': 'News',
            'page_news_subtitle': 'Latest updates on regulations, policies, and industry developments',
            'page_insights_title': 'Insights',
            'page_insights_subtitle': 'In-depth legal analysis and strategic guidance',
            
            // Empty States
            'no_results': 'No results found',
            'no_results_desc': 'Try adjusting your search or filter criteria',
            
            // Form
            'form_name': 'Name',
            'form_email': 'Email',
            'form_phone': 'Phone',
            'form_company': 'Company',
            'form_service_type': 'Service Type',
            'form_service_placeholder': 'Select Service Type',
            'form_service_cross_border': 'Cross-Border Transactions',
            'form_service_regulatory': 'Regulatory & Compliance',
            'form_service_dispute': 'Dispute Resolution',
            'form_service_ip': 'IP Litigation',
            'form_service_general': 'General Inquiry',
            'form_inquiry': 'Inquiry',
            'form_submit': 'Submit Inquiry',
            'form_schedule': 'Schedule a Consultation',
            'privacy_consent_prefix': 'I have read and agree to the ',
            'privacy_policy_link': 'Privacy Policy',
            'privacy_consent_suffix': '. I understand that submitting this form does not create an attorney-client relationship.',
            'form_warning_title': 'IMPORTANT NOTICE:',
            'form_warning_1': 'Please do not include confidential or sensitive information in this form.',
            'form_warning_2': 'Submission of this form does not establish an attorney-client relationship. An attorney-client relationship is established only after we reach an agreement to represent you and you have signed an engagement letter.',
            
            // Privacy Policy Modal
            'privacy_policy_title': 'Privacy Policy',
            
            // Location
            'location_sv': 'Silicon Valley'
        },
        zh: {
            // Navigation
            'nav_home': '首页',
            'nav_about': '关于我们',
            'nav_practices': '业务领域',
            'nav_clients': '客户',
            'nav_news': '热点聚焦',
            'nav_insights': '法律评析',
            'nav_team': '专业团队',
            'nav_contact': '联系我们',
            'lang_btn': '中',
            
            // Hero Section
            'hero_title_1': '跨境有道',
            'hero_title_2': '判断有衡',
            'hero_subtitle': '我们专注于复杂的美国法律事务，为跨境交易、监管合规及争议解决提供战略性法律咨询。',
            'hero_desc': '博衡律师事务所是一家美国律师事务所，致力于协助企业在跨境经营中稳健发展。',
            'contact_us': '联系我们',
            'our_services': '业务领域',
            'scroll': '向下滚动',
            
            // About Section
            'about_title': '跨境有道，判断有衡',
            'about_desc': '我们为在多个司法管辖区运营的企业提供法律服务，涵盖涉美交易、监管合规及争议解决。我们的执业重点是将跨境复杂性转化为清晰、可执行的法律策略。',
            'value_1_title': '务实判断',
            'value_1_desc': '立足商业现实，提供切实可行的法律解决方案。',
            'value_2_title': '跨境精准',
            'value_2_desc': '化繁为简，将复杂的监管要求转化为可落地的执行策略。',
            'value_3_title': '恪守诚信',
            'value_3_desc': '提供清晰建议、诚实评估与审慎的战略判断。',
            'about_quote': '以务实判断，连接法律制度。',
            
            // Practice Areas
            'services': '服务',
            'practice_areas': '业务领域',
            'practice_1_title': '跨境交易及美国市场准入',
            'practice_1_desc': '为国际企业提供在美战略投资、收购及市场准入的法律服务。我们在交易全流程提供支持，涵盖交易架构设计、尽职调查、谈判及交割后整合，重点关注跨境法律与监管风险。',
            'practice_2_title': '监管合规与风险管理',
            'practice_2_desc': '就美国监管框架与全球合规义务为客户提供法律咨询，涵盖出口管制、经济制裁及供应链风险。我们协助企业建立并执行符合美国执法标准、顺应国际法规演变的合规体系。',
            'practice_3_title': '争议解决与跨境执行',
            'practice_3_desc': '代表客户处理跨司法管辖区的复杂商事争议，涵盖美国诉讼、国际仲裁及跨境执行。我们专注于处理由交易、股东冲突及国际业务运营引发的高风险争议。',
            'practice_4_title': '美国本地法律顾问与跨境协调',
            'practice_4_desc': '在多司法管辖区事务中，我们为外国客户担任美国法律顾问，或协调本地律师协同工作。我们打通法律、文化与程序壁垒，确保客户在美国诉讼及交易中获得有效代理。',
            'practice_5_title': '知识产权与技术争议',
            'practice_5_desc': '我们为知识产权争议提供法律服务，涵盖专利诉讼、商业秘密保护及美国国际贸易委员会（ITC）第337条调查，协助客户在高度竞争及受监管的市场中有效管理知识产权风险。',
            
            // Clients Section
            'who_we_serve': '服务对象',
            'clients': '客户',
            'clients_desc': '我们为面临复杂美国法律与监管挑战的企业、投资者及机构提供法律服务。',
            'clients_include': '我们的客户包括：',
            'client_1': '已进入或正在拓展美国市场的国际公司',
            'client_2': '成长型企业及拥有跨境业务的跨国企业',
            'client_3': '从事美国相关交易的私募股权及投资基金',
            'client_4': '从事国际业务、面临跨境争议的美国企业',
            
            // Industries Section
            'sectors_label': '重点行业',
            'industries_title': '行业',
            'industries_desc': '我们专注于跨境监管、交易及争议风险高度集中的行业：',
            'industry_1_title': '科技与创新',
            'industry_1_desc': '（人工智能、软件、半导体、跨境数据）',
            'industry_2_title': '先进制造与工业',
            'industry_2_desc': '（设备、汽车、供应链）',
            'industry_3_title': '能源与基础设施',
            'industry_3_desc': '（可再生能源、工程总承包项目、全球投资）',
            'industry_4_title': '国际贸易与供应链',
            'industry_4_desc': '（出口管制、制裁、贸易救济）',
            
            // News Section
            'updates': '最新动态',
            'view_all_news': '查看全部热点',
            
            // Insights Section
            'latest': '法律评析',
            'view_all_insights': '查看全部评析',
            
            // Team Section
            'our_people': '专业团队',
            'team_desc': '团队成员曾任职于国际律师事务所及专业机构，拥有丰富的执业经验。',
            
            // Contact Section
            'get_in_touch': '联系我们',
            'contact_desc': '无论您正面临复杂的监管调查，还是筹划跨境交易，我们的团队随时准备为您提供战略性法律支持。',
            'office_ca': '邮寄地址',
            'office_phone': '电话',
            'office_email': '电子邮件',
            
            // Common
            'view_all': '查看全部',
            'read_more': '阅读更多',
            'load_more': '加载更多',
            'search': '搜索',
            'filter_by': '筛选',
            'all': '全部',
            'back': '返回',
            'share': '分享',
            'print': '打印',
            'learn_more': '了解更多',
            
            // News Categories
            'category_policy': '政策预警',
            'category_regulation': '法规更新',
            'category_case': '案例研究',
            'category_industry': '行业动态',
            
            // Insight Topics
            'topic_export': '出口管制',
            'topic_cfius': 'CFIUS',
            'topic_ip': '知识产权',
            'topic_compliance': '合规监管',
            'topic_litigation': '诉讼仲裁',
            'topic_transaction': '跨境交易',
            
            // Footer
            'privacy_policy': '隐私政策',
            'disclaimer': '免责声明',
            'footer_tagline': '以务实判断，连接法律制度',
            'attorney_advertising_label': '律师广告',
            'attorney_advertising_text': '根据适用法律，本网站可能被视为律师广告。过往结果不保证类似成果。本网站信息不构成法律意见。联系我们不当然形成律师-客户关系。',
            
            // Page Titles
            'page_news_title': '热点聚焦',
            'page_news_subtitle': '法规政策与行业动态的最新更新',
            'page_insights_title': '法律评析',
            'page_insights_subtitle': '深度法律分析与战略指导',
            
            // Empty States
            'no_results': '未找到结果',
            'no_results_desc': '请尝试调整搜索或筛选条件',
            
            // Form
            'form_name': '姓名',
            'form_email': '邮箱',
            'form_phone': '电话',
            'form_company': '公司名称',
            'form_service_type': '服务类型',
            'form_service_placeholder': '选择服务类型',
            'form_service_cross_border': '跨境交易',
            'form_service_regulatory': '监管合规',
            'form_service_dispute': '争议解决',
            'form_service_ip': '知识产权诉讼',
            'form_service_general': '一般咨询',
            'form_inquiry': '咨询内容',
            'form_submit': '提交咨询',
            'form_schedule': '预约咨询',
            'privacy_consent_prefix': '我已阅读并同意',
            'privacy_policy_link': '隐私政策',
            'privacy_consent_suffix': '。我理解提交此表单不形成律师-客户关系。',
            'form_warning_title': '重要声明：',
            'form_warning_1': '请勿在此表单中包含机密或敏感信息。',
            'form_warning_2': '提交此表单不建立律师-客户关系。律师-客户关系仅在我们达成代理协议且您已签署聘用函后建立。',
            
            // Privacy Policy Modal
            'privacy_policy_title': '隐私政策',
            
            // Location
            'location_sv': '硅谷'
        }
    };
    
    function get(key) {
        return translations[currentLang][key] || key;
    }
    
    function toggle() {
        currentLang = currentLang === 'en' ? 'zh' : 'en';
        localStorage.setItem('cathay-lang', currentLang);
        updatePage();
        // Update language switch button text
        const btns = document.querySelectorAll('#lang-btn, #lang-switch');
        btns.forEach(function(btn) {
            if (btn) btn.textContent = currentLang === 'en' ? '中' : 'EN';
        });
        return currentLang;
    }
    
    function set(lang) {
        if (translations[lang]) {
            currentLang = lang;
            localStorage.setItem('cathay-lang', currentLang);
            updatePage();
        }
    }
    
    function getCurrent() {
        return currentLang;
    }
    
    function updatePage() {
        // Update all elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (translations[currentLang] && translations[currentLang][key]) {
                if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                    el.placeholder = translations[currentLang][key];
                } else {
                    el.textContent = translations[currentLang][key];
                }
            }
        });
        
        // Update lang button
        const langBtn = document.getElementById('lang-btn');
        if (langBtn) {
            langBtn.textContent = currentLang === 'en' ? '中' : 'EN';
        }
        
        // Update HTML lang attribute
        document.documentElement.lang = currentLang;
        
        // Update select options if they have data-i18n
        document.querySelectorAll('select[data-i18n] option[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (translations[currentLang] && translations[currentLang][key]) {
                el.textContent = translations[currentLang][key];
            }
        });
        
        // Dispatch event for other components
        document.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang: currentLang } }));
    }
    
    // Add translations dynamically
    function addTranslations(newTranslations) {
        if (newTranslations.en) {
            Object.assign(translations.en, newTranslations.en);
        }
        if (newTranslations.zh) {
            Object.assign(translations.zh, newTranslations.zh);
        }
        updatePage();
    }
    
    // Initialize - wait for other scripts to load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(updatePage, 0);
        });
    } else {
        setTimeout(updatePage, 0);
    }
    
    return {
        get,
        toggle,
        set,
        getCurrent,
        updatePage,
        addTranslations
    };
})();

// ============================================
// Navigation Module
// ============================================
const NavigationModule = (function() {
    function init() {
        // Navbar scroll effect
        const navbar = document.getElementById('navbar');
        if (navbar) {
            window.addEventListener('scroll', () => {
                if (window.scrollY > 50) {
                    navbar.classList.add('navbar-scrolled');
                } else {
                    navbar.classList.remove('navbar-scrolled');
                }
            });
        }
        
        // Mobile menu toggle
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const navLinks = document.getElementById('nav-links');
        if (mobileMenuBtn && navLinks) {
            mobileMenuBtn.addEventListener('click', () => {
                navLinks.classList.toggle('active');
                mobileMenuBtn.classList.toggle('active');
            });
        }
        
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href !== '#') {
                    const target = document.querySelector(href);
                    if (target) {
                        e.preventDefault();
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });
    }
    
    document.addEventListener('DOMContentLoaded', init);
    
    return {
        init
    };
})();

// ============================================
// Filter Module (for News/Insights pages)
// ============================================
const FilterModule = (function() {
    let activeFilter = 'all';
    let searchQuery = '';
    let onFilterChange = null;
    
    function init(options = {}) {
        onFilterChange = options.onChange || null;
        
        // Filter tabs
        const filterTabs = document.querySelectorAll('.filter-tab');
        filterTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                filterTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                activeFilter = tab.getAttribute('data-filter') || 'all';
                triggerFilterChange();
            });
        });
        
        // Search box
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            let debounceTimer;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => {
                    searchQuery = e.target.value.toLowerCase();
                    triggerFilterChange();
                }, 300);
            });
        }
    }
    
    function triggerFilterChange() {
        if (onFilterChange) {
            onFilterChange({
                filter: activeFilter,
                search: searchQuery
            });
        }
    }
    
    function getActiveFilter() {
        return activeFilter;
    }
    
    function getSearchQuery() {
        return searchQuery;
    }
    
    function filterItems(items) {
        return items.filter(item => {
            // Category filter
            if (activeFilter !== 'all' && item.category !== activeFilter) {
                return false;
            }
            
            // Search filter
            if (searchQuery) {
                const searchFields = [
                    item.title?.en || '',
                    item.title?.zh || '',
                    item.excerpt?.en || '',
                    item.excerpt?.zh || '',
                    item.category || ''
                ].join(' ').toLowerCase();
                
                if (!searchFields.includes(searchQuery)) {
                    return false;
                }
            }
            
            return true;
        });
    }
    
    return {
        init,
        getActiveFilter,
        getSearchQuery,
        filterItems
    };
})();

// ============================================
// Pagination Module
// ============================================
const PaginationModule = (function() {
    let currentPage = 1;
    let itemsPerPage = 9;
    let totalItems = 0;
    let onPageChange = null;
    
    function init(options = {}) {
        itemsPerPage = options.itemsPerPage || 9;
        onPageChange = options.onChange || null;
    }
    
    function setTotalItems(total) {
        totalItems = total;
        render();
    }
    
    function goToPage(page) {
        const totalPages = Math.ceil(totalItems / itemsPerPage);
        if (page >= 1 && page <= totalPages) {
            currentPage = page;
            if (onPageChange) {
                onPageChange(currentPage);
            }
            render();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }
    
    function getCurrentPage() {
        return currentPage;
    }
    
    function getItemsPerPage() {
        return itemsPerPage;
    }
    
    function getPaginatedItems(items) {
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        return items.slice(start, end);
    }
    
    function render() {
        const container = document.getElementById('pagination');
        if (!container) return;
        
        const totalPages = Math.ceil(totalItems / itemsPerPage);
        
        if (totalPages <= 1) {
            container.innerHTML = '';
            return;
        }
        
        let html = '';
        
        // Previous button
        html += `<button class="pagination-btn" ${currentPage === 1 ? 'disabled' : ''} onclick="PaginationModule.goToPage(${currentPage - 1})">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
        </button>`;
        
        // Page numbers
        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
                html += `<button class="pagination-btn ${i === currentPage ? 'active' : ''}" onclick="PaginationModule.goToPage(${i})">${i}</button>`;
            } else if (i === currentPage - 2 || i === currentPage + 2) {
                html += `<span class="pagination-btn" style="cursor: default;">...</span>`;
            }
        }
        
        // Next button
        html += `<button class="pagination-btn" ${currentPage === totalPages ? 'disabled' : ''} onclick="PaginationModule.goToPage(${currentPage + 1})">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
        </button>`;
        
        container.innerHTML = html;
    }
    
    return {
        init,
        setTotalItems,
        goToPage,
        getCurrentPage,
        getItemsPerPage,
        getPaginatedItems
    };
})();

// ============================================
// Utility Functions
// ============================================
const Utils = {
    // Format date
    formatDate: function(dateStr, lang = 'en') {
        const date = new Date(dateStr);
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return date.toLocaleDateString(lang === 'zh' ? 'zh-CN' : 'en-US', options);
    },
    
    // Truncate text
    truncate: function(text, maxLength = 150) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength).trim() + '...';
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Get URL parameter
    getUrlParam: function(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    },
    
    // Set URL parameter
    setUrlParam: function(param, value) {
        const url = new URL(window.location);
        if (value) {
            url.searchParams.set(param, value);
        } else {
            url.searchParams.delete(param);
        }
        window.history.pushState({}, '', url);
    }
};

// ============================================
// Global Exports
// ============================================
window.LanguageModule = LanguageModule;
window.NavigationModule = NavigationModule;
window.FilterModule = FilterModule;
window.PaginationModule = PaginationModule;
window.Utils = Utils;

// Toggle language global function
function toggleLang() {
    LanguageModule.toggle();
}

// Close mobile menu global function
function closeMobileMenu() {
    const navLinks = document.getElementById('nav-links');
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    if (navLinks) navLinks.classList.remove('active');
    if (mobileMenuBtn) mobileMenuBtn.classList.remove('active');
}
