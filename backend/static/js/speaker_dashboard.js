// Speaker Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    initializeDashboard();
    
    // Set up event listeners
    setupEventListeners();
    
    // Load initial data
    loadDashboardData();
});

function initializeDashboard() {
    // Show sessions section by default
    showSection('sessions');
    
    // Initialize navigation
    initializeNavigation();
}

function setupEventListeners() {
    // Navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('href').substring(1);
            showSection(sectionId);
            updateActiveNav(this);
        });
    });
    
    // New session button
    const newSessionBtn = document.getElementById('new-session-btn');
    if (newSessionBtn) {
        newSessionBtn.addEventListener('click', function() {
            showNewSessionModal();
        });
    }
    
    // New session form
    const newSessionForm = document.getElementById('new-session-form');
    if (newSessionForm) {
        newSessionForm.addEventListener('submit', handleNewSessionSubmit);
    }
    
    // Session action buttons
    document.addEventListener('click', function(e) {
        if (e.target.closest('[data-action]')) {
            const action = e.target.closest('[data-action]').dataset.action;
            const sessionId = e.target.closest('[data-session-id]')?.dataset.sessionId;
            handleSessionAction(action, sessionId);
        }
    });
}

function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('href').substring(1);
            showSection(sectionId);
            updateActiveNav(this);
        });
    });
}

function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.dashboard-section').forEach(section => {
        section.classList.add('hidden');
    });
    
    // Show selected section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.remove('hidden');
        targetSection.classList.add('fade-in');
    }
}

function updateActiveNav(activeLink) {
    // Remove active class from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('bg-blue-50', 'text-blue-600');
        link.classList.add('hover:bg-gray-50', 'text-gray-600');
    });
    
    // Add active class to clicked link
    activeLink.classList.add('bg-blue-50', 'text-blue-600');
    activeLink.classList.remove('hover:bg-gray-50', 'text-gray-600');
}

function showNewSessionModal() {
    const modal = document.getElementById('new-session-modal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function closeModal() {
    const modal = document.getElementById('new-session-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

async function handleNewSessionSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        title: formData.get('title'),
        abstract: formData.get('abstract'),
        category: formData.get('category'),
        track: formData.get('track')
    };
    
    try {
        const response = await fetch('/speaker/sessions/new', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('Session submitted successfully!', 'success');
            closeModal();
            e.target.reset();
            loadDashboardData(); // Reload data
        } else {
            showNotification(result.message || 'Failed to submit session', 'error');
        }
    } catch (error) {
        console.error('Error submitting session:', error);
        showNotification('An error occurred while submitting the session', 'error');
    }
}

async function handleSessionAction(action, sessionId) {
    if (!sessionId) return;
    
    try {
        let response;
        
        switch (action) {
            case 'view':
                response = await fetch(`/speaker/sessions/${sessionId}/details`);
                const sessionData = await response.json();
                if (sessionData.success) {
                    showSessionDetails(sessionData.session);
                }
                break;
                
            case 'edit':
                showEditSessionModal(sessionId);
                break;
                
            case 'confirm':
                response = await fetch(`/speaker/sessions/${sessionId}/confirm`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ status: 'confirmed' })
                });
                const confirmResult = await response.json();
                if (confirmResult.success) {
                    showNotification('Session confirmed successfully!', 'success');
                    loadDashboardData();
                }
                break;
                
            case 'decline':
                response = await fetch(`/speaker/sessions/${sessionId}/confirm`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ status: 'declined' })
                });
                const declineResult = await response.json();
                if (declineResult.success) {
                    showNotification('Session declined', 'info');
                    loadDashboardData();
                }
                break;
        }
    } catch (error) {
        console.error('Error handling session action:', error);
        showNotification('An error occurred', 'error');
    }
}

function showSessionDetails(session) {
    // Create and show session details modal
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="bg-white rounded-lg w-full max-w-2xl p-6">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-2xl font-bold text-gray-800">Session Details</h3>
                <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-gray-600">
                    <i class="fas fa-times text-xl"></i>
                </button>
            </div>
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">Title</label>
                    <p class="text-gray-900">${session.title}</p>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Abstract</label>
                    <p class="text-gray-900">${session.abstract}</p>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Category</label>
                        <p class="text-gray-900">${session.category}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Track</label>
                        <p class="text-gray-900">${session.track}</p>
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Status</label>
                    <span class="px-3 py-1 rounded-full text-sm ${
                        session.status === 'approved' ? 'bg-green-100 text-green-800' :
                        session.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                    }">${session.status}</span>
                </div>
                ${session.timeslot ? `
                <div>
                    <label class="block text-sm font-medium text-gray-700">Time Slot</label>
                    <p class="text-gray-900">${session.timeslot}</p>
                </div>
                ` : ''}
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

