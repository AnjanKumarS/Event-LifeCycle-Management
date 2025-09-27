// Speaker dashboard specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    handleNavigation();
    initializeNewSession();
    initializeSessionActions();
    initializeDocumentUpload();
    initializeAnimations();
    initializeScrollAnimations();
    
    // Add classes for animations
    document.querySelectorAll('.bg-gradient-to-r').forEach(card => {
        card.classList.add('stat-card');
    });

    document.querySelectorAll('.session-actions button').forEach(button => {
        button.classList.add('button-effect');
    });

    // Initial animations
    animateOnLoad();
});

function handleNavigation() {
    const navLinks = document.querySelectorAll('.dashboard-nav a');
    const sections = document.querySelectorAll('.dashboard-section');
    let currentSection = null;
    
    navLinks.forEach(link => {
        link.addEventListener('click', async (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').slice(1);
            const targetSection = document.getElementById(targetId);
            
            if (currentSection === targetSection) return;

            // Update active states with animation
            navLinks.forEach(l => {
                l.style.transition = 'all 0.3s ease';
                l.classList.remove('bg-blue-50', 'text-blue-600');
                l.classList.add('hover:bg-gray-50', 'text-gray-600');
            });
            
            // Animate the active link
            link.classList.remove('hover:bg-gray-50', 'text-gray-600');
            link.classList.add('bg-blue-50', 'text-blue-600');
            
            // Fade out current section
            if (currentSection) {
                currentSection.style.opacity = '0';
                currentSection.style.transform = 'translateY(10px)';
                await new Promise(resolve => setTimeout(resolve, 300));
                currentSection.classList.add('hidden');
            }
            
            // Show and fade in new section
            if (targetSection) {
                sections.forEach(s => {
                    if (s !== targetSection) {
                        s.classList.add('hidden');
                    }
                });
                
                targetSection.classList.remove('hidden');
                targetSection.style.opacity = '0';
                targetSection.style.transform = 'translateY(10px)';
                
                // Initialize any loading states in the new section
                targetSection.querySelectorAll('[data-loading]').forEach(element => {
                    element.classList.add('loading');
                });
                
                // Trigger reflow
                targetSection.offsetHeight;
                
                targetSection.style.transition = 'all 0.5s ease';
                targetSection.style.opacity = '1';
                targetSection.style.transform = 'translateY(0)';
                
                // Animate child elements
                const children = targetSection.children;
                for (let i = 0; i < children.length; i++) {
                    const child = children[i];
                    child.style.opacity = '0';
                    child.style.transform = 'translateY(20px)';
                    
                    setTimeout(() => {
                        child.style.transition = 'all 0.5s ease';
                        child.style.opacity = '1';
                        child.style.transform = 'translateY(0)';
                    }, i * 100);
                }
                
                // Remove loading states after animation
                setTimeout(() => {
                    targetSection.querySelectorAll('[data-loading]').forEach(element => {
                        element.classList.remove('loading');
                    });
                }, 1000);
                
                currentSection = targetSection;
                
                // Update URL hash without scrolling
                history.pushState(null, null, `#${targetId}`);
                
                // Initialize any charts or other interactive elements
                initializeSectionContent(targetSection);
            }
        });
    });
}

function initializeNewSession() {
    const modal = document.getElementById('new-session-modal');
    const newSessionBtn = document.getElementById('new-session-btn');
    const sessionForm = document.getElementById('new-session-form');

    newSessionBtn.addEventListener('click', () => {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    });

    window.closeModal = function() {
        modal.classList.remove('flex');
        modal.classList.add('hidden');
    };

    sessionForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());
        
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
                location.reload();
            } else {
                showNotification(result.message || 'Error submitting session', 'error');
            }
        } catch (error) {
            showNotification('Error submitting session', 'error');
        }
    });
}

function initializeSessionActions() {
    const actionButtons = document.querySelectorAll('.session-actions button');
    actionButtons.forEach(button => {
        button.addEventListener('click', handleSessionAction);
    });
}

async function handleSessionAction(e) {
    const action = e.target.closest('button').querySelector('i').className;
    const sessionCard = e.target.closest('.bg-white');
    const sessionId = sessionCard.dataset.id;

    if (action.includes('edit')) {
        // Show edit modal
        showEditSessionModal(sessionId);
    } else if (action.includes('eye')) {
        // Show session details
        showSessionDetails(sessionId);
    } else if (action.includes('upload')) {
        // Show document upload modal
        showDocumentUploadModal(sessionId);
    }
}

function showEditSessionModal(sessionId) {
    // Implementation for edit modal
}

async function showSessionDetails(sessionId) {
    try {
        const response = await fetch(`/speaker/sessions/${sessionId}/details`);
        const data = await response.json();
        
        if (data.success) {
            // Create and show modal with session details
            showDetailsModal(data.session);
        } else {
            showNotification('Error fetching session details', 'error');
        }
    } catch (error) {
        showNotification('Error fetching session details', 'error');
    }
}

function showDetailsModal(session) {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center';
    modal.innerHTML = `
        <div class="bg-white rounded-lg w-full max-w-2xl p-6">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-2xl font-bold text-gray-800">${session.title}</h3>
                <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-gray-600">
                    <i class="fas fa-times text-xl"></i>
                </button>
            </div>
            <div class="space-y-4">
                <div>
                    <h4 class="font-semibold text-gray-700">Abstract</h4>
                    <p class="text-gray-600">${session.abstract}</p>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <h4 class="font-semibold text-gray-700">Track</h4>
                        <p class="text-gray-600">${session.track}</p>
                    </div>
                    <div>
                        <h4 class="font-semibold text-gray-700">Category</h4>
                        <p class="text-gray-600">${session.category}</p>
                    </div>
                </div>
                <div>
                    <h4 class="font-semibold text-gray-700">Status</h4>
                    <span class="px-3 py-1 rounded-full text-sm inline-block mt-1
                        ${getStatusClass(session.status)}">
                        ${session.status.charAt(0).toUpperCase() + session.status.slice(1)}
                    </span>
                </div>
                ${session.timeslot ? `
                <div>
                    <h4 class="font-semibold text-gray-700">Time Slot</h4>
                    <p class="text-gray-600">${session.timeslot}</p>
                </div>
                ` : ''}
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

function initializeDocumentUpload() {
    const uploadButtons = document.querySelectorAll('button[data-upload]');
    uploadButtons.forEach(button => {
        // Create a container for the progress bar
        const progressContainer = document.createElement('div');
        progressContainer.className = 'progress-bar hidden mt-2';
        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar-fill';
        progressContainer.appendChild(progressBar);
        button.parentNode.insertBefore(progressContainer, button.nextSibling);

        button.addEventListener('click', () => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = button.dataset.accept || '*/*';
            input.click();

            input.addEventListener('change', async () => {
                const file = input.files[0];
                if (file) {
                    const formData = new FormData();
                    formData.append('file', file);
                    formData.append('sessionId', button.dataset.sessionId);
                    formData.append('type', button.dataset.upload);

                    // Show loading state
                    button.disabled = true;
                    const originalText = button.innerHTML;
                    button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Uploading...';
                    progressContainer.classList.remove('hidden');
                    
                    // Initialize progress animation
                    let progress = 0;
                    const progressInterval = setInterval(() => {
                        if (progress < 90) {
                            progress += 5;
                            animateProgressBar(progressContainer, progress);
                        }
                    }, 200);

                    try {
                        const response = await fetch('/speaker/documents/upload', {
                            method: 'POST',
                            body: formData
                        });
                        const result = await response.json();
                        
                        // Complete progress animation
                        clearInterval(progressInterval);
                        animateProgressBar(progressContainer, 100);
                        
                        if (result.success) {
                            // Show success animation
                            button.innerHTML = '<i class="fas fa-check mr-2"></i>Success!';
                            button.classList.add('bg-green-500');
                            
                            // Update UI with new document
                            const documentElement = createDocumentElement(result.document);
                            documentElement.style.opacity = '0';
                            documentElement.style.transform = 'translateY(20px)';
                            
                            const container = document.querySelector(`#documents-${result.document.sessionId}`);
                            if (container) {
                                container.appendChild(documentElement);
                                // Trigger animation
                                setTimeout(() => {
                                    documentElement.style.transition = 'all 0.5s ease';
                                    documentElement.style.opacity = '1';
                                    documentElement.style.transform = 'translateY(0)';
                                }, 100);
                            }

                            showNotification('File uploaded successfully!', 'success');
                        } else {
                            throw new Error(result.message || 'Upload failed');
                        }
                    } catch (error) {
                        button.classList.add('bg-red-500');
                        button.innerHTML = '<i class="fas fa-exclamation-circle mr-2"></i>Error';
                        showNotification(error.message || 'Error uploading file', 'error');
                    } finally {
                        // Reset button state after delay
                        setTimeout(() => {
                            button.disabled = false;
                            button.innerHTML = originalText;
                            button.classList.remove('bg-green-500', 'bg-red-500');
                            progressContainer.classList.add('hidden');
                            progressBar.style.width = '0%';
                        }, 2000);
                    }
                }
            });
        });
    });
}

