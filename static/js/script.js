/* =========================================
   CAMPUS CONNECT - MASTER JAVASCRIPT
========================================= */

// 1. THEME TOGGLE (DARK / LIGHT MODE)
window.applySavedTheme = function () {
    const savedTheme = localStorage.getItem("theme");
    const themeIcon = document.getElementById("themeIcon");
    const themeText = document.getElementById("themeText");

    if (savedTheme === "dark") {
        document.body.classList.add("dark-theme");
        if (themeIcon) themeIcon.innerHTML = '<i class="fa-solid fa-sun"></i>';
        if (themeText) themeText.textContent = "Light";
    } else {
        document.body.classList.remove("dark-theme");
        if (themeIcon) themeIcon.innerHTML = '<i class="fa-solid fa-moon"></i>';
        if (themeText) themeText.textContent = "Dark";
    }
};

window.toggleTheme = function () {
    const isDark = document.body.classList.toggle("dark-theme");
    const themeIcon = document.getElementById("themeIcon");
    const themeText = document.getElementById("themeText");

    if (isDark) {
        localStorage.setItem("theme", "dark");
        if (themeIcon) themeIcon.innerHTML = '<i class="fa-solid fa-sun"></i>';
        if (themeText) themeText.textContent = "Light";
    } else {
        localStorage.setItem("theme", "light");
        if (themeIcon) themeIcon.innerHTML = '<i class="fa-solid fa-moon"></i>';
        if (themeText) themeText.textContent = "Dark";
    }
};

// 2. MODAL CONTROLS (POPUP FORMS)
window.openModal = function (id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.style.display = "flex";
    }
};

window.closeModal = function (id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.style.display = "none";
    }
};

window.onclick = function (event) {
    if (event.target && event.target.classList && event.target.classList.contains("modal")) {
        event.target.style.display = "none";
    }
};

// 3. CUSTOM CONFIRM DELETE MODAL (REPLACES BROWSER ALERT)
let deleteTargetUrl = "";

window.confirmCustomDelete = function (targetUrl, message) {
    deleteTargetUrl = targetUrl;
    const deleteModal = document.getElementById("customDeleteModal");
    const messageElem = document.getElementById("customDeleteMessage");
    const confirmBtn = document.getElementById("customDeleteConfirmBtn");

    if (messageElem && message) {
        messageElem.textContent = message;
    }
    if (confirmBtn) {
        confirmBtn.onclick = function () {
            if (deleteTargetUrl) {
                window.location.href = deleteTargetUrl;
            }
        };
    }
    if (deleteModal) {
        deleteModal.style.display = "flex";
    }
};

window.closeCustomDeleteModal = function () {
    const deleteModal = document.getElementById("customDeleteModal");
    if (deleteModal) {
        deleteModal.style.display = "none";
    }
    deleteTargetUrl = "";
};

// 4. FLASH ALERT CLOSE / DISMISS
window.dismissAlert = function (btnElement) {
    const alertBox = btnElement.closest(".alert-msg");
    if (alertBox) {
        alertBox.style.opacity = "0";
        alertBox.style.transform = "translateY(-6px)";
        setTimeout(() => {
            alertBox.remove();
        }, 250);
    }
};

// 5. VIEW MORE / SHOW LESS TOGGLE FOR TABLES
window.toggleTableRows = function (rowClass, btnId, defaultCount) {
    const rows = document.getElementsByClassName(rowClass);
    const btn = document.getElementById(btnId);
    if (!btn) return;
    const isExpanded = btn.getAttribute("data-expanded") === "true";

    for (let i = defaultCount; i < rows.length; i++) {
        if (isExpanded) {
            rows[i].classList.add("hidden-row");
            rows[i].style.display = "none";
        } else {
            rows[i].classList.remove("hidden-row");
            rows[i].style.display = "table-row";
        }
    }

    if (isExpanded) {
        btn.setAttribute("data-expanded", "false");
        if (rowClass === "student-row") {
            btn.innerHTML = `<i class="fa-solid fa-eye"></i> View More (Show All ${rows.length} Students)`;
        } else if (rowClass === "staff-row") {
            btn.innerHTML = `<i class="fa-solid fa-eye"></i> View More (Show All ${rows.length} Staff Members)`;
        } else {
            btn.innerHTML = `<i class="fa-solid fa-eye"></i> View More (Show All ${rows.length})`;
        }
    } else {
        btn.setAttribute("data-expanded", "true");
        btn.innerHTML = '<i class="fa-solid fa-chevron-up"></i> Show Less';
    }
};

