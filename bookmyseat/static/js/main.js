/* ===== BOOKMYSEAT MAIN JS ===== */

// User dropdown
$(document).ready(function () {
    // User menu toggle
    $('#userMenuBtn').click(function (e) {
        e.stopPropagation();
        $('#userDropdown').toggleClass('open');
    });
    $(document).click(function () {
        $('#userDropdown').removeClass('open');
    });

    // Mobile nav toggle
    $('#navToggle').click(function () {
        $('.nav-links').toggleClass('mobile-open');
    });

    // Auto-dismiss messages
    setTimeout(function () {
        $('.messages-container .alert').fadeOut(400);
    }, 4000);

    // Smooth scroll
    $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();
        const target = $($(this).attr('href'));
        if (target.length) {
            $('html, body').animate({ scrollTop: target.offset().top - 80 }, 400);
        }
    });
});

// Loading overlay
function showLoading(text) {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.querySelector('.loading-text').textContent = text || 'Processing...';
        overlay.classList.add('show');
    }
}
function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.remove('show');
}

// Mobile nav CSS
const style = document.createElement('style');
style.textContent = `
    @media (max-width: 768px) {
        .nav-links.mobile-open {
            display: flex !important;
            flex-direction: column;
            position: absolute;
            top: 64px;
            left: 0; right: 0;
            background: rgba(10,10,15,0.98);
            padding: 16px 24px 20px;
            border-bottom: 1px solid rgba(255,255,255,0.07);
            gap: 4px;
            z-index: 999;
        }
    }
`;
document.head.appendChild(style);