async function loadDashboardData() {
    try {
        // Load sessions
        const sessionsResponse = await fetch('/speaker/sessions');
        if (sessionsResponse.ok) {
            const sessionsData = await sessionsResponse.json();
            updateSessionsDisplay(sessionsData.sessions);
        }
        
        // Load certificates
        const certificatesResponse = await fetch('/speaker/certificates');
        if (certificatesResponse.ok) {
            const certificatesData = await certificatesResponse.json();
            updateCertificatesDisplay(certificatesData.certificates);
        }
        
        // Load QR codes
        loadQRCodes();
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function updateSessionsDisplay(sessions) {
    const sessionsContainer = document.querySelector('#sessions .grid');
    if (!sessionsContainer) return;
    
    sessionsContainer.innerHTML = sessions.map(session => `
        <div class="bg-white rounded-lg shadow-sm p-6 transform hover:scale-[1.02] transition-transform" data-session-id="${session.id}">
            <div class="flex justify-between items-start mb-4">
                <h3 class="text-xl font-semibold text-gray-800">${session.title}</h3>
                <span class="px-3 py-1 rounded-full text-sm ${
                    session.status === 'approved' ? 'bg-green-100 text-green-800' :
                    session.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                }">${session.status}</span>
            </div>
            <p class="text-gray-600 mb-4">${session.abstract.substring(0, 200)}...</p>
            <div class="flex flex-wrap gap-4 text-sm text-gray-500 mb-4">
                <span class="flex items-center">
                    <i class="fas fa-tag mr-2"></i>${session.track}
                </span>
                <span class="flex items-center">
                    <i class="fas fa-calendar mr-2"></i>${session.category}
                </span>
                ${session.timeslot ? `
                <span class="flex items-center">
                    <i class="fas fa-clock mr-2"></i>${session.timeslot}
                </span>
                ` : ''}
            </div>
            <div class="flex items-center justify-end space-x-3">
                <button data-action="view" class="text-gray-600 hover:text-blue-600 transition-colors">
                    <i class="fas fa-eye"></i>
                </button>
                ${session.status === 'pending' ? `
                <button data-action="edit" class="text-gray-600 hover:text-blue-600 transition-colors">
                    <i class="fas fa-edit"></i>
                </button>
                ` : ''}
                ${session.status === 'approved' ? `
                <button data-action="confirm" class="text-green-600 hover:text-green-800 transition-colors">
                    <i class="fas fa-check"></i>
                </button>
                <button data-action="decline" class="text-red-600 hover:text-red-800 transition-colors">
                    <i class="fas fa-times"></i>
                </button>
                ` : ''}
            </div>
        </div>
    `).join('');
}

function updateCertificatesDisplay(certificates) {
    const certificatesContainer = document.querySelector('#certificates .grid');
    if (!certificatesContainer) return;
    
    certificatesContainer.innerHTML = certificates.map(cert => `
        <div class="bg-gray-50 p-4 rounded-lg">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                    <div class="bg-purple-100 text-purple-600 p-3 rounded-lg">
                        <i class="fas fa-certificate text-xl"></i>
                    </div>
                    <div>
                        <h3 class="font-semibold text-gray-800">Speaker Certificate</h3>
                        <p class="text-sm text-gray-500">Issued on ${new Date(cert.generated_at).toLocaleDateString()}</p>
                    </div>
                </div>
                <a href="/static/${cert.image_path}" class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors" download>
                    <i class="fas fa-download mr-2"></i>Download
                </a>
            </div>
        </div>
    `).join('');
}

function loadQRCodes() {
    // QR codes are loaded via static files in the template
    // This function can be used to refresh QR codes if needed
    const checkinQR = document.querySelector('#qrcodes img[alt="Check-in QR Code"]');
    const tshirtQR = document.querySelector('#qrcodes img[alt="T-shirt QR Code"]');
    
    if (checkinQR) {
        checkinQR.src = `/speaker/qrcodes/checkin?t=${Date.now()}`;
    }
    if (tshirtQR) {
        tshirtQR.src = `/speaker/qrcodes/tshirt?t=${Date.now()}`;
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg ${
        type === 'success' ? 'bg-green-500 text-white' :
        type === 'error' ? 'bg-red-500 text-white' :
        type === 'warning' ? 'bg-yellow-500 text-white' :
        'bg-blue-500 text-white'
    }`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Global functions for template use
window.closeModal = closeModal;
window.showNotification = showNotification;