// 6. BACK TO TOP (SCROLL TO TOP BUTTON)
document.addEventListener('DOMContentLoaded', () => {
    // Create the button dynamically if it doesn't exist
    if (!document.getElementById("backToTopBtn")) {
        const topBtn = document.createElement("button");
        topBtn.id = "backToTopBtn";
        topBtn.innerHTML = '<i class="fa-solid fa-arrow-up"></i>';
        topBtn.title = "Go to top";
        
        // Stylish floating circle styling
        Object.assign(topBtn.style, {
            display: "none",
            position: "fixed",
            bottom: "30px",
            right: "30px",
            zIndex: "9999",
            fontSize: "20px",
            border: "none",
            outline: "none",
            backgroundColor: "#2563eb",
            color: "white",
            cursor: "pointer",
            width: "50px",
            height: "50px",
            borderRadius: "50%",
            boxShadow: "0 4px 6px rgba(0,0,0,0.2)",
            transition: "background-color 0.2s ease, opacity 0.3s ease",
            alignItems: "center",
            justifyContent: "center",
            opacity: "0"
        });
        
        topBtn.onmouseover = function() { this.style.backgroundColor = '#1d4ed8'; };
        topBtn.onmouseout = function() { this.style.backgroundColor = '#2563eb'; };
        topBtn.onclick = function() { window.scrollTo({ top: 0, behavior: 'smooth' }); };
        
        document.body.appendChild(topBtn);
    }

    // Scroll behavior
    window.addEventListener('scroll', function () {
        const topBtn = document.getElementById("backToTopBtn");
        if (topBtn) {
            if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
                topBtn.style.display = "flex";
                // slight delay to allow display:flex to apply before opacity transition
                setTimeout(() => topBtn.style.opacity = "1", 10);
            } else {
                topBtn.style.opacity = "0";
                setTimeout(() => {
                    if (document.body.scrollTop <= 200 && document.documentElement.scrollTop <= 200) {
                        topBtn.style.display = "none";
                    }
                }, 300); // match transition duration
            }
        }
    });
});

// 7. PASSWORD VISIBILITY TOGGLE (CLEAN INSTAGRAM / FB STYLE SVG)
const EYE_OPEN_SVG = `<svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>`;
const EYE_CLOSED_SVG = `<svg viewBox="0 0 24 24"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>`;

window.togglePasswordVisibility = function (fieldId, iconId) {
    const passwordField = document.getElementById(fieldId);
    const iconSpan = document.getElementById(iconId);

    if (!passwordField) return;

    if (passwordField.type === "password") {
        passwordField.type = "text";
        if (iconSpan) iconSpan.innerHTML = EYE_CLOSED_SVG;
    } else {
        passwordField.type = "password";
        if (iconSpan) iconSpan.innerHTML = EYE_OPEN_SVG;
    }
};

document.addEventListener("DOMContentLoaded", function () {
    window.applySavedTheme();

    const themeBtn = document.getElementById("themeToggle");
    if (themeBtn) {
        themeBtn.onclick = window.toggleTheme;
    }
});

