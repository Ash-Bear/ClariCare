/**
 * ClariCare — chat.js
 * Manages the conversational chatbot session with Clara.
 * Handles session lifecycle, message rendering, typing indicators,
 * quick replies, analysis card injection, and emergency alerts.
 */

const API_BASE = window.location.protocol === 'file:'
    ? 'http://localhost:8000'
    : window.location.origin;

let sessionId = null;
let isWaiting = false;       // Prevent double-sends during bot "typing"
let lastAnalysisData = null; // Stored for Print Summary
let conversationHistory = []; // Q&A history for clinical print summary

// ─── Page Init ────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    initChat();

    // Auto-resize textarea as user types
    const textarea = document.getElementById('chat-input');
    textarea.addEventListener('input', () => {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    });

    // Enter to send (Shift+Enter for newline)
    textarea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});

async function initChat() {
    await checkHealth();
    await startSession();

    // If user came from Explore page with ?symptom=Headache, auto-fill + send
    const params = new URLSearchParams(window.location.search);
    const symptom = params.get('symptom');
    if (symptom) {
        await sleep(600); // let greeting render first
        const textarea = document.getElementById('chat-input');
        textarea.value = `I have ${symptom.toLowerCase()}`;
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }
}

// ─── Session Management ───────────────────────────────────────────────────────

async function startSession() {
    try {
        const res = await fetch(`${API_BASE}/api/chat/start`, { method: 'POST' });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        sessionId = data.session_id;
        appendBotMessage(data.bot_reply);
        showQuickReplies(data.quick_replies);
    } catch (err) {
        appendErrorMessage(
            'Could not connect to ClariCare. Please make sure the backend server is running at localhost:8000.'
        );
        console.error('Session start failed:', err);
    }
}

function newConsultation() {
    sessionId = null;
    isWaiting = false;
    document.getElementById('messages-area').innerHTML = '';
    clearQuickReplies();
    document.getElementById('emergency-alert').classList.add('hidden');
    document.getElementById('chat-input').value = '';
    document.getElementById('chat-input').style.height = 'auto';
    document.getElementById('send-btn').disabled = false;
    conversationHistory = [];
    lastAnalysisData = null;
    startSession();
}

// ─── Send Message ─────────────────────────────────────────────────────────────

async function sendMessage(presetText = null) {
    const textarea = document.getElementById('chat-input');
    const text = presetText || textarea.value.trim();

    if (!text || isWaiting) return;

    // Clear input immediately
    textarea.value = '';
    textarea.style.height = 'auto';
    clearQuickReplies();
    appendUserMessage(text);

    isWaiting = true;
    setTypingIndicator(true);

    // Natural thinking delay (400–900ms)
    await sleep(400 + Math.random() * 500);

    try {
        const res = await fetch(`${API_BASE}/api/chat/message`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, message: text })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        sessionId = data.session_id;

        setTypingIndicator(false);
        appendBotMessage(data.bot_reply);

        // Analysis card injected after a short pause
        if (data.analysis) {
            await sleep(300);
            appendAnalysisCard(data.analysis);
        }

        if (data.show_emergency_alert) {
            showEmergencyAlert();
        }

        showQuickReplies(data.quick_replies);

    } catch (err) {
        setTypingIndicator(false);
        appendErrorMessage('Something went wrong. Please try again.');
        console.error('Message send failed:', err);
    } finally {
        isWaiting = false;
    }
}

// ─── Message Renderers ────────────────────────────────────────────────────────

function appendUserMessage(text) {
    conversationHistory.push({ role: 'patient', text });
    const area = document.getElementById('messages-area');
    const now = getCurrentTime();

    const div = document.createElement('div');
    div.className = 'flex justify-end items-end gap-2.5 message-enter';
    div.innerHTML = `
        <div class="max-w-[75%] sm:max-w-[65%]">
            <div class="chat-bubble-user">${nl2br(escapeHtml(text))}</div>
            <p class="text-right text-[11px] text-surface-400 mt-1.5 font-medium">You · ${now}</p>
        </div>
        <div class="w-8 h-8 rounded-full bg-surface-200 border-2 border-surface-300 flex items-center justify-center flex-shrink-0">
            <svg class="w-4 h-4 text-surface-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
        </div>
    `;
    area.appendChild(div);
    scrollToBottom();
}

