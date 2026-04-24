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
            'attorney_advertising': 'Attorney Advertising',
            'attorney_advertising_text': 'This website may be considered attorney advertising under applicable state laws. Information does not constitute legal advice. Contacting us does not create an attorney-client relationship.',
            
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
            'form_inquiry': 'Inquiry',
            'form_submit': 'Submit Inquiry',
            'form_schedule': 'Schedule a Consultation'
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
            'attorney_advertising': '律师广告',
            'attorney_advertising_text': '根据适用法律，本网站可能被视为律师广告。信息不构成法律意见。联系不当然形成律师关系。',
            
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
            'form_inquiry': '咨询内容',
            'form_submit': '提交咨询',
            'form_schedule': '预约咨询'
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
