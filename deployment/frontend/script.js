/**
 * ClariCare — Frontend JavaScript
 * Handles user interactions, API calls, and dynamic result rendering.
 */

// If opened directly from file system, default to localhost:8000 where FastAPI usually runs.
const API_BASE = window.location.protocol === 'file:' 
    ? 'http://localhost:8000' 
    : window.location.origin;

// ─── DOM Elements ───────────────────────────────────────────────────────────────
const symptomInput = document.getElementById('symptom-input');
const analyzeBtn = document.getElementById('analyze-btn');
const btnText = document.getElementById('btn-text');
const btnSpinner = document.getElementById('btn-spinner');
const charCount = document.getElementById('char-count');
const loadingSection = document.getElementById('loading-section');
const resultsSection = document.getElementById('results-section');

// ─── Character counter ──────────────────────────────────────────────────────────
symptomInput.addEventListener('input', () => {
    charCount.textContent = symptomInput.value.length;
    if (symptomInput.value.length > 2000) {
        charCount.classList.add('text-red-500');
    } else {
        charCount.classList.remove('text-red-500');
    }
});

// Enter key submits (Shift+Enter for new line)
symptomInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        analyzeSymptoms();
    }
});

// ─── Quick tag buttons ──────────────────────────────────────────────────────────
function addTag(tag) {
    const current = symptomInput.value.trim();
    if (current.toLowerCase().includes(tag.toLowerCase())) return;

    if (current.length > 0 && !current.endsWith(',') && !current.endsWith('.')) {
        symptomInput.value = current + ', ' + tag;
    } else {
        symptomInput.value = (current ? current + ' ' : '') + tag;
    }

    charCount.textContent = symptomInput.value.length;

    // Toggle tag visual state
    const tagButtons = document.querySelectorAll('.symptom-tag');
    tagButtons.forEach(btn => {
        if (btn.textContent.trim().toLowerCase() === tag.toLowerCase()) {
            btn.classList.add('active');
            setTimeout(() => btn.classList.remove('active'), 1000);
        }
    });

    symptomInput.focus();
}

// ─── Main analysis function ─────────────────────────────────────────────────────
async function analyzeSymptoms() {
    const symptoms = symptomInput.value.trim();

    if (!symptoms || symptoms.length < 3) {
        symptomInput.classList.add('error-shake', '!border-red-400');
        setTimeout(() => {
            symptomInput.classList.remove('error-shake', '!border-red-400');
        }, 600);
        return;
    }

    // Show loading state
    setLoadingState(true);

    try {
        const response = await fetch(`${API_BASE}/api/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symptoms })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        renderResults(data);

    } catch (error) {
        console.error('Analysis failed:', error);
        showError(error.message);
    } finally {
        setLoadingState(false);
    }
}

// ─── Loading state ──────────────────────────────────────────────────────────────
function setLoadingState(loading) {
    if (loading) {
        analyzeBtn.disabled = true;
        btnText.textContent = 'Analyzing...';
        btnSpinner.classList.remove('hidden');
        loadingSection.classList.remove('hidden');
        resultsSection.classList.add('hidden');
    } else {
        analyzeBtn.disabled = false;
        btnText.textContent = 'Analyze Symptoms';
        btnSpinner.classList.add('hidden');
        loadingSection.classList.add('hidden');
    }
}

// ─── Error display ──────────────────────────────────────────────────────────────
function showError(message) {
    resultsSection.innerHTML = `
        <div class="max-w-3xl mx-auto px-4">
            <div class="bg-red-50 border border-red-200 rounded-2xl p-6 text-center animate-scale-in shadow-sm">
                <div class="w-12 h-12 mx-auto mb-3 rounded-full bg-red-100 flex items-center justify-center">
                    <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                </div>
                <h3 class="text-red-800 font-bold mb-1">Analysis Failed</h3>
                <p class="text-red-600 text-sm font-medium">${escapeHtml(message)}</p>
                <p class="text-red-500/70 text-xs mt-2">Please ensure the FastAPI backend is running.</p>
            </div>
        </div>
    `;
    resultsSection.classList.remove('hidden');
}

// ─── Render results ─────────────────────────────────────────────────────────────
function renderResults(data) {
    // Reset section innerHTML if it was overwritten by an error earlier
    if (resultsSection.querySelector('.bg-red-50')) {
        location.reload(); // Quick hack to reset cleanly if previously errored
        return;
    }

    resultsSection.classList.remove('hidden');

    // Re-trigger animations
    document.querySelectorAll('#results-section [class*="animate-"]').forEach(el => {
        el.style.animation = 'none';
        el.offsetHeight; // trigger reflow
        el.style.animation = '';
    });

    renderMeta(data.analysis_meta);
    renderRisk(data.risk);
    renderSymptoms(data.sections.symptom_summary || []);
    renderCauses(data.sections.possible_causes || {});
    renderLifestyle(data.sections.lifestyle_advice || {});
    renderDoctors(data.specialists, data.sections.doctor_recommendation || {});
    renderDisclaimer(data.disclaimer);

    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 200);
}

// ─── Meta bar ───────────────────────────────────────────────────────────────────
function renderMeta(meta) {
    document.getElementById('meta-method').textContent = meta.method || 'Unknown';
    document.getElementById('meta-symptoms-count').textContent = `${meta.symptoms_detected} symptom${meta.symptoms_detected !== 1 ? 's' : ''} detected`;

    const bertBadge = document.getElementById('meta-bert-badge');
    if (meta.bert_available) {
        bertBadge.className = 'flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-100 shadow-sm';
        bertBadge.innerHTML = '<div class="w-1.5 h-1.5 rounded-full bg-emerald-500"></div> BERT Active';
    } else {
        bertBadge.className = 'flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full bg-amber-50 text-amber-700 border border-amber-100 shadow-sm';
        bertBadge.innerHTML = '<div class="w-1.5 h-1.5 rounded-full bg-amber-500"></div> Keyword Mode';
    }
}

// ─── Risk assessment ────────────────────────────────────────────────────────────
function renderRisk(risk) {
    const riskCard = document.getElementById('risk-card');
    const riskBadge = document.getElementById('risk-badge');
    const riskLabel = document.getElementById('risk-label');
    const riskUrgency = document.getElementById('risk-urgency');
    const riskFactors = document.getElementById('risk-factors');
    const riskIcon = document.getElementById('risk-icon');
    const riskIconContainer = document.getElementById('risk-icon-container');

    const colors = {
        low: { header: 'bg-emerald-50/50', border: 'border-emerald-100', text: 'text-emerald-700', badge: 'bg-emerald-100 text-emerald-800 border border-emerald-200', icon: '✅', iconBg: 'bg-emerald-100 border-emerald-200 text-emerald-600' },
        medium: { header: 'bg-amber-50/50', border: 'border-amber-100', text: 'text-amber-700', badge: 'bg-amber-100 text-amber-800 border border-amber-200', icon: '⚠️', iconBg: 'bg-amber-100 border-amber-200 text-amber-600' },
        high: { header: 'bg-red-50/50', border: 'border-red-100', text: 'text-red-700', badge: 'bg-red-100 text-red-800 border border-red-200', icon: '🚨', iconBg: 'bg-red-100 border-red-200 text-red-600' },
        none: { header: 'bg-surface-50/50', border: 'border-surface-200', text: 'text-surface-600', badge: 'bg-surface-100 text-surface-700 border border-surface-200', icon: '❓', iconBg: 'bg-surface-100 border-surface-200 text-surface-600' }
    };

    const c = colors[risk.level] || colors.none;
    const header = document.getElementById('risk-header');
    
    header.className = `px-6 py-5 border-b ${c.border} ${c.header}`;
    riskBadge.className = `self-start sm:self-auto px-4 py-1.5 rounded-full text-sm font-bold uppercase tracking-wider ${c.badge}`;
    riskBadge.textContent = risk.label;
    riskLabel.textContent = 'Risk Assessment';
    riskUrgency.textContent = risk.urgency;
    riskIcon.textContent = c.icon;
    riskIconContainer.className = `w-12 h-12 rounded-xl flex items-center justify-center border ${c.iconBg} risk-pulse risk-${risk.level}`;

    // Risk factors
    riskFactors.innerHTML = '';
    (risk.factors || []).forEach(factor => {
        const div = document.createElement('div');
        div.className = 'flex items-start gap-2.5 text-sm text-surface-700 font-medium';
        div.innerHTML = `
            <div class="mt-0.5 w-4 h-4 rounded-full flex items-center justify-center flex-shrink-0 bg-white border border-surface-200 shadow-sm">
                <div class="w-1.5 h-1.5 rounded-full ${c.text.replace('text', 'bg')}"></div>
            </div>
            <span>${escapeHtml(factor)}</span>
        `;
        riskFactors.appendChild(div);
    });
}

// ─── Detected symptoms ──────────────────────────────────────────────────────────
function renderSymptoms(symptoms) {
    const grid = document.getElementById('symptoms-grid');
    grid.innerHTML = '';

    if (!symptoms || symptoms.length === 0) {
        grid.innerHTML = '<p class="text-surface-500 font-medium text-sm">No specific symptoms detected</p>';
        return;
    }

    symptoms.forEach((symptom, index) => {
        const confidence = Math.round((symptom.confidence || 0) * 100);
        const barColor =
            confidence >= 80 ? 'bg-emerald-500' :
            confidence >= 60 ? 'bg-brand-400' :
            confidence >= 40 ? 'bg-amber-400' : 'bg-surface-400';

        const methodLabel =
            symptom.method === 'keyword + BERT' ? '🔬 Keyword + BERT' :
            symptom.method === 'BERT semantic' ? '🧠 BERT Semantic' :
            '🔑 Keyword Match';

        const div = document.createElement('div');
        div.className = 'symptom-detected';
        div.style.animationDelay = `${index * 0.08}s`;
        div.innerHTML = `
            <div class="flex items-center justify-between mb-2.5">
                <span class="font-bold text-sm text-surface-900">${escapeHtml(symptom.symptom)}</span>
                <span class="text-xs font-bold text-surface-500 bg-surface-50 px-2 py-0.5 rounded-md border border-surface-200">${confidence}%</span>
            </div>
            <div class="confidence-bar mb-2">
                <div class="confidence-bar-fill ${barColor}" style="width: 0%"></div>
            </div>
            <span class="text-[10px] font-medium text-surface-400 uppercase tracking-wide">${methodLabel}</span>
        `;
        grid.appendChild(div);

        // Animate confidence bar
        setTimeout(() => {
            div.querySelector('.confidence-bar-fill').style.width = `${confidence}%`;
        }, 300 + index * 100);
    });
}

// ─── Possible causes ────────────────────────────────────────────────────────────
function renderCauses(causes) {
    const content = document.getElementById('causes-content');
    content.innerHTML = '';

    const entries = Object.entries(causes);
    if (entries.length === 0) {
        content.innerHTML = '<p class="text-surface-500 font-medium text-sm">No specific factors identified</p>';
        return;
    }

    entries.forEach(([symptom, causeList]) => {
        const section = document.createElement('div');
        section.innerHTML = `
            <h4 class="text-sm font-bold text-surface-800 mb-2.5">${escapeHtml(symptom)}</h4>
            <div class="flex flex-wrap gap-2">
                ${causeList.map(cause => `<span class="cause-tag">${escapeHtml(cause)}</span>`).join('')}
            </div>
        `;
        content.appendChild(section);
    });
}

// ─── Lifestyle suggestions ──────────────────────────────────────────────────────
function renderLifestyle(advice) {
    const content = document.getElementById('lifestyle-content');
    content.innerHTML = '';

    const allTips = [];
    const seen = new Set();

    Object.values(advice).forEach(tips => {
        tips.forEach(tip => {
            if (!seen.has(tip)) {
                seen.add(tip);
                allTips.push(tip);
            }
        });
    });

    if (allTips.length === 0) {
        content.innerHTML = '<p class="text-surface-500 font-medium text-sm col-span-2">No lifestyle suggestions available</p>';
        return;
    }

    allTips.slice(0, 8).forEach(tip => {
        const div = document.createElement('div');
        div.className = 'lifestyle-tip';
        div.innerHTML = `
            <span class="text-brand-600 flex-shrink-0 mt-0.5">🌿</span>
            <span class="font-medium">${escapeHtml(tip)}</span>
        `;
        content.appendChild(div);
    });
}

// ─── Doctor recommendations ─────────────────────────────────────────────────────
function renderDoctors(specialists, doctorSection) {
    const content = document.getElementById('doctor-content');
    const adviceEl = document.getElementById('doctor-advice');
    content.innerHTML = '';

    if (!specialists || specialists.length === 0) {
        content.innerHTML = '<p class="text-surface-500 font-medium text-sm">No specific specialist recommendation</p>';
        adviceEl.parentElement.classList.add('hidden');
        return;
    }

    adviceEl.parentElement.classList.remove('hidden');

    specialists.forEach((spec, index) => {
        const isPrimary = index === 0;
        const div = document.createElement('div');
        div.className = `specialist-card ${isPrimary ? 'primary' : ''}`;
        div.innerHTML = `
            <div class="w-12 h-12 rounded-xl ${isPrimary ? 'bg-white shadow-sm border border-green-200' : 'bg-surface-50 border border-surface-200'} flex items-center justify-center flex-shrink-0">
                <span class="text-2xl">${spec.icon || '🩺'}</span>
            </div>
            <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-0.5">
                    <span class="font-bold text-sm text-surface-900">${escapeHtml(spec.name)}</span>
                    ${isPrimary ? '<span class="px-2 py-0.5 rounded-full text-[10px] bg-brand-500 text-white font-bold tracking-wide uppercase">Primary</span>' : ''}
                </div>
                <p class="text-xs text-surface-500 font-medium truncate">For: ${spec.symptoms.join(', ')}</p>
            </div>
            <div class="text-xs font-bold text-surface-400 bg-surface-50 px-2.5 py-1 rounded-lg border border-surface-200">${Math.round((spec.max_confidence || 0) * 100)}% match</div>
        `;
        content.appendChild(div);
    });

    adviceEl.textContent = doctorSection.general_advice || '';
}

// ─── Disclaimer ─────────────────────────────────────────────────────────────────
function renderDisclaimer(disclaimer) {
    document.getElementById('disclaimer-text').textContent = disclaimer || '';
}

// ─── Utility ────────────────────────────────────────────────────────────────────
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ─── Health check on load ───────────────────────────────────────────────────────
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/api/health`);
        const data = await response.json();

        const badge = document.getElementById('status-badge');
        if (data.status === 'healthy') {
            badge.className = 'flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 shadow-sm';
            badge.innerHTML = `
                <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                <span class="text-xs text-emerald-700 font-bold">${data.bert_available ? 'BERT Ready' : 'Keyword Mode'}</span>
            `;
        }
    } catch (e) {
        const badge = document.getElementById('status-badge');
        badge.className = 'flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-50 border border-red-200 shadow-sm';
        badge.innerHTML = `
            <div class="w-2 h-2 rounded-full bg-red-500"></div>
            <span class="text-xs text-red-700 font-bold">Server Offline</span>
        `;
    }
}

// Run health check on page load
document.addEventListener('DOMContentLoaded', checkHealth);
