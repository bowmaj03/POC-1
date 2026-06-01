const sectionMessages = {
    causes: 'Causes selected: review root causes and potential triggers that lead to the hazard.',
    preventative: 'Preventative mitigation selected: examine controls and safeguards that stop the hazard from occurring.',
    hazard: 'Hazard selected: this is the central risk event to monitor and control.',
    corrective: 'Corrective mitigation selected: evaluate actions that reduce the impact if the hazard happens.',
    consequence: 'Consequence selected: understand the outcome if the hazard is not controlled.'
};

function highlightSection(section) {
    const bowtieItems = document.querySelectorAll('.bowtie-item');
    const detailCards = document.querySelectorAll('.detail-card');

    bowtieItems.forEach(item => {
        item.style.opacity = '0.7';
        item.style.filter = 'none';
    });

    detailCards.forEach(card => {
        card.style.backgroundColor = '#f9f9f9';
        card.style.borderLeftColor = '#0066cc';
        card.style.fontWeight = 'normal';
    });

    const element = document.getElementById(section);
    if (element) {
        element.style.opacity = '1';
        element.style.filter = 'drop-shadow(0 0 12px rgba(0, 102, 204, 0.8))';
    }

    const cardId = 'detail-' + section;
    const card = document.getElementById(cardId);
    if (card) {
        card.style.backgroundColor = '#e8f4ff';
        card.style.borderLeftColor = '#ff6b6b';
        card.style.fontWeight = 'bold';
    }

    const infoBox = document.getElementById('selected-info');
    if (infoBox) {
        infoBox.textContent = sectionMessages[section] || 'Section selected: click another section to explore more.';
    }
}

function resetHighlights() {
    document.querySelectorAll('.bowtie-item').forEach(item => {
        item.style.opacity = '0.7';
        item.style.filter = 'none';
    });

    document.querySelectorAll('.detail-card').forEach(card => {
        card.style.backgroundColor = '#f9f9f9';
        card.style.borderLeftColor = '#0066cc';
        card.style.fontWeight = 'normal';
    });

    const infoBox = document.getElementById('selected-info');
    if (infoBox) {
        infoBox.textContent = 'Hover over or click a section to see risk details here.';
    }
}

async function calculateRisk() {
    const responseBox = document.getElementById('risk-response');
    if (!responseBox) return;

    responseBox.textContent = 'Calculating risk score...';

    try {
        const response = await fetch('/calculate-risk');
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();
        responseBox.innerHTML = `
            <strong>Risk score:</strong> ${data.risk_score.toFixed(2)}<br>
            <strong>Likelihood:</strong> ${data.likelihood}<br>
            <strong>Impact:</strong> ${data.impact}<br>
            <strong>Level:</strong> ${data.risk_level}
        `;
    } catch (error) {
        responseBox.textContent = `Unable to contact Python service: ${error.message}`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.detail-card').forEach(card => {
        const sectionName = card.id.replace('detail-', '');

        card.addEventListener('mouseenter', () => {
            highlightSection(sectionName);
        });

        card.addEventListener('mouseleave', () => {
            resetHighlights();
        });
    });

    const calcButton = document.getElementById('calculate-risk-button');
    if (calcButton) {
        calcButton.addEventListener('click', calculateRisk);
    }

    resetHighlights();
});
