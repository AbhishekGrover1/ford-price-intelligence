const form = document.getElementById('predict-form');
const submitBtn = document.getElementById('submit-btn');
const resultBox = document.getElementById('result');
const resultValue = document.getElementById('result-value');
const errorBox = document.getElementById('error');

// Relative path: works because this file is served by the same FastAPI
// app that exposes /api/predict (the default setup for this project).
// Point this at a full URL instead only if you host the frontend
// somewhere separate from the API.
const API_BASE = '';

const currency = new Intl.NumberFormat('en-GB', {
  style: 'currency',
  currency: 'GBP',
  maximumFractionDigits: 0,
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    model: document.getElementById('model').value,
    year: Number(document.getElementById('year').value),
    transmission: document.getElementById('transmission').value,
    mileage: Number(document.getElementById('mileage').value),
    fuelType: document.getElementById('fuelType').value,
    tax: Number(document.getElementById('tax').value),
    mpg: Number(document.getElementById('mpg').value),
    engineSize: Number(document.getElementById('engineSize').value),
  };

  setLoading(true);
  hideError();

  try {
    const response = await fetch(`${API_BASE}/api/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const body = await response.json().catch(() => null);
      throw new Error((body && body.detail) || 'Request failed.');
    }

    const data = await response.json();
    showResult(data.predicted_price);
  } catch (err) {
    showError("Couldn't get an estimate. Please try again.");
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  submitBtn.textContent = isLoading ? 'Estimating…' : 'Estimate Price';
}

function showResult(price) {
  resultValue.textContent = currency.format(price);
  resultBox.hidden = false;
  resultBox.classList.remove('result--enter');
  // Force a reflow so the animation restarts on repeated submissions.
  void resultBox.offsetWidth;
  resultBox.classList.add('result--enter');
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.hidden = false;
  resultBox.hidden = true;
}

function hideError() {
  errorBox.hidden = true;
}
