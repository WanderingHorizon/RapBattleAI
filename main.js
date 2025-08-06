// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('battle-form');
    const userInput = document.getElementById('user-rap-input');
    const battleLog = document.getElementById('battle-log');
    const loadingIndicator = document.getElementById('loading-indicator');
    const submitButton = form.querySelector('button');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const userRap = userInput.value.trim();
        if (!userRap) {
            // Maybe a less intrusive notification later, but alert is fine for now.
            alert('Please type your rap verse first!');
            return;
        }

        const rapper = document.getElementById('rapper-select').value;
        const mode = document.getElementById('mode-select').value;
        const beat = document.getElementById('beat-select').value;

        addMessage(userRap, 'You', 'user-message');
        userInput.value = '';

        loadingIndicator.style.display = 'flex';
        submitButton.disabled = true;
        submitButton.textContent = 'AI is Cooking...';

        try {
            const response = await fetch('/battle', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_rap: userRap, rapper, mode, beat }),
            });

            const data = await response.json();

            if (response.ok) {
                addMessage(data.ai_rap, rapper, 'ai-message');
            } else {
                addMessage(data.error || 'An unknown error occurred.', 'SYSTEM', 'error-message');
            }

        } catch (error) {
            console.error('Fetch Error:', error);
            addMessage('Could not connect to the server. Check your console and the Flask server terminal.', 'SYSTEM', 'error-message');
        } finally {
            loadingIndicator.style.display = 'none';
            submitButton.disabled = false;
            submitButton.textContent = 'Spit Bars!';
        }
    });

    function addMessage(text, author, messageClass) {
        const messageDiv = document.createElement('div');
        // The 'message' class is for base styling, the messageClass is for specific user/ai/system styling
        messageDiv.classList.add('message', messageClass);

        const authorSpan = document.createElement('span');
        authorSpan.classList.add('author');
        authorSpan.textContent = author;

        const paragraph = document.createElement('p');
        paragraph.innerHTML = text.replace(/\n/g, '<br>');

        messageDiv.appendChild(authorSpan);
        messageDiv.appendChild(paragraph);
        battleLog.appendChild(messageDiv);

        // Scroll to the latest message
        battleLog.scrollTop = battleLog.scrollHeight;
    }
});