function appendBotMessage(text) {
    conversationHistory.push({ role: 'clara', text });
    const area = document.getElementById('messages-area');
    const now = getCurrentTime();

    const div = document.createElement('div');
    div.className = 'flex items-end gap-2.5 message-enter';
    div.innerHTML = `
        <div class="w-9 h-9 rounded-full bg-gradient-to-br from-brand-500 to-emerald-400 flex items-center justify-center flex-shrink-0 shadow-md shadow-brand-500/20">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
        </div>
        <div class="max-w-[75%] sm:max-w-[65%]">
            <p class="text-[11px] text-surface-500 mb-1.5 font-semibold">Clara · ClariCare AI</p>
            <div class="chat-bubble-bot">${nl2br(formatMarkdown(escapeHtml(text)))}</div>
            <p class="text-[11px] text-surface-400 mt-1.5 font-medium">${now}</p>
        </div>
    `;
    area.appendChild(div);
    scrollToBottom();
}

function appendAnalysisCard(data) {
    lastAnalysisData = data;
    const area = document.getElementById('messages-area');

    // Indent to align with bot messages (avatar offset)
    const wrapper = document.createElement('div');
    wrapper.className = 'flex gap-2.5 message-enter';
    wrapper.innerHTML = `<div class="w-9 flex-shrink-0"></div>`; // spacer for avatar

    const card = buildAnalysisCard(data);
    wrapper.appendChild(card);
    area.appendChild(wrapper);
    scrollToBottom();
}

// ─── Analysis Card Builder ────────────────────────────────────────────────────

