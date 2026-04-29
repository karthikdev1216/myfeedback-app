const API_URL = 'http://localhost:5000/submit-feedback';

const feedbackForm = document.getElementById('feedbackForm');
const successMessage = document.getElementById('successMessage');
const submitBtn = document.getElementById('submitBtn');
const errorToast = document.getElementById('errorMessage');

feedbackForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Disable button and show loader
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;

    const formData = new FormData(feedbackForm);
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        rating: parseInt(formData.get('rating')),
        experience: formData.get('experience')
    };

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (response.ok) {
            showSuccess();
        } else {
            showError(result.error || 'Something went wrong. Please try again.');
        }
    } catch (error) {
        showError('Could not connect to the server. Is it running?');
        console.error('Submission error:', error);
    } finally {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
});

function showSuccess() {
    feedbackForm.classList.add('hidden');
    successMessage.classList.remove('hidden');
}

function resetForm() {
    feedbackForm.reset();
    successMessage.classList.add('hidden');
    feedbackForm.classList.remove('hidden');
}

function showError(message) {
    errorToast.textContent = message;
    errorToast.classList.remove('hidden');
    
    setTimeout(() => {
        errorToast.classList.add('hidden');
    }, 5000);
}

// Simple debounce for submit button
let lastSubmit = 0;
const SUBMIT_COOLDOWN = 2000; // 2 seconds

feedbackForm.addEventListener('submit', (e) => {
    const now = Date.now();
    if (now - lastSubmit < SUBMIT_COOLDOWN) {
        e.preventDefault();
        e.stopImmediatePropagation();
        showError('Please wait a moment before submitting again.');
        return;
    }
    lastSubmit = now;
}, true);
