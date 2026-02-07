/**
 * AI WhatsApp Automation Logic
 * Handles validation, formatting, and sequential redirection
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const messageInput = document.getElementById('message-input');
    const countryCodeInput = document.getElementById('country-code');
    const phoneListInput = document.getElementById('phone-list');
    const sendBtn = document.getElementById('send-all-btn');
    const contactCountDisplay = document.getElementById('contact-count');
    const validationStatus = document.getElementById('validation-status');
    const statusSection = document.getElementById('status-section');
    const executionLog = document.getElementById('execution-log');
    const closeLogBtn = document.getElementById('close-log');

    // State
    let validatedNumbers = [];

    /**
     * Parse and validate phone numbers from the textarea
     */
    function validateNumbers() {
        const defaultCC = countryCodeInput.value || '91';
        const lines = phoneListInput.value.split('\n');
        validatedNumbers = [];

        lines.forEach(line => {
            // Remove all non-numeric characters except +
            let cleaned = line.replace(/[^\d+]/g, '');
            if (!cleaned) return;

            // If it's 10 digits, prepend default country code
            if (cleaned.length === 10 && !cleaned.startsWith('+')) {
                cleaned = defaultCC + cleaned;
            }

            // Remove leading + for the final URL
            cleaned = cleaned.replace('+', '');

            // Basic international length check (7 to 15 digits)
            if (cleaned.length >= 7 && cleaned.length <= 15) {
                validatedNumbers.push({
                    original: line.trim(),
                    formatted: cleaned
                });
            }
        });

        // Update UI
        contactCountDisplay.textContent = `${validatedNumbers.length} Recipients`;
        if (validatedNumbers.length > 0) {
            validationStatus.textContent = 'All numbers validated';
            validationStatus.className = 'status-success';
        } else {
            validationStatus.textContent = 'Enter valid numbers (one per line)';
            validationStatus.className = 'status-neutral';
        }
    }

    /**
     * Handle the Send All operation
     */
    function sendDirectly() {
        const message = messageInput.value.trim();

        // 1. Validate inputs
        if (!message) {
            showToast('⚠️ Please enter a message content.', 'error');
            messageInput.focus();
            return;
        }

        if (validatedNumbers.length === 0) {
            showToast('⚠️ Please enter at least one valid phone number.', 'error');
            phoneListInput.focus();
            return;
        }

        // 2. Prepare Log Section
        statusSection.style.display = 'block';
        executionLog.innerHTML = '';
        statusSection.scrollIntoView({ behavior: 'smooth' });

        // 3. Process Numbers
        /**
         * Browser interaction model: 
         * Automatically opening many tabs is blocked by default popup blockers.
         * We provide a guided "Send" list where users can click individual links,
         * ensuring the highest success rate and following professional tool standards.
         */
        validatedNumbers.forEach((num, index) => {
            const waUrl = `https://wa.me/${num.formatted}?text=${encodeURIComponent(message)}`;

            const logItem = document.createElement('div');
            logItem.className = 'log-item';
            logItem.innerHTML = `
                <span><strong>${index + 1}.</strong> ${num.formatted}</span>
                <a href="${waUrl}" target="_blank" class="log-btn-small">Open WhatsApp</a>
            `;
            executionLog.appendChild(logItem);

            // For the first number, we can try to trigger it immediately if only one
            if (validatedNumbers.length === 1 && index === 0) {
                window.open(waUrl, '_blank');
            }
        });

        if (validatedNumbers.length > 1) {
            showToast(`🚀 Generated ${validatedNumbers.length} links. Click to send!`, 'success');
        } else {
            showToast(`✅ Redirecting to WhatsApp...`, 'success');
        }
    }

    /**
     * Toast notification system
     */
    function showToast(text, type = 'success') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.style.cssText = `
            background: ${type === 'success' ? 'var(--primary-green)' : '#ff5e5e'};
            color: ${type === 'success' ? '#000' : '#fff'};
            padding: 12px 24px;
            border-radius: 12px;
            margin-top: 10px;
            font-weight: 600;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            animation: slideIn 0.3s ease-out;
            pointer-events: auto;
        `;
        toast.textContent = text;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(20px)';
            toast.style.transition = '0.3s';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Event Listeners
    phoneListInput.addEventListener('input', validateNumbers);
    countryCodeInput.addEventListener('input', validateNumbers);
    sendBtn.addEventListener('click', sendDirectly);
    closeLogBtn.addEventListener('click', () => statusSection.style.display = 'none');

    // Add CSS for toast and animation keyframes
    const style = document.createElement('style');
    style.innerHTML = `
        .toast-container {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(50px); }
            to { opacity: 1; transform: translateX(0); }
        }
    `;
    document.head.appendChild(style);
});