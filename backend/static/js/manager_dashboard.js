// Manager dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize interactive features
    initializeFilters();
    initializeSessionActions();
    initializeSpeakerManagement();
    initializeAgendaBuilder();
    handleNavigation();
});

function handleNavigation() {
    const navLinks = document.querySelectorAll('.dashboard-nav a');
    const sections = document.querySelectorAll('.dashboard-section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').slice(1);
            
            // Update active states
            navLinks.forEach(l => {
                l.classList.remove('bg-blue-50', 'text-blue-600');
                l.classList.add('hover:bg-gray-50', 'text-gray-600');
            });
            link.classList.remove('hover:bg-gray-50', 'text-gray-600');
            link.classList.add('bg-blue-50', 'text-blue-600');
            
            // Show/hide sections with animation
            sections.forEach(section => {
                if(section.id === targetId) {
                    section.classList.remove('hidden');
                    section.classList.add('animate-fade-in');
                } else {
                    section.classList.add('hidden');
                    section.classList.remove('animate-fade-in');
                }
            });
        });
    });
}

function initializeFilters() {
    const filterInputs = document.querySelectorAll('.filter-input');
    let debounceTimer;

    filterInputs.forEach(input => {
        input.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => applyFilters(), 300);
        });
    });
}

async function applyFilters() {
    const filters = {
        track: document.getElementById('track-filter').value,
        status: document.getElementById('status-filter').value,
        search: document.getElementById('search-input').value
    };

    try {
        const response = await fetch('/manager/submissions/filter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filters)
        });

        if (!response.ok) throw new Error('Filter request failed');

        const data = await response.json();
        updateSubmissionsList(data.submissions);
    } catch (error) {
        console.error('Error applying filters:', error);
        showNotification('Error filtering submissions', 'error');
    }
}

function updateSubmissionsList(submissions) {
    const container = document.getElementById('submissions-list');
    container.innerHTML = '';

    submissions.forEach(submission => {
        const card = createSubmissionCard(submission);
        container.appendChild(card);
    });
}

function createSubmissionCard(submission) {
    const cardDiv = document.createElement('div');
    cardDiv.className = 'bg-white rounded-lg shadow-sm p-6 mb-4 transform hover:scale-[1.02] transition-transform';
    cardDiv.innerHTML = `
        <div class="flex justify-between items-start mb-4">
            <h3 class="text-xl font-semibold text-gray-800">${submission.title}</h3>
            <span class="px-3 py-1 rounded-full text-sm 
                ${getStatusClass(submission.status)}">
                ${submission.status.charAt(0).toUpperCase() + submission.status.slice(1)}
            </span>
        </div>
        <p class="text-gray-600 mb-4">${submission.abstract.slice(0, 200)}...</p>
        <div class="flex flex-wrap gap-4 text-sm text-gray-500 mb-4">
            <span class="flex items-center">
                <i class="fas fa-user mr-2"></i>${submission.speaker.name}
            </span>
            <span class="flex items-center">
                <i class="fas fa-tag mr-2"></i>${submission.track}
            </span>
        </div>
        <div class="flex items-center justify-end space-x-3">
            ${getActionButtons(submission)}
        </div>
    `;

    // Add event listeners for action buttons
    const buttons = cardDiv.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', () => handleSubmissionAction(submission.id, button.dataset.action));
    });

    return cardDiv;
}

function getStatusClass(status) {
    const classes = {
        approved: 'bg-green-100 text-green-800',
        rejected: 'bg-red-100 text-red-800',
        pending: 'bg-yellow-100 text-yellow-800',
        submitted: 'bg-blue-100 text-blue-800'
    };
    return classes[status] || classes.submitted;
}

function getActionButtons(submission) {
    if (submission.status === 'submitted' || submission.status === 'pending') {
        return `
            <button data-action="approve" class="text-white bg-green-500 hover:bg-green-600 px-4 py-2 rounded-lg transition-colors">
                <i class="fas fa-check mr-2"></i>Approve
            </button>
            <button data-action="reject" class="text-white bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg transition-colors">
                <i class="fas fa-times mr-2"></i>Reject
            </button>
            <button data-action="hold" class="text-white bg-yellow-500 hover:bg-yellow-600 px-4 py-2 rounded-lg transition-colors">
                <i class="fas fa-pause mr-2"></i>Hold
            </button>
        `;
    }
    return `
        <button data-action="view" class="text-gray-600 hover:text-blue-600 transition-colors">
            <i class="fas fa-eye"></i>
        </button>
    `;
}

async function handleSubmissionAction(submissionId, action) {
    try {
        const response = await fetch(`/manager/submissions/${submissionId}/${action}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) throw new Error('Action request failed');

        const data = await response.json();
        if (data.success) {
            showNotification(`Session ${action}ed successfully`, 'success');
            applyFilters(); // Refresh the list
        }
    } catch (error) {
        console.error('Error handling submission action:', error);
        showNotification('Error processing action', 'error');
    }
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg ${
        type === 'success' ? 'bg-green-500' : 'bg-red-500'
    } text-white animate-fade-in`;
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function initializeSpeakerManagement() {
    const speakerSearch = document.getElementById('speaker-search');
    if (speakerSearch) {
        speakerSearch.addEventListener('input', debounce(searchSpeakers, 300));
    }
}

function initializeAgendaBuilder() {
    // Initialize drag and drop functionality
    const draggables = document.querySelectorAll('.draggable-session');
    const dropZones = document.querySelectorAll('.time-slot');

    draggables.forEach(draggable => {
        draggable.addEventListener('dragstart', handleDragStart);
        draggable.addEventListener('dragend', handleDragEnd);
    });

    dropZones.forEach(zone => {
        zone.addEventListener('dragover', handleDragOver);
        zone.addEventListener('drop', handleDrop);
    });
}

function handleDragStart(e) {
    e.target.classList.add('opacity-50');
    e.dataTransfer.setData('text/plain', e.target.id);
}

function handleDragEnd(e) {
    e.target.classList.remove('opacity-50');
}

function handleDragOver(e) {
    e.preventDefault();
    e.target.classList.add('bg-blue-50');
}

function handleDrop(e) {
    e.preventDefault();
    const sessionId = e.dataTransfer.getData('text/plain');
    const timeSlot = e.target.dataset.timeslot;
    updateSessionTimeslot(sessionId, timeSlot);
}

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

async function searchSpeakers(query) {
    // Implement speaker search functionality
}

async function updateSessionTimeslot(sessionId, timeslot) {
    // Implement timeslot update functionality
}