// 8. DYNAMIC SIDEBAR TABS GENERATOR (100% Jinja Safe)
document.addEventListener('DOMContentLoaded', () => {
    const main = document.querySelector('main.dashboard');
    // Only apply if there is a main.dashboard and it contains h2 tags (which represent sections)
    if (!main) return;
    const h2s = main.querySelectorAll('h2');
    if (h2s.length === 0) return;

    // Create Layout Wrappers
    const layout = document.createElement('div');
    layout.className = 'dashboard-layout';

    const sidebar = document.createElement('aside');
    sidebar.className = 'dashboard-sidebar';
    const sidebarList = document.createElement('ul');
    sidebarList.className = 'sidebar-nav-list';
    sidebar.appendChild(sidebarList);

    const contentArea = document.createElement('div');
    contentArea.className = 'dashboard-content-area';

    // Separate modals to avoid hiding them accidentally when parent section is hidden
    const allChildren = Array.from(main.childNodes);
    const modals = [];
    const childrenToProcess = [];

    allChildren.forEach(node => {
        if (node.nodeType === 1 && node.classList && node.classList.contains('modal')) {
            modals.push(node);
        } else {
            childrenToProcess.push(node);
        }
    });

    // Group elements into sections
    let currentSection = document.createElement('section');
    currentSection.className = 'tab-section active-section';
    currentSection.id = 'tab-overview';
    currentSection.style.display = 'block';

    let sectionCount = 0;

    // Overview Link
    const overviewLink = document.createElement('li');
    overviewLink.className = 'active';
    overviewLink.dataset.target = 'tab-overview';
    overviewLink.innerHTML = '<i class="fa-solid fa-chart-pie"></i> Dashboard Overview';
    overviewLink.onclick = () => window.switchTab('tab-overview', overviewLink);
    sidebarList.appendChild(overviewLink);

    // Process content sequentially
    childrenToProcess.forEach(node => {
        if (node.nodeType === 1 && node.tagName.toLowerCase() === 'h2') {
            // Push previous section to content area if not empty
            contentArea.appendChild(currentSection);

            sectionCount++;
            const secId = 'tab-section-' + sectionCount;

            currentSection = document.createElement('section');
            currentSection.className = 'tab-section';
            currentSection.id = secId;
            currentSection.style.display = 'none';

            let h2Text = node.innerText || node.textContent;
            let cleanName = h2Text.replace(/\(.*?\)/g, '').replace(/Total:.*/, '').trim();

            let h2Html = node.innerHTML;
            let faMatch = h2Html.match(/<i class="[^"]+"><\/i>/);
            let iconHtml = faMatch ? faMatch[0] + ' ' : '';

            // Extract or assign emoji
            let linkText = cleanName;
            if (iconHtml) {
                // If the h2 has a FontAwesome icon, we use it. We also strip any remaining emoji if desired,
                // but usually the emoji is replaced by the icon.
                let textWithoutEmoji = cleanName.replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]|\p{Emoji_Presentation}/gu, '').trim();
                linkText = iconHtml + textWithoutEmoji;
            } else {
                let emojiMatch = h2Text.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]|\p{Emoji_Presentation}/u);
                if (!emojiMatch) {
                    linkText = '<i class="fa-solid fa-circle-dot"></i> ' + cleanName;
                } else {
                    linkText = cleanName;
                }
            }

            const link = document.createElement('li');
            link.innerHTML = linkText;
            link.dataset.target = secId;
            link.onclick = () => window.switchTab(secId, link);
            sidebarList.appendChild(link);
        }
        currentSection.appendChild(node);
    });

    // Append the final section
    contentArea.appendChild(currentSection);

    // Append layout to main
    layout.appendChild(sidebar);
    layout.appendChild(contentArea);
    main.appendChild(layout);

    // Re-append modals to main (outside of hidden sections)
    modals.forEach(m => main.appendChild(m));

    // --- Mobile Sidebar Toggle Logic ---
    const header = document.querySelector('header.dashboard-header') || document.querySelector('header');
    if (header) {
        const menuBtn = document.createElement('button');
        menuBtn.className = 'mobile-menu-btn';
        menuBtn.innerHTML = '☰';
        menuBtn.title = "Toggle Menu";

        const overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        document.body.appendChild(overlay);

        header.appendChild(menuBtn); // Absolute positioned via CSS

        menuBtn.onclick = function () {
            sidebar.classList.add('open');
            overlay.classList.add('active');
        };

        overlay.onclick = function () {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        };
    }

    // Switch function global logic
    window.switchTab = function (sectionId, linkElement) {
        document.querySelectorAll('.tab-section').forEach(sec => {
            sec.style.display = 'none';
            sec.classList.remove('active-section');
        });
        document.querySelectorAll('.sidebar-nav-list li').forEach(li => {
            li.classList.remove('active');
        });

        const target = document.getElementById(sectionId);
        if (target) {
            target.style.display = 'block';
            setTimeout(() => target.classList.add('active-section'), 10);
        }
        if (linkElement) {
            linkElement.classList.add('active');
        } else {
            // Fallback: try to find the link if not passed directly
            const fallbackLink = document.querySelector(`.sidebar-nav-list li[data-target="${sectionId}"]`);
            if (fallbackLink) fallbackLink.classList.add('active');
        }

        // Save to localStorage so it persists across reloads and form submissions
        localStorage.setItem('activeTab_' + window.location.pathname, sectionId);

        // Only scroll smoothly if triggered manually, not on initial load
        if (linkElement) {
            // Auto-close sidebar on mobile after clicking a link
            sidebar.classList.remove('open');
            const overlay = document.querySelector('.sidebar-overlay');
            if (overlay) overlay.classList.remove('active');

            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    };

    // Auto-restore active tab from localStorage if available
    const savedTab = localStorage.getItem('activeTab_' + window.location.pathname);
    if (savedTab && document.getElementById(savedTab)) {
        window.switchTab(savedTab, null);
    }
});

// =========================================
// 8. REGIONAL LANGUAGE SELECTOR (GOOGLE TRANSLATE INTEGRATION)
// =========================================
window.googleTranslateElementInit = function() {
    new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'en,hi,or',
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
        autoDisplay: false
    }, 'google_translate_element');
};

document.addEventListener('DOMContentLoaded', function() {
    // 1. Inject Google Translate script and hidden div
    const gtScript = document.createElement('script');
    gtScript.type = 'text/javascript';
    gtScript.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.body.appendChild(gtScript);

    const gtDiv = document.createElement('div');
    gtDiv.id = 'google_translate_element';
    gtDiv.style.display = 'none';
    document.body.appendChild(gtDiv);

    // 2. Inject CSS to hide Google Translate banner and tooltips for seamless experience
    const style = document.createElement('style');
    style.innerHTML = `
        body { top: 0 !important; position: static !important; }
        .goog-te-banner-frame { display: none !important; }
        .goog-te-balloon-frame { display: none !important; }
        .goog-tooltip { display: none !important; }
        .goog-tooltip:hover { display: none !important; }
        #goog-gt-tt, .goog-te-balloon-frame { display: none !important; }
        .goog-text-highlight { background-color: transparent !important; border: none !important; box-shadow: none !important; }
    `;
    document.head.appendChild(style);

    // 3. Add language selector UI next to themeToggle if not already present
    const themeToggles = document.querySelectorAll('.theme-toggle-btn');
    themeToggles.forEach(toggle => {
        // Prevent duplicate injection
        if (toggle.previousElementSibling && toggle.previousElementSibling.classList.contains('lang-selector')) {
            return;
        }

        const langContainer = document.createElement('div');
        langContainer.className = 'lang-selector';
        langContainer.style.display = 'inline-flex';
        langContainer.style.alignItems = 'center';
        langContainer.style.gap = '8px';
        langContainer.style.marginRight = '12px';
        langContainer.style.verticalAlign = 'middle';

        langContainer.innerHTML = `
            <i class="fa-solid fa-language" style="font-size: 1.2rem; color: var(--text-secondary);"></i>
            <select class="customLangSelect" style="padding: 6px 10px; border-radius: 6px; border: 1px solid var(--border-color); background: var(--bg-card); color: var(--text-primary); cursor: pointer; outline: none; font-size: 14px; font-family: inherit;">
                <option value="en">English</option>
                <option value="hi">Hindi</option>
                <option value="or">Odia</option>
            </select>
        `;

        toggle.parentNode.insertBefore(langContainer, toggle);

        const select = langContainer.querySelector('.customLangSelect');
        
        // Load saved language
        const savedLang = localStorage.getItem('selected_language') || 'en';
        select.value = savedLang;
        
        if (savedLang !== 'en') {
            setLanguageCookie(savedLang);
        } else {
            clearLanguageCookie();
        }

        select.addEventListener('change', function() {
            const newLang = this.value;
            localStorage.setItem('selected_language', newLang);
            if (newLang === 'en') {
                clearLanguageCookie();
            } else {
                setLanguageCookie(newLang);
            }
            window.location.reload();
        });
    });
});

function setLanguageCookie(lang) {
    document.cookie = "googtrans=/en/" + lang + "; path=/";
    document.cookie = "googtrans=/en/" + lang + "; domain=" + window.location.hostname + "; path=/";
}

function clearLanguageCookie() {
    document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; domain=" + window.location.hostname + "; path=/;";
}