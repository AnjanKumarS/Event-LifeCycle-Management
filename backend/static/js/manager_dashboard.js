// Manager Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    initializeDashboard();
    
    // Set up event listeners
    setupEventListeners();
    
    // Load initial data
    loadDashboardData();
});

function initializeDashboard() {
    // Show submissions section by default
    showSection('submissions');
    
    // Initialize navigation
    initializeNavigation();
    
    // Initialize drag and drop for agenda builder
    initializeDragAndDrop();
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
    
    // Filter controls
    const trackFilter = document.getElementById('track-filter');
    const statusFilter = document.getElementById('status-filter');
    const searchInput = document.getElementById('search-input');
    
    if (trackFilter) {
        trackFilter.addEventListener('change', filterSubmissions);
    }
    if (statusFilter) {
        statusFilter.addEventListener('change', filterSubmissions);
    }
    if (searchInput) {
        searchInput.addEventListener('input', debounce(filterSubmissions, 300));
    }
    
    // Session action buttons
    document.addEventListener('click', function(e) {
        if (e.target.closest('[data-action]')) {
            const action = e.target.closest('[data-action]').dataset.action;
            const sessionId = e.target.closest('[data-session-id]')?.dataset.sessionId;
            handleSessionAction(action, sessionId);
        }
    });
    
    // Change request buttons
    document.addEventListener('click', function(e) {
        if (e.target.closest('[data-change-action]')) {
            const action = e.target.closest('[data-change-action]').dataset.changeAction;
            const requestId = e.target.closest('[data-request-id]')?.dataset.requestId;
            handleChangeRequest(action, requestId);
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
    
    // Load section-specific data
    switch (sectionId) {
        case 'submissions':
            loadSubmissions();
            break;
        case 'agenda':
            loadAgenda();
            break;
        case 'communications':
            loadCommunications();
            break;
        case 'speakers':
            loadSpeakers();
            break;
        case 'feedback':
            loadFeedback();
            break;
        case 'certificates':
            loadCertificates();
            break;
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

async function handleSessionAction(action, sessionId) {
    if (!sessionId) return;
    
    try {
        let response;
        
        switch (action) {
            case 'view':
                response = await fetch(`/manager/submissions/${sessionId}/view`);
                const sessionData = await response.json();
                if (sessionData.success) {
                    showSessionDetails(sessionData.session);
                }
                break;
                
            case 'approve':
            case 'reject':
            case 'hold':
                response = await fetch(`/manager/submissions/${sessionId}/${action}`, {
                    method: 'POST'
                });
                const result = await response.json();
                if (result.success) {
                    showNotification(`Session ${action}ed successfully!`, 'success');
                    loadSubmissions();
                } else {
                    showNotification(result.message || `Failed to ${action} session`, 'error');
                }
                break;
        }
    } catch (error) {
        console.error('Error handling session action:', error);
        showNotification('An error occurred', 'error');
    }
}

async function handleChangeRequest(action, requestId) {
    if (!requestId) return;
    
    try {
        const response = await fetch(`/manager/change-requests/${requestId}/${action}`, {
            method: 'POST'
        });
        
        const result = await response.json();
        if (result.success) {
            showNotification(`Change request ${action}ed successfully!`, 'success');
            loadChangeRequests();
        } else {
            showNotification(result.message || `Failed to ${action} change request`, 'error');
        }
    } catch (error) {
        console.error('Error handling change request:', error);
        showNotification('An error occurred', 'error');
    }
}

function showSessionDetails(session) {
    // Create and show session details modal
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="bg-white rounded-lg w-full max-w-4xl p-6 max-h-[90vh] overflow-y-auto">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-2xl font-bold text-gray-800">Session Details</h3>
                <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-gray-600">
                    <i class="fas fa-times text-xl"></i>
                </button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
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
                </div>
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Speaker</label>
                        <div class="bg-gray-50 p-4 rounded-lg">
                            <p class="font-semibold">${session.speaker.name}</p>
                            <p class="text-sm text-gray-600">${session.speaker.email}</p>
                            <p class="text-sm text-gray-600">${session.speaker.mobile}</p>
                        </div>
                    </div>
                    ${session.speaker2 ? `
                    <div>
                        <label class="block text-sm font-medium text-gray-700">Co-Speaker</label>
                        <div class="bg-gray-50 p-4 rounded-lg">
                            <p class="font-semibold">${session.speaker2.name}</p>
                            <p class="text-sm text-gray-600">${session.speaker2.email}</p>
                        </div>
                    </div>
                    ` : ''}
                </div>
            </div>
            <div class="mt-6 flex justify-end space-x-3">
                ${session.status === 'submitted' || session.status === 'pending' ? `
                <button onclick="handleSessionAction('approve', ${session.id})" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg">
                    <i class="fas fa-check mr-2"></i>Approve
                </button>
                <button onclick="handleSessionAction('reject', ${session.id})" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg">
                    <i class="fas fa-times mr-2"></i>Reject
                </button>
                <button onclick="handleSessionAction('hold', ${session.id})" class="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg">
                    <i class="fas fa-pause mr-2"></i>Hold
                </button>
                ` : ''}
                <button onclick="this.closest('.fixed').remove()" class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg">
                    Close
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

async function loadDashboardData() {
    try {
        await loadSubmissions();
        await loadChangeRequests();
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

async function loadSubmissions() {
    try {
        const response = await fetch('/manager/submissions');
        if (response.ok) {
            const data = await response.json();
            updateSubmissionsDisplay(data.submissions);
        }
    } catch (error) {
        console.error('Error loading submissions:', error);
    }
}

async function loadChangeRequests() {
    try {
        const response = await fetch('/manager/change-requests');
        if (response.ok) {
            const data = await response.json();
            updateChangeRequestsDisplay(data.change_requests);
        }
    } catch (error) {
        console.error('Error loading change requests:', error);
    }
}

function updateSubmissionsDisplay(submissions) {
    const submissionsContainer = document.getElementById('submissions-list');
    if (!submissionsContainer) return;
    
    submissionsContainer.innerHTML = submissions.map(submission => `
        <div class="bg-white rounded-lg shadow-sm p-6 transform hover:scale-[1.02] transition-transform" data-session-id="${submission.id}">
            <div class="flex justify-between items-start mb-4">
                <h3 class="text-xl font-semibold text-gray-800">${submission.title}</h3>
                <span class="px-3 py-1 rounded-full text-sm ${
                    submission.status === 'approved' ? 'bg-green-100 text-green-800' :
                    submission.status === 'submitted' ? 'bg-blue-100 text-blue-800' :
                    submission.status === 'rejected' ? 'bg-red-100 text-red-800' :
                    'bg-yellow-100 text-yellow-800'
                }">${submission.status}</span>
            </div>
            <p class="text-gray-600 mb-4">${submission.abstract.substring(0, 200)}...</p>
            <div class="flex flex-wrap gap-4 text-sm text-gray-500 mb-4">
                <span class="flex items-center">
                    <i class="fas fa-user mr-2"></i>${submission.speaker.name}
                </span>
                <span class="flex items-center">
                    <i class="fas fa-tag mr-2"></i>${submission.track}
                </span>
            </div>
            <div class="flex flex-wrap items-center justify-end space-x-3">
                ${submission.status === 'submitted' || submission.status === 'pending' ? `
                <button data-action="approve" class="text-white bg-green-500 hover:bg-green-600 px-4 py-2 rounded-lg transition-colors">
                    <i class="fas fa-check mr-2"></i>Approve
                </button>
                <button data-action="reject" class="text-white bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg transition-colors">
                    <i class="fas fa-times mr-2"></i>Reject
                </button>
                <button data-action="hold" class="text-white bg-yellow-500 hover:bg-yellow-600 px-4 py-2 rounded-lg transition-colors">
                    <i class="fas fa-pause mr-2"></i>Hold
                </button>
                ` : ''}
                <button data-action="view" class="text-gray-600 hover:text-blue-600 transition-colors">
                    <i class="fas fa-eye"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function updateChangeRequestsDisplay(changeRequests) {
    // This would update a change requests section if it exists
    console.log('Change requests:', changeRequests);
}

async function filterSubmissions() {
    const trackFilter = document.getElementById('track-filter')?.value;
    const statusFilter = document.getElementById('status-filter')?.value;
    const searchInput = document.getElementById('search-input')?.value;
    
    const filterData = {
        track: trackFilter || null,
        status: statusFilter || null,
        search: searchInput || null
    };
    
    try {
        const response = await fetch('/manager/submissions/filter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filterData)
        });
        
        if (response.ok) {
            const data = await response.json();
            updateSubmissionsDisplay(data.submissions);
        }
    } catch (error) {
        console.error('Error filtering submissions:', error);
    }
}

function initializeDragAndDrop() {
    // Initialize drag and drop for agenda builder
    const draggableSessions = document.querySelectorAll('.draggable-session');
    const timeSlots = document.querySelectorAll('.time-slot');
    
    draggableSessions.forEach(session => {
        session.draggable = true;
        session.addEventListener('dragstart', handleDragStart);
    });
    
    timeSlots.forEach(slot => {
        slot.addEventListener('dragover', handleDragOver);
        slot.addEventListener('drop', handleDrop);
    });
}

function handleDragStart(e) {
    e.dataTransfer.setData('text/plain', e.target.dataset.id);
    e.target.style.opacity = '0.5';
}

function handleDragOver(e) {
    e.preventDefault();
    e.target.style.backgroundColor = '#e5e7eb';
}

function handleDrop(e) {
    e.preventDefault();
    e.target.style.backgroundColor = '';
    
    const sessionId = e.dataTransfer.getData('text/plain');
    const timeslot = e.target.dataset.timeslot;
    
    if (sessionId && timeslot) {
        scheduleSession(sessionId, timeslot);
    }
    
    // Reset dragged element
    const draggedElement = document.querySelector(`[data-id="${sessionId}"]`);
    if (draggedElement) {
        draggedElement.style.opacity = '1';
    }
}

async function scheduleSession(sessionId, timeslot) {
    try {
        const response = await fetch('/manager/agenda/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId,
                timeslot: timeslot
            })
        });
        
        const result = await response.json();
        if (result.success) {
            showNotification('Session scheduled successfully!', 'success');
            loadAgenda();
        } else {
            showNotification(result.message || 'Failed to schedule session', 'error');
        }
    } catch (error) {
        console.error('Error scheduling session:', error);
        showNotification('An error occurred while scheduling session', 'error');
    }
}

async function loadAgenda() {
    // Load agenda data
    console.log('Loading agenda...');
}

async function loadCommunications() {
    // Load communications data
    console.log('Loading communications...');
}

async function loadSpeakers() {
    // Load speakers data
    console.log('Loading speakers...');
}

async function loadFeedback() {
    // Load feedback data
    console.log('Loading feedback...');
}

async function loadCertificates() {
    // Load certificates data
    console.log('Loading certificates...');
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

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Global functions for template use
window.handleSessionAction = handleSessionAction;
window.handleChangeRequest = handleChangeRequest;
window.showNotification = showNotification;