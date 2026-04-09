/**
 * ClariCare — landing.js
 * Handles landing page micro-interactions:
 *   - System health check (status badge)
 *   - Scroll-triggered reveal animations for sections
 */

const API_BASE = window.location.protocol === 'file:'
    ? 'http://localhost:8000'
    : window.location.origin;

// ─── Init ─────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    initRevealAnimations();
    handleChatSymptomParam();
});

// ─── Health Check ─────────────────────────────────────────────────────────────

async function checkHealth() {
    const badge = document.getElementById('status-badge');
    try {
        const res = await fetch(`${API_BASE}/api/health`);
        const data = await res.json();
        if (data.status === 'healthy') {
            badge.className = 'flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 shadow-sm';
            badge.innerHTML = `
                <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                <span class="text-xs text-emerald-700 font-bold">${data.bert_available ? 'BERT Ready' : 'Keyword Mode'}</span>
            `;
        } else {
            throw new Error('not healthy');
        }
    } catch {
        if (badge) {
            badge.className = 'flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-50 border border-red-200 shadow-sm';
            badge.innerHTML = `
                <div class="w-2 h-2 rounded-full bg-red-500"></div>
                <span class="text-xs text-red-700 font-bold">Server Offline</span>
            `;
        }
    }
}

// ─── Scroll Reveal ────────────────────────────────────────────────────────────

function initRevealAnimations() {
    const elements = document.querySelectorAll('.reveal');
    if (!elements.length) return;

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.12 }
    );

    elements.forEach(el => observer.observe(el));
}

// ─── Chat Pre-fill ────────────────────────────────────────────────────────────
// If user clicks "Chat about this" from the explore page,
// the URL may carry ?symptom=Headache — we just redirect them.

function handleChatSymptomParam() {
    const params = new URLSearchParams(window.location.search);
    const symptom = params.get('symptom');
    if (symptom) {
        // Navigate to chat with the symptom pre-filled (chat.js handles this)
        window.location.href = `/chat?symptom=${encodeURIComponent(symptom)}`;
    }
}
