
document.getElementById('merge-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const filesInput = document.getElementById('merge-files');
    const files = filesInput.files;
    if (files.length < 2) {
        alert('Please select at least two PDF files to merge.');
        return;
    }
    const formData = new FormData();
    for (const file of files) {
        formData.append('files', file);
    }
    const response = await fetch('/merge', {
        method: 'POST',
        body: formData,
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('merge-download');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    } else {
        const error = await response.json();
        alert('Error: ' + error.error);
    }
});

document.getElementById('split-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('split-file');
    const pageNumberInput = document.getElementById('split-page-number');
    const file = fileInput.files[0];
    const pageNumber = pageNumberInput.value;
    if (!file) {
        alert('Please select a PDF file to split.');
        return;
    }
    if (!pageNumber || pageNumber < 1) {
        alert('Please enter a valid page number.');
        return;
    }
    const formData = new FormData();
    formData.append('file', file);
    formData.append('page_number', pageNumber);
    const response = await fetch('/split', {
        method: 'POST',
        body: formData,
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('split-download');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    } else {
        const error = await response.json();
        alert('Error: ' + error.error);
    }
});

document.getElementById('compress-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('compress-file');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a PDF file to compress.');
        return;
    }
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch('/compress', {
        method: 'POST',
        body: formData,
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('compress-download');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    } else {
        const error = await response.json();
        alert('Error: ' + error.error);
    }
});

document.getElementById('pdf-to-word-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('pdf-to-word-file');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a PDF file to convert to Word.');
        return;
    }
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch('/pdf-to-word', {
        method: 'POST',
        body: formData,
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('pdf-to-word-download');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    } else {
        const error = await response.json();
        alert('Error: ' + error.error);
    }
});

document.getElementById('word-to-pdf-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('word-to-pdf-file');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a Word file to convert to PDF.');
        return;
    }
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch('/word-to-pdf', {
        method: 'POST',
        body: formData,
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('word-to-pdf-download');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    } else {
        const error = await response.json();
        alert('Error: ' + error.error);
    }
});

document.getElementById('pdf-to-jpg-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('pdf-to-jpg-file');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a PDF file to convert to JPG.');
        return;
    }
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch('/pdf-to-jpg', {
        method: 'POST',
        body: formData,
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('pdf-to-jpg-download');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    } else {
        const error = await response.json();
        alert('Error: ' + error.error);
    }
});

document.getElementById('jpg-to-pdf-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const filesInput = document.getElementById('jpg-to-pdf-files');
    const files = filesInput.files;
    if (files.length === 0) {
        alert('Please select JPG/PNG images to convert to PDF.');
        return;
    }
    const formData = new FormData();
    for (const file of files) {
        formData.append('files', file);
    }
    const response = await fetch('/jpg-to-pdf', {
        method: 'POST',
        body: formData,
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('jpg-to-pdf-download');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    } else {
        const error = await response.json();
        alert('Error: ' + error.error);
    }
});

document.getElementById('sign-pdf-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    alert('Sign PDF feature is not implemented yet.');
});

document.getElementById('watermark-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('watermark-file');
    const watermarkInput = document.getElementById('watermark-watermark');
    const file = fileInput.files[0];
    const watermark = watermarkInput.files[0];
    if (!file || !watermark) {
        alert('Please select both PDF and watermark PDF files.');
        return;
    }
    const formData = new FormData();
    formData.append('file', file);
    formData.append('watermark', watermark);
    const response = await fetch('/watermark', {
        method: 'POST',
        body: formData,
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('watermark-download');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    } else {
        const error = await response.json();
        alert('Error: ' + error.error);
    }
});

document.getElementById('rotate-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('rotate-file');
    const directionSelect = document.getElementById('rotate-direction');
    const file = fileInput.files[0];
    const direction = directionSelect.value;
    if (!file) {
        alert('Please select a PDF file to rotate.');
        return;
    }
    if (!direction) {
        alert('Please select a rotation direction.');
        return;
    }
    const formData = new FormData();
    formData.append('file', file);
    formData.append('direction', direction);
    const response = await fetch('/rotate', {
        method: 'POST',
        body: formData,
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('rotate-download');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    } else {
        const error = await response.json();
        alert('Error: ' + error.error);
    }
});

document.getElementById('unlock-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('unlock-file');
    const passwordInput = document.getElementById('unlock-password');
    const file = fileInput.files[0];
    const password = passwordInput.value;
    if (!file) {
        alert('Please select a PDF file to unlock.');
        return;
    }
    const formData = new FormData();
    formData.append('file', file);
    formData.append('password', password);
    const response = await fetch('/unlock', {
        method: 'POST',
        body: formData,
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('unlock-download');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    } else {
        const error = await response.json();
        alert('Error: ' + error.error);
    }
});

document.getElementById('protect-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('protect-file');
    const passwordInput = document.getElementById('protect-password');
    const file = fileInput.files[0];
    const password = passwordInput.value;
    if (!file) {
        alert('Please select a PDF file to protect.');
        return;
    }
    if (!password) {
        alert('Please enter a password to protect the PDF.');
        return;
    }
    const formData = new FormData();
    formData.append('file', file);
    formData.append('password', password);
    const response = await fetch('/protect', {
        method: 'POST',
        body: formData,
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('protect-download');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    } else {
        const error = await response.json();
        alert('Error: ' + error.error);
    }
});

document.getElementById('organize-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('organize-file');
    const orderInput = document.getElementById('organize-order');
    const file = fileInput.files[0];
    const order = orderInput.value;
    if (!file) {
        alert('Please select a PDF file to organize.');
        return;
    }
    if (!order) {
        alert('Please enter the page order.');
        return;
    }
    const formData = new FormData();
    formData.append('file', file);
    formData.append('order', order);
    const response = await fetch('/organize', {
        method: 'POST',
        body: formData,
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('organize-download');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    } else {
        const error = await response.json();
        alert('Error: ' + error.error);
    }
});

document.getElementById('add-page-numbers-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    alert('Add page numbers feature is not implemented yet.');
});

document.getElementById('crop-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('crop-file');
    const leftInput = document.getElementById('crop-left');
    const bottomInput = document.getElementById('crop-bottom');
    const rightInput = document.getElementById('crop-right');
    const topInput = document.getElementById('crop-top');
    const file = fileInput.files[0];
    const left = leftInput.value;
    const bottom = bottomInput.value;
    const right = rightInput.value;
    const top = topInput.value;
    if (!file) {
        alert('Please select a PDF file to crop.');
        return;
    }
    if (!left || !bottom || !right || !top) {
        alert('Please enter all crop coordinates.');
        return;
    }
    const formData = new FormData();
    formData.append('file', file);
    formData.append('left', left);
    formData.append('bottom', bottom);
    formData.append('right', right);
    formData.append('top', top);
    const response = await fetch('/crop', {
        method: 'POST',
        body: formData,
    });
    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('crop-download');
        downloadLink.href = url;
        downloadLink.style.display = 'block';
    } else {
        const error = await response.json();
        alert('Error: ' + error.error);
    }
});

const themeToggleBtn = document.getElementById('theme-toggle');
const currentTheme = localStorage.getItem('theme') || 'light';

function applyTheme(theme) {
    if (theme === 'dark') {
        document.body.classList.add('dark-theme');
        themeToggleBtn.textContent = '☀️';
    } else {
        document.body.classList.remove('dark-theme');
        themeToggleBtn.textContent = '🌙';
    }
    localStorage.setItem('theme', theme);
}

applyTheme(currentTheme);

themeToggleBtn.addEventListener('click', () => {
    const newTheme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
    applyTheme(newTheme);
});