function createDocumentElement(document) {
    const element = document.createElement('div');
    element.className = 'flex items-center justify-between bg-white p-4 rounded-lg hover-card mb-4';
    element.innerHTML = `
        <div class="flex items-center space-x-3">
            <i class="fas fa-${getFileIcon(document.filename)} text-blue-500 text-xl"></i>
            <div>
                <p class="font-medium text-gray-800">${document.filename}</p>
                <p class="text-sm text-gray-500">Uploaded ${new Date(document.uploadedAt).toLocaleDateString()}</p>
            </div>
        </div>
        <div class="flex space-x-2">
            <button class="button-effect text-blue-600 hover:text-blue-800" onclick="downloadDocument('${document.id}')">
                <i class="fas fa-download"></i>
            </button>
            <button class="button-effect text-red-600 hover:text-red-800" onclick="deleteDocument('${document.id}')">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;
    return element;
}

function getFileIcon(filename) {
    const extension = filename.split('.').pop().toLowerCase();
    const icons = {
        pdf: 'file-pdf',
        doc: 'file-word',
        docx: 'file-word',
        xls: 'file-excel',
        xlsx: 'file-excel',
        ppt: 'file-powerpoint',
        pptx: 'file-powerpoint',
        jpg: 'file-image',
        jpeg: 'file-image',
        png: 'file-image',
        gif: 'file-image',
        zip: 'file-archive',
        rar: 'file-archive'
    };
    return icons[extension] || 'file';
}

function updateDocumentList(document) {
    const documentsList = document.querySelector(`#documents-${document.sessionId}`);
    if (documentsList) {
        const item = document.createElement('div');
        item.className = 'flex items-center justify-between bg-white p-4 rounded-lg';
        item.innerHTML = `
            <div class="flex items-center space-x-3">
                <i class="fas fa-file text-blue-500 text-xl"></i>
                <div>
                    <p class="font-medium text-gray-800">${document.filename}</p>
                    <p class="text-sm text-gray-500">Uploaded ${new Date(document.uploadedAt).toLocaleDateString()}</p>
                </div>
            </div>
            <div class="flex space-x-2">
                <a href="${document.url}" class="text-blue-600 hover:text-blue-800" download>
                    <i class="fas fa-download"></i>
                </a>
                <button class="text-red-600 hover:text-red-800" onclick="deleteDocument('${document.id}')">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        documentsList.appendChild(item);
    }
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

function initializeAnimations() {
    // Add hover animations to buttons
    document.querySelectorAll('button').forEach(button => {
        if (!button.classList.contains('button-effect')) {
            button.classList.add('button-effect');
        }
    });

    // Add hover animations to cards
    document.querySelectorAll('.bg-white').forEach(card => {
        if (!card.classList.contains('hover-card')) {
            card.classList.add('hover-card');
        }
    });

    // Initialize loading states
    document.querySelectorAll('[data-loading]').forEach(element => {
        element.addEventListener('click', () => {
            element.classList.add('loading');
            setTimeout(() => {
                element.classList.remove('loading');
            }, 2000);
        });
    });
}

function initializeScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });

    document.querySelectorAll('.section-transition').forEach(section => {
        observer.observe(section);
    });
}

function animateOnLoad() {
    // Animate stat cards
    document.querySelectorAll('.stat-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 150);
    });

    // Animate sessions
    document.querySelectorAll('.session-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 500 + index * 100); // Start after stat cards
    });

    // Animate navigation items
    document.querySelectorAll('nav a').forEach((link, index) => {
        link.style.opacity = '0';
        link.style.transform = 'translateX(-20px)';
        setTimeout(() => {
            link.style.opacity = '1';
            link.style.transform = 'translateX(0)';
        }, 200 + index * 100);
    });
}

function showLoadingState(element) {
    element.classList.add('loading');
    const originalContent = element.innerHTML;
    element.innerHTML = '<div class="spinner"></div>';
    return () => {
        element.classList.remove('loading');
        element.innerHTML = originalContent;
    };
}

function animateProgressBar(progressBar, targetPercentage) {
    const fill = progressBar.querySelector('.progress-bar-fill');
    let currentWidth = 0;
    const step = targetPercentage / 100;
    
    const animate = () => {
        if (currentWidth < targetPercentage) {
            currentWidth += step;
            fill.style.width = `${currentWidth}%`;
            requestAnimationFrame(animate);
        }
    };
    
    requestAnimationFrame(animate);
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg ${
        type === 'success' ? 'bg-green-500' : 'bg-red-500'
    } text-white slide-in`;
    
    const icon = document.createElement('i');
    icon.className = `fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} mr-2`;
    notification.appendChild(icon);
    
    const text = document.createElement('span');
    text.textContent = message;
    notification.appendChild(text);
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

function initializeSectionContent(section) {
    // Initialize charts if present
    const chartContainers = section.querySelectorAll('[data-chart]');
    chartContainers.forEach(container => {
        const chartType = container.dataset.chart;
        const chartData = JSON.parse(container.dataset.chartData || '{}');
        initializeChart(container, chartType, chartData);
    });

    // Initialize any dropzones
    const dropzones = section.querySelectorAll('.dropzone');
    dropzones.forEach(dropzone => {
        initializeDropzone(dropzone);
    });

    // Initialize tooltips
    const tooltips = section.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', (e) => {
            const tooltip = document.createElement('div');
            tooltip.className = 'absolute bg-gray-800 text-white px-2 py-1 rounded text-sm z-50 transform -translate-y-full -translate-x-1/2 left-1/2 top-0';
            tooltip.textContent = element.dataset.tooltip;
            tooltip.style.pointerEvents = 'none';
            element.style.position = 'relative';
            element.appendChild(tooltip);
        });

        element.addEventListener('mouseleave', () => {
            const tooltip = element.querySelector('.bg-gray-800');
            if (tooltip) tooltip.remove();
        });
    });

    // Initialize sorting and filtering
    const sortButtons = section.querySelectorAll('[data-sort]');
    sortButtons.forEach(button => {
        button.addEventListener('click', () => {
            const target = button.dataset.sort;
            const direction = button.dataset.direction === 'asc' ? 'desc' : 'asc';
            button.dataset.direction = direction;
            
            // Update sort icon
            const icon = button.querySelector('i');
            icon.className = `fas fa-sort-${direction === 'asc' ? 'up' : 'down'} ml-1`;
            
            // Perform sorting with animation
            const container = document.querySelector(`[data-sort-container="${target}"]`);
            if (container) {
                const items = Array.from(container.children);
                items.sort((a, b) => {
                    const valueA = a.dataset[target];
                    const valueB = b.dataset[target];
                    return direction === 'asc' ? 
                        valueA.localeCompare(valueB) : 
                        valueB.localeCompare(valueA);
                });

                // Animate reordering
                items.forEach((item, index) => {
                    item.style.transition = 'transform 0.3s ease';
                    item.style.transform = 'translateY(20px)';
                    item.style.opacity = '0';
                    
                    setTimeout(() => {
                        container.appendChild(item);
                        requestAnimationFrame(() => {
                            item.style.transform = 'translateY(0)';
                            item.style.opacity = '1';
                        });
                    }, index * 50);
                });
            }
        });
    });

    // Initialize search functionality
    const searchInputs = section.querySelectorAll('[data-search]');
    searchInputs.forEach(input => {
        input.addEventListener('input', debounce((e) => {
            const searchTerm = e.target.value.toLowerCase();
            const target = input.dataset.search;
            const container = document.querySelector(`[data-search-container="${target}"]`);
            
            if (container) {
                const items = container.children;
                Array.from(items).forEach(item => {
                    const text = item.textContent.toLowerCase();
                    const match = text.includes(searchTerm);
                    
                    item.style.transition = 'all 0.3s ease';
                    if (match) {
                        item.style.display = '';
                        item.style.opacity = '1';
                        item.style.transform = 'translateY(0)';
                    } else {
                        item.style.opacity = '0';
                        item.style.transform = 'translateY(20px)';
                        setTimeout(() => {
                            item.style.display = 'none';
                        }, 300);
                    }
                });
            }
        }, 300));
    });
}

function initializeDropzone(dropzone) {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => {
            dropzone.classList.add('border-blue-500');
            dropzone.classList.add('bg-blue-50');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => {
            dropzone.classList.remove('border-blue-500');
            dropzone.classList.remove('bg-blue-50');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        const input = dropzone.querySelector('input[type="file"]');
        
        if (input && files.length > 0) {
            input.files = files;
            input.dispatchEvent(new Event('change'));
        }
    });
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

async function deleteDocument(documentId) {
    if (!confirm('Are you sure you want to delete this document?')) return;

    try {
        const response = await fetch(`/speaker/documents/${documentId}`, {
            method: 'DELETE'
        });
        const result = await response.json();
        
        if (result.success) {
            showNotification('Document deleted successfully!', 'success');
            // Remove the document from the UI
            document.querySelector(`[data-document-id="${documentId}"]`).remove();
        } else {
            showNotification(result.message || 'Error deleting document', 'error');
        }
    } catch (error) {
        showNotification('Error deleting document', 'error');
    }
}