function buildAnalysisCard(data) {
    const risk = data.risk || {};
    const specialists = data.specialists || [];
    const sections = data.sections || {};
    const symptoms = sections.symptom_summary || [];
    const lifestyle = sections.lifestyle_advice || {};
    const meta = data.analysis_meta || {};

    // Deduplicate lifestyle tips
    const allTips = [];
    const tipsSeen = new Set();
    Object.values(lifestyle).forEach(tips => {
        tips.forEach(tip => {
            if (!tipsSeen.has(tip)) { tipsSeen.add(tip); allTips.push(tip); }
        });
    });

    const rc = getRiskColors(risk.level);

    const card = document.createElement('div');
    card.className = 'analysis-card';

    card.innerHTML = `
        <div class="analysis-card-inner">

            <!-- Card Header -->
            <div class="flex items-center gap-3 mb-5 pb-4 border-b border-surface-100">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500 to-emerald-400 flex items-center justify-center shadow-sm flex-shrink-0">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                </div>
                <div class="flex-1 min-w-0">
                    <h3 class="font-display font-bold text-surface-900 text-sm">Your Health Assessment</h3>
                    <p class="text-[11px] text-surface-500 font-medium">${escapeHtml(meta.method || 'AI Analysis')} · ${meta.symptoms_detected || 0} symptom(s) found</p>
                </div>
                <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border flex-shrink-0 ${rc.badge}">${risk.label || 'Unknown'}</span>
            </div>

            <!-- Risk Block -->
            <div class="rounded-xl p-4 mb-5 ${rc.bg} border ${rc.border}">
                <div class="flex items-center gap-2 mb-1.5">
                    <span class="text-xl">${rc.icon}</span>
                    <span class="font-bold text-sm ${rc.text}">${risk.label || 'Unknown Risk'}</span>
                </div>
                <p class="text-sm ${rc.text} leading-relaxed">${escapeHtml(risk.urgency || '')}</p>
            </div>

            <!-- Detected Symptoms -->
            ${symptoms.length > 0 ? `
            <div class="mb-5">
                <h4 class="text-[10px] font-bold uppercase tracking-widest text-surface-400 mb-2.5">Detected Symptoms</h4>
                <div class="space-y-2">
                    ${symptoms.slice(0, 6).map(s => `
                        <div class="flex items-center justify-between bg-surface-50 rounded-lg px-3 py-2.5 border border-surface-100">
                            <div>
                                <span class="text-sm font-semibold text-surface-800">${escapeHtml(s.symptom)}</span>
                                <span class="ml-2 text-[10px] text-surface-400 font-medium">${escapeHtml(s.method || '')}</span>
                            </div>
                            <div class="flex items-center gap-2 flex-shrink-0">
                                <div class="w-16 h-1.5 rounded-full bg-surface-200 overflow-hidden">
                                    <div class="h-full rounded-full ${s.confidence >= 0.8 ? 'bg-emerald-500' : s.confidence >= 0.6 ? 'bg-brand-400' : 'bg-amber-400'}" style="width:${Math.round(s.confidence*100)}%"></div>
                                </div>
                                <span class="text-xs font-bold text-surface-500 w-9 text-right">${Math.round(s.confidence*100)}%</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>` : ''}

            <!-- Specialists -->
            ${specialists.length > 0 ? `
            <div class="mb-5">
                <h4 class="text-[10px] font-bold uppercase tracking-widest text-surface-400 mb-2.5">Recommended Specialists</h4>
                <div class="space-y-2">
                    ${specialists.slice(0, 3).map((spec, i) => `
                        <div class="rounded-xl border overflow-hidden transition-all ${i === 0 ? 'bg-emerald-50 border-emerald-200' : 'bg-white border-surface-200'}">
                            <!-- Specialist info row -->
                            <div class="flex items-center gap-3 p-3">
                                <span class="text-2xl flex-shrink-0">${spec.icon || '🩺'}</span>
                                <div class="flex-1 min-w-0">
                                    <div class="flex items-center gap-2 flex-wrap">
                                        <span class="text-sm font-bold text-surface-900">${escapeHtml(spec.name)}</span>
                                        ${i === 0 ? '<span class="text-[9px] bg-brand-500 text-white px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">Primary</span>' : ''}
                                    </div>
                                    <p class="text-xs text-surface-500 mt-0.5 truncate">For: ${spec.symptoms.slice(0,3).join(', ')}</p>
                                </div>
                            </div>
                            <!-- Find Nearby action row -->
                            <div class="border-t ${i === 0 ? 'border-emerald-200' : 'border-surface-100'} grid grid-cols-2 divide-x ${i === 0 ? 'divide-emerald-200' : 'divide-surface-100'}">
                                <a href="https://www.google.com/maps/search/${encodeURIComponent(spec.name + ' near me')}"
                                   target="_blank" rel="noopener noreferrer"
                                   class="flex items-center justify-center gap-1.5 py-2 text-[11px] font-bold text-blue-600 hover:bg-blue-50 transition-all">
                                    <svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                                    Find Doctor Nearby
                                </a>
                                <a href="https://www.google.com/maps/search/${encodeURIComponent(spec.name + ' hospital near me')}"
                                   target="_blank" rel="noopener noreferrer"
                                   class="flex items-center justify-center gap-1.5 py-2 text-[11px] font-bold text-blue-600 hover:bg-blue-50 transition-all">
                                    <svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
                                    Find Hospitals
                                </a>
                            </div>
                        </div>
                    `).join('')}
                </div>

                <!-- All nearby healthcare facilities banner -->
                <a href="https://www.google.com/maps/search/hospitals+and+clinics+near+me"
                   target="_blank" rel="noopener noreferrer"
                   class="mt-3 flex items-center gap-2.5 p-3 rounded-xl bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 hover:border-blue-400 hover:shadow-md transition-all group">
                    <div class="w-8 h-8 rounded-lg bg-blue-100 border border-blue-200 flex items-center justify-center flex-shrink-0 group-hover:bg-blue-200 transition-all">
                        <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>
                    </div>
                    <div class="flex-1 min-w-0">
                        <p class="text-xs font-bold text-blue-800">🏥 Find All Nearby Healthcare Facilities</p>
                        <p class="text-[10px] text-blue-600 font-medium">Hospitals, clinics &amp; urgent care centers near you → Google Maps</p>
                    </div>
                    <svg class="w-4 h-4 text-blue-400 flex-shrink-0 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                </a>
            </div>` : ''}

            <!-- Lifestyle Tips -->
            ${allTips.length > 0 ? `
            <div class="mb-5">
                <h4 class="text-[10px] font-bold uppercase tracking-widest text-surface-400 mb-2.5">Lifestyle Suggestions</h4>
                <div class="grid grid-cols-1 gap-2">
                    ${allTips.slice(0, 4).map(tip => `
                        <div class="flex items-start gap-2 bg-emerald-50 border border-emerald-100 rounded-lg px-3 py-2.5">
                            <span class="flex-shrink-0 text-sm">🌿</span>
                            <span class="text-xs text-emerald-800 font-medium leading-relaxed">${escapeHtml(tip)}</span>
                        </div>
                    `).join('')}
                </div>
            </div>` : ''}

            <!-- Disclaimer -->
            <div class="p-3.5 rounded-xl bg-amber-50 border border-amber-200">
                <p class="text-xs text-amber-800 font-medium leading-relaxed">
                    ⚕️ <strong>Disclaimer:</strong> This is AI-powered guidance only and does not constitute medical advice or diagnosis. Please consult a qualified healthcare professional for proper evaluation.
                </p>
            </div>

            <!-- Action buttons -->
            <div class="mt-4 pt-4 border-t border-surface-100 flex gap-3">
                <button onclick="newConsultation()" class="flex-1 py-2.5 rounded-xl border border-surface-200 text-surface-600 font-semibold text-sm hover:bg-surface-50 transition-all">
                    New Consultation
                </button>
                <button onclick="printClinicalSummary()" class="flex-1 py-2.5 rounded-xl bg-brand-600 text-white font-semibold text-sm hover:bg-brand-500 transition-all flex items-center justify-center gap-2 active:scale-95">
                    <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
                    Print Summary
                </button>
            </div>
        </div>
    `;
    return card;
}

// ─── Print Clinical Summary ───────────────────────────────────────────────────

function printClinicalSummary() {
    const data = lastAnalysisData;
    if (!data) {
        alert('No analysis available yet. Please complete a consultation first.');
        return;
    }

    const risk        = data.risk || {};
    const specialists = data.specialists || [];
    const sections    = data.sections || {};
    const symptoms    = sections.symptom_summary || [];
    const lifestyle   = sections.lifestyle_advice || {};
    const meta        = data.analysis_meta || {};

    // Deduplicate lifestyle tips
    const allTips = [];
    const tipsSeen = new Set();
    Object.values(lifestyle).forEach(arr => arr.forEach(t => {
        if (!tipsSeen.has(t)) { tipsSeen.add(t); allTips.push(t); }
    }));

    // Build Q&A from tracked conversation history
    // Clara[0] = greeting, lastClara = analysis intro — keep the middle as follow-up Qs
    const patientMsgs    = conversationHistory.filter(m => m.role === 'patient');
    const claraMsgs      = conversationHistory.filter(m => m.role === 'clara');
    const chiefComplaint = patientMsgs[0]?.text || 'Not recorded';
    const followUpQA     = claraMsgs.slice(1, -1).map((q, i) => ({
        question : q.text,
        answer   : patientMsgs[i + 1]?.text || '—'
    }));

    // HTML escape helper (local, for the print document)
    const esc = s => s ? String(s)
        .replace(/&/g,'&amp;').replace(/</g,'&lt;')
        .replace(/>/g,'&gt;').replace(/"/g,'&quot;') : '';

    const riskPalette = { low:'#059669', medium:'#d97706', high:'#dc2626', none:'#64748b' };
    const riskColor   = riskPalette[risk.level] || riskPalette.none;
    const riskIcon    = risk.level === 'high' ? '🚨' : risk.level === 'medium' ? '⚠️' : '✅';
    const now         = new Date();
    const dateStr     = now.toLocaleDateString('en-US', { weekday:'long', year:'numeric', month:'long', day:'numeric' });
    const timeStr     = now.toLocaleTimeString('en-US', { hour:'2-digit', minute:'2-digit' });

    const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ClariCare Clinical Summary</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;font-size:12px;line-height:1.65;color:#1a1a1a;background:#fff;padding:44px;max-width:820px;margin:0 auto}
.doc-header{display:flex;align-items:flex-start;justify-content:space-between;border-bottom:3px solid #059669;padding-bottom:18px;margin-bottom:28px}
.brand{display:flex;align-items:center;gap:10px}
.brand-dot{width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,#10b981,#34d399);display:flex;align-items:center;justify-content:center;font-size:20px}
.brand-name{font-size:22px;font-weight:800;color:#064e3b;letter-spacing:-0.5px}
.brand-sub{font-size:9px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:1.2px}
.meta-title{font-weight:800;font-size:15px;color:#059669;text-transform:uppercase;letter-spacing:0.5px;text-align:right}
.meta-info{font-size:10px;color:#64748b;margin-top:4px;text-align:right}
.section{margin-bottom:24px}
.sec-hdr{font-size:9px;font-weight:900;text-transform:uppercase;letter-spacing:2px;color:#059669;border-bottom:1.5px solid #d1fae5;padding-bottom:5px;margin-bottom:12px}
.chief{background:#f8fafc;border-left:4px solid #059669;padding:13px 16px;border-radius:0 6px 6px 0;font-style:italic;color:#334155;font-size:13px;line-height:1.75}
.qa-item{margin-bottom:11px}
.qa-q{font-weight:700;color:#1e293b}
.qa-q::before{content:'Q  ';color:#059669;font-weight:900}
.qa-a{color:#334155;padding-left:20px;margin-top:3px}
.qa-a::before{content:'A  ';color:#94a3b8;font-weight:700}
.risk-box{padding:13px 16px;border-radius:8px;border:1.5px solid;display:flex;align-items:flex-start;gap:12px}
.risk-lbl{font-weight:800;font-size:14px}
.risk-desc{font-size:11px;color:#475569;margin-top:3px}
table{width:100%;border-collapse:collapse}
th{text-align:left;padding:7px 10px;font-size:9px;text-transform:uppercase;letter-spacing:1px;color:#64748b;background:#f8fafc;border-bottom:1px solid #e2e8f0;font-weight:700}
td{padding:8px 10px;border-bottom:1px solid #f1f5f9;font-size:11px;vertical-align:middle}
.bar-wrap{display:inline-block;background:#e2e8f0;width:56px;height:5px;border-radius:3px;vertical-align:middle;margin-right:6px;overflow:hidden}
.bar-fill{height:100%;border-radius:3px}
.spec-card{padding:11px 14px;border-radius:8px;margin-bottom:9px;border:1px solid}
.spec-name{font-weight:700;font-size:13px}
.spec-det{font-size:10px;color:#64748b;margin-top:3px}
.spec-maps{font-size:10px;color:#2563eb;margin-top:6px}
.tip{padding:7px 12px;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:6px;margin-bottom:6px;font-size:11px;color:#14532d}
.disclaimer{background:#fffbeb;border:1px solid #fde68a;padding:13px 16px;border-radius:8px;font-size:10px;color:#92400e;line-height:1.8}
.doc-footer{margin-top:28px;padding-top:14px;border-top:2px solid #e2e8f0;display:flex;justify-content:space-between;align-items:center;font-size:9px;color:#94a3b8}
.actions{text-align:center;padding:24px 0 0;border-top:1px dashed #e2e8f0;margin-top:26px}
.btn-print{background:#059669;color:#fff;border:none;padding:11px 32px;border-radius:8px;font-size:13px;font-weight:700;cursor:pointer;margin:0 6px}
.btn-close{background:#fff;color:#475569;border:1px solid #e2e8f0;padding:11px 32px;border-radius:8px;font-size:13px;font-weight:700;cursor:pointer;margin:0 6px}
@media print{.actions{display:none}body{padding:22px}}
</style>
</head>
<body>

<div class="doc-header">
  <div class="brand">
    <div class="brand-dot">🫀</div>
    <div>
      <div class="brand-name">ClariCare</div>
      <div class="brand-sub">AI Health Guidance Platform</div>
    </div>
  </div>
  <div>
    <div class="meta-title">Clinical Summary for Physician</div>
    <div class="meta-info">Generated: ${dateStr} at ${timeStr}</div>
    <div class="meta-info">AI Method: ${esc(meta.method || 'BERT + Keyword Hybrid')} &nbsp;·&nbsp; ${meta.symptoms_detected || 0} symptom(s) detected</div>
  </div>
</div>

<div class="section">
  <div class="sec-hdr">Chief Complaint</div>
  <div class="chief">&ldquo;${esc(chiefComplaint)}&rdquo;</div>
</div>

${followUpQA.length > 0 ? `
<div class="section">
  <div class="sec-hdr">Consultation History — Patient Responses to Follow-Up Questions</div>
  ${followUpQA.map(p => `
  <div class="qa-item">
    <div class="qa-q">${esc(p.question)}</div>
    <div class="qa-a">${esc(p.answer)}</div>
  </div>`).join('')}
</div>` : ''}

<div class="section">
  <div class="sec-hdr">AI Risk Assessment</div>
  <div class="risk-box" style="background:${riskColor}14;border-color:${riskColor}55">
    <div style="font-size:22px;margin-top:1px">${riskIcon}</div>
    <div>
      <div class="risk-lbl" style="color:${riskColor}">${esc(risk.label || 'Unknown Risk')}</div>
      <div class="risk-desc">${esc(risk.urgency || '')}</div>
    </div>
  </div>
</div>

${symptoms.length > 0 ? `
<div class="section">
  <div class="sec-hdr">Detected Symptoms</div>
  <table>
    <thead><tr><th>Symptom</th><th>Detection Method</th><th>AI Confidence</th></tr></thead>
    <tbody>
      ${symptoms.slice(0, 8).map(s => `
      <tr>
        <td><strong>${esc(s.symptom)}</strong></td>
        <td style="color:#64748b">${esc(s.method || '—')}</td>
        <td>
          <span class="bar-wrap"><span class="bar-fill" style="width:${Math.round(s.confidence * 100)}%;background:${s.confidence >= 0.8 ? '#10b981' : s.confidence >= 0.6 ? '#f59e0b' : '#ef4444'}"></span></span>
          ${Math.round(s.confidence * 100)}%
        </td>
      </tr>`).join('')}
    </tbody>
  </table>
</div>` : ''}

${specialists.length > 0 ? `
<div class="section">
  <div class="sec-hdr">Recommended Specialists</div>
  ${specialists.slice(0, 3).map((sp, i) => `
  <div class="spec-card" style="background:${i === 0 ? '#f0fdf4' : '#f8fafc'};border-color:${i === 0 ? '#bbf7d0' : '#e2e8f0'}">
    <div style="display:flex;align-items:center;gap:9px">
      <span style="font-size:20px">${sp.icon || '🩺'}</span>
      <div>
        <div class="spec-name">${esc(sp.name)}${i === 0 ? ' <span style="background:#059669;color:#fff;font-size:8px;padding:2px 7px;border-radius:10px;margin-left:5px;vertical-align:middle">PRIMARY</span>' : ''}</div>
        <div class="spec-det">Recommended for: ${sp.symptoms.slice(0, 5).map(s => esc(s)).join(', ')}</div>
      </div>
    </div>
    <div class="spec-maps">🔍 Find nearby: google.com/maps/search/${encodeURIComponent(sp.name + ' near me')}</div>
  </div>`).join('')}
</div>` : ''}

${allTips.length > 0 ? `
<div class="section">
  <div class="sec-hdr">Lifestyle &amp; Self-Care Recommendations</div>
  ${allTips.slice(0, 6).map(t => `<div class="tip">🌿&nbsp; ${esc(t)}</div>`).join('')}
</div>` : ''}

<div class="disclaimer">
  <strong>⚕️ Medical Disclaimer:</strong> This clinical summary was generated by ClariCare, an AI-powered health guidance platform. It does <strong>not</strong> constitute a medical diagnosis, treatment plan, or prescription. This document is intended solely as a conversational aid to help communicate symptoms to a qualified healthcare professional. Always consult a licensed physician for proper medical evaluation and advice. In a medical emergency, contact emergency services immediately.
</div>

<div class="doc-footer">
  <span>ClariCare v2 &nbsp;·&nbsp; AI Health Guidance Platform</span>
  <span>For informational purposes only &nbsp;·&nbsp; Not a substitute for professional medical advice</span>
</div>

<div class="actions">
  <button class="btn-print" onclick="window.print()">🖨️&nbsp; Print / Save as PDF</button>
  <button class="btn-close" onclick="window.close()">✕ Close</button>
</div>

</body></html>`;

    const win = window.open('', '_blank', 'width=920,height=720,scrollbars=yes,resizable=yes');
    win.document.write(html);
    win.document.close();
    win.focus();
}

// ─── Quick Replies ────────────────────────────────────────────────────────────

function showQuickReplies(replies) {
    if (!replies || replies.length === 0) return;
    const bar = document.getElementById('quick-replies-bar');
    bar.innerHTML = '';
    bar.classList.remove('hidden');
    replies.forEach(reply => {
        const btn = document.createElement('button');
        btn.className = 'quick-reply-chip';
        btn.textContent = reply;
        btn.onclick = () => sendMessage(reply);
        bar.appendChild(btn);
    });
}

function clearQuickReplies() {
    const bar = document.getElementById('quick-replies-bar');
    bar.innerHTML = '';
    bar.classList.add('hidden');
}

// ─── Typing Indicator ─────────────────────────────────────────────────────────

function setTypingIndicator(show) {
    const area = document.getElementById('messages-area');
    const existing = document.getElementById('typing-indicator');
    const sendBtn = document.getElementById('send-btn');

    if (show && !existing) {
        const div = document.createElement('div');
        div.id = 'typing-indicator';
        div.className = 'flex items-end gap-2.5 message-enter';
        div.innerHTML = `
            <div class="w-9 h-9 rounded-full bg-gradient-to-br from-brand-500 to-emerald-400 flex items-center justify-center flex-shrink-0 shadow-md shadow-brand-500/20">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
            </div>
            <div class="chat-bubble-bot py-3.5 px-5 inline-flex items-center gap-1.5">
                <div class="typing-dot" style="animation-delay:0s"></div>
                <div class="typing-dot" style="animation-delay:0.15s"></div>
                <div class="typing-dot" style="animation-delay:0.3s"></div>
            </div>
        `;
        area.appendChild(div);
        sendBtn.disabled = true;
        scrollToBottom();
    } else if (!show && existing) {
        existing.remove();
        sendBtn.disabled = false;
    }
}

// ─── Emergency Alert ──────────────────────────────────────────────────────────

function showEmergencyAlert() {
    document.getElementById('emergency-alert').classList.remove('hidden');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── Error Message ────────────────────────────────────────────────────────────

function appendErrorMessage(msg) {
    const area = document.getElementById('messages-area');
    const div = document.createElement('div');
    div.className = 'flex justify-center message-enter';
    div.innerHTML = `
        <div class="max-w-sm bg-red-50 border border-red-200 rounded-xl px-5 py-4 text-sm shadow-sm">
            <p class="text-red-700 font-semibold mb-1">Connection Error</p>
            <p class="text-red-600 font-medium text-xs leading-relaxed">${escapeHtml(msg)}</p>
        </div>
    `;
    area.appendChild(div);
    scrollToBottom();
}

// ─── Health Check ─────────────────────────────────────────────────────────────

async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE}/api/health`);
        const data = await res.json();
        const badge = document.getElementById('status-badge');
        const modeLabel = document.getElementById('mode-label');
        if (data.status === 'healthy') {
            badge.className = 'flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-200';
            badge.innerHTML = `
                <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                <span class="text-xs text-emerald-700 font-bold">${data.bert_available ? 'BERT Ready' : 'Keyword Mode'}</span>
            `;
            if (modeLabel) modeLabel.textContent = data.nlp_method || 'BERT + Keyword';
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

function scrollToBottom() {
    const area = document.getElementById('messages-area');
    setTimeout(() => area.scrollTo({ top: area.scrollHeight, behavior: 'smooth' }), 60);
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function getCurrentTime() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function escapeHtml(str) {
    if (!str) return '';
    const d = document.createElement('div');
    d.textContent = String(str);
    return d.innerHTML;
}

function nl2br(str) {
    return str.replace(/\n/g, '<br>');
}

function formatMarkdown(str) {
    if (!str) return '';
    return String(str)
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');
}

function getRiskColors(level) {
    const map = {
        low:    { bg:'bg-emerald-50', border:'border-emerald-200', text:'text-emerald-700', badge:'bg-emerald-100 text-emerald-800 border-emerald-200', icon:'✅' },
        medium: { bg:'bg-amber-50',   border:'border-amber-200',   text:'text-amber-700',   badge:'bg-amber-100 text-amber-800 border-amber-200',   icon:'⚠️' },
        high:   { bg:'bg-red-50',     border:'border-red-200',     text:'text-red-700',     badge:'bg-red-100 text-red-800 border-red-200',     icon:'🚨' },
        none:   { bg:'bg-surface-50', border:'border-surface-200', text:'text-surface-600', badge:'bg-surface-100 text-surface-700 border-surface-200', icon:'❓' }
    };
    return map[level] || map.none;
}
