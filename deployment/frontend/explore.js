/**
 * ClariCare — explore.js
 * Fetches symptom data from the API and renders the interactive
 * symptom explorer with search and risk-level filtering.
 */

const API_BASE = window.location.protocol === 'file:'
    ? 'http://localhost:8000'
    : window.location.origin;

let allSymptoms = [];
let activeFilter = 'all';

// ─── Init ─────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    loadSymptoms();
    checkHealth();

    // Live search
    document.getElementById('search-input').addEventListener('input', () => {
        renderVisible();
    });
});

// ─── Data Loading ─────────────────────────────────────────────────────────────

async function loadSymptoms() {
    try {
        const res = await fetch(`${API_BASE}/api/symptoms`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        allSymptoms = data.symptoms || [];

        // Hide skeleton, show grid
        document.getElementById('skeleton-grid').classList.add('hidden');
        document.getElementById('symptom-grid').classList.remove('hidden');

        renderVisible();
    } catch (err) {
        document.getElementById('skeleton-grid').innerHTML = `
            <div class="col-span-3 text-center py-16">
                <div class="w-14 h-14 rounded-full bg-red-50 border border-red-200 flex items-center justify-center mx-auto mb-4">
                    <svg class="w-7 h-7 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                </div>
                <p class="text-red-600 font-semibold">Could not load symptoms</p>
                <p class="text-surface-400 text-sm mt-1">Make sure the ClariCare backend is running.</p>
                <button onclick="loadSymptoms()" class="mt-4 px-4 py-2 bg-brand-600 text-white rounded-xl text-sm font-semibold hover:bg-brand-500 transition-all">Retry</button>
            </div>
        `;
        console.error('Failed to load symptoms:', err);
    }
}

// ─── Filter ───────────────────────────────────────────────────────────────────

function setFilter(filter, btn) {
    activeFilter = filter;

    // Update button styles
    document.querySelectorAll('.filter-tab').forEach(b => {
        b.className = 'filter-tab'; // reset
    });
    btn.classList.add(`active-${filter}`);

    renderVisible();
}

// ─── Render ───────────────────────────────────────────────────────────────────

function renderVisible() {
    const query = document.getElementById('search-input').value.toLowerCase().trim();
    const grid = document.getElementById('symptom-grid');
    const noResults = document.getElementById('no-results');
    const countEl = document.getElementById('visible-count');

    // Filter by risk + search
    const filtered = allSymptoms.filter(s => {
        const matchesFilter = activeFilter === 'all' || s.risk_level === activeFilter;
        const matchesSearch = !query ||
            s.name.toLowerCase().includes(query) ||
            s.key.toLowerCase().includes(query) ||
            s.specialist.toLowerCase().includes(query) ||
            (s.keywords || []).some(k => k.toLowerCase().includes(query));
        return matchesFilter && matchesSearch;
    });

    grid.innerHTML = '';

    if (filtered.length === 0) {
        noResults.classList.remove('hidden');
        countEl.textContent = '0 symptoms';
    } else {
        noResults.classList.add('hidden');
        filtered.forEach((symptom, index) => {
            const card = buildSymptomCard(symptom, index);
            grid.appendChild(card);
        });
        countEl.textContent = `${filtered.length} of ${allSymptoms.length} symptoms`;
    }
}

function buildSymptomCard(symptom, index) {
    const riskBadgeClass = {
        low: 'risk-badge-low',
        medium: 'risk-badge-medium',
        high: 'risk-badge-high'
    }[symptom.risk_level] || 'risk-badge-low';

    const riskLabel = {
        low: '🟢 Low Risk',
        medium: '🟡 Medium Risk',
        high: '🔴 High Risk'
    }[symptom.risk_level] || 'Low Risk';

    const card = document.createElement('div');
    card.className = 'symptom-card reveal';
    card.style.transitionDelay = `${index * 0.03}s`;

    card.innerHTML = `
        <div class="flex items-start justify-between gap-3">
            <div class="flex items-center gap-3">
                <span class="text-2xl flex-shrink-0">${symptom.icon || '🩺'}</span>
                <div>
                    <h3 class="font-display font-bold text-surface-900">${escapeHtml(symptom.name)}</h3>
                    <p class="text-xs text-surface-500 font-medium mt-0.5">${escapeHtml(symptom.specialist)}</p>
                </div>
            </div>
            <span class="${riskBadgeClass} flex-shrink-0">${riskLabel}</span>
        </div>

        <div>
            <p class="text-[10px] font-bold text-surface-400 uppercase tracking-widest mb-2">Common keywords</p>
            <div class="flex flex-wrap gap-1.5">
                ${(symptom.keywords || []).slice(0, 4).map(k => `
                    <span class="keyword-tag">${escapeHtml(k)}</span>
                `).join('')}
            </div>
        </div>

        <div class="pt-3 border-t border-surface-100 flex gap-2">
            <a href="/chat?symptom=${encodeURIComponent(symptom.name)}"
               class="flex-1 text-center py-2 rounded-lg bg-brand-50 border border-brand-100 text-brand-700 font-semibold text-xs hover:bg-brand-100 transition-all">
                💬 Chat about this
            </a>
        </div>
    `;

    // Observer for reveal animation
    observeReveal(card);
    return card;
}

// ─── Scroll Reveal ────────────────────────────────────────────────────────────

function observeReveal(el) {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    e.target.classList.add('visible');
                    observer.unobserve(e.target);
                }
            });
        },
        { threshold: 0.1 }
    );
    observer.observe(el);
}

// ─── Health Check ─────────────────────────────────────────────────────────────

async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE}/api/health`);
        const data = await res.json();
        const badge = document.getElementById('status-badge');
        if (data.status === 'healthy') {
            badge.className = 'flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-200';
            badge.innerHTML = `
                <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                <span class="text-xs text-emerald-700 font-bold">${data.bert_available ? 'BERT Ready' : 'Keyword Mode'}</span>
            `;
        }
    } catch {
        const badge = document.getElementById('status-badge');
        if (badge) {
            badge.className = 'flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-50 border border-red-200';
            badge.innerHTML = `<div class="w-2 h-2 rounded-full bg-red-500"></div><span class="text-xs text-red-700 font-bold">Offline</span>`;
        }
    }
}

// ─── Utilities ────────────────────────────────────────────────────────────────

function escapeHtml(str) {
    if (!str) return '';
    const d = document.createElement('div');
    d.textContent = String(str);
    return d.innerHTML;
}
