/**
 * Multimodal AI Assistant - Main Application Script
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendMessageBtn = document.getElementById('send-message');
    const clearChatBtn = document.getElementById('clear-chat');
    const menuItems = document.querySelectorAll('.menu-item');
    const viewContainers = document.querySelectorAll('.view-container');
    const themeSelector = document.getElementById('theme-selector');
    const animationLevel = document.getElementById('animation-level');
    const uploadArea = document.getElementById('upload-area');
    const imageUpload = document.getElementById('image-upload');
    const imagePreviewContainer = document.getElementById('image-preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeImageBtn = document.getElementById('remove-image');
    const imagePrompt = document.getElementById('image-prompt');
    const analyzeImageBtn = document.getElementById('analyze-image');
    const analysisResults = document.getElementById('analysis-results');
    const resultContent = document.getElementById('result-content');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    // State
    let sessionId = generateSessionId();
    let selectedFile = null;
    let animationEnabled = true;
    
    // Initialize
    initializeApp();
    
    /**
     * Initialize the application
     */
    function initializeApp() {
        // Set up event listeners
        setupEventListeners();
        
        // Auto-resize textarea
        setupTextareaAutoResize();
        
        // Check animation preference
        checkAnimationPreference();
        
        // Add animation classes to initial elements if enabled
        if (animationEnabled) {
            document.querySelectorAll('.message').forEach(msg => {
                msg.classList.add('fade-in');
            });
        }
    }
    
    /**
     * Set up event listeners
     */
    function setupEventListeners() {
        // Send message on button click
        sendMessageBtn.addEventListener('click', handleSendMessage);
        
        // Send message on Enter key (but allow Shift+Enter for new line)
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
            }
        });
        
        // Clear chat
        clearChatBtn.addEventListener('click', () => {
            // Remove all messages except the first one (welcome message)
            const messages = chatMessages.querySelectorAll('.message');
            for (let i = 1; i < messages.length; i++) {
                messages[i].remove();
            }
            
            // Generate new session ID
            sessionId = generateSessionId();
        });
        
        // Menu navigation
        menuItems.forEach(item => {
            item.addEventListener('click', () => {
                const view = item.getAttribute('data-view');
                
                // Update active menu item
                menuItems.forEach(menuItem => menuItem.classList.remove('active'));
                item.classList.add('active');
                
                // Show corresponding view
                viewContainers.forEach(container => {
                    container.classList.remove('active');
                    if (container.id === `${view}-view`) {
                        container.classList.add('active');
                    }
                });
            });
        });
        
        // Theme selector
        themeSelector.addEventListener('change', () => {
            document.body.className = `theme-${themeSelector.value}`;
            localStorage.setItem('theme', themeSelector.value);
        });
        
        // Animation level
        animationLevel.addEventListener('change', () => {
            animationEnabled = animationLevel.value !== 'none';
            localStorage.setItem('animationLevel', animationLevel.value);
        });
        
        // Image upload via click
        uploadArea.addEventListener('click', () => {
            imageUpload.click();
        });
        
        // Image upload via drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            if (e.dataTransfer.files.length) {
                handleImageUpload(e.dataTransfer.files[0]);
            }
        });
        
        // Image upload via file input
        imageUpload.addEventListener('change', (e) => {
            if (e.target.files.length) {
                handleImageUpload(e.target.files[0]);
            }
        });
        
        // Remove image
        removeImageBtn.addEventListener('click', () => {
            selectedFile = null;
            imagePreviewContainer.style.display = 'none';
            uploadArea.style.display = 'block';
            analyzeImageBtn.disabled = true;
        });
        
        // Analyze image
        analyzeImageBtn.addEventListener('click', handleImageAnalysis);
    }
    
    /**
     * Set up textarea auto-resize
     */
    function setupTextareaAutoResize() {
        const textareas = [chatInput, imagePrompt];
        
        textareas.forEach(textarea => {
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
            });
        });
    }
    
    /**
     * Check animation preference from localStorage
     */
    function checkAnimationPreference() {
        // Check theme preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            themeSelector.value = savedTheme;
            document.body.className = `theme-${savedTheme}`;
        }
        
        // Check animation preference
        const savedAnimationLevel = localStorage.getItem('animationLevel');
        if (savedAnimationLevel) {
            animationLevel.value = savedAnimationLevel;
            animationEnabled = savedAnimationLevel !== 'none';
        }
    }
    
    /**
     * Handle sending a message
     */
    async function handleSendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage('user', message);
        
        // Clear input
        chatInput.value = '';
        chatInput.style.height = 'auto';
        
        // Show loading indicator
        showLoading();
        
        try {
            // Send message to API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message,
                    session_id: sessionId
                })
            });
            
            const data = await response.json();
            
            // Update session ID if provided
            if (data.session_id) {
                sessionId = data.session_id;
            }
            
            // Add assistant response to chat
            addMessage('assistant', data.reply);
        } catch (error) {
            console.error('Error sending message:', error);
            addMessage('assistant', 'Sorry, I encountered an error while processing your message. Please try again.');
        } finally {
            // Hide loading indicator
            hideLoading();
        }
    }
    
    /**
     * Handle image upload
     * @param {File} file - The uploaded image file
     */
    function handleImageUpload(file) {
        // Check if file is an image
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file.');
            return;
        }
        
        // Store the file
        selectedFile = file;
        
        // Display image preview
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreviewContainer.style.display = 'block';
            uploadArea.style.display = 'none';
            analyzeImageBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }
    
    /**
     * Handle image analysis
     */
    async function handleImageAnalysis() {
        if (!selectedFile) return;
        
        // Show loading indicator
        showLoading();
        
        // Get prompt if provided
        const prompt = imagePrompt.value.trim() || 'Please describe this image in detail.';
        
        // Create form data
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('prompt', prompt);
        formData.append('session_id', sessionId);
        
        try {
            // Send image to API
            const response = await fetch('/api/image-analysis', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            // Update session ID if provided
            if (data.session_id) {
                sessionId = data.session_id;
            }
            
            // Display analysis results
            resultContent.textContent = data.analysis;
            analysisResults.style.display = 'block';
            
            // Scroll to results
            analysisResults.scrollIntoView({ behavior: 'smooth' });
        } catch (error) {
            console.error('Error analyzing image:', error);
            resultContent.textContent = 'Sorry, I encountered an error while analyzing the image. Please try again.';
            analysisResults.style.display = 'block';
        } finally {
            // Hide loading indicator
            hideLoading();
        }
    }
    
    /**
     * Add a message to the chat
     * @param {string} role - The role of the message sender ('user' or 'assistant')
     * @param {string} content - The message content
     */
    function addMessage(role, content) {
        // Create message elements
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;
        if (animationEnabled) {
            messageDiv.classList.add('slide-in');
        }
        
        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        
        const avatarImg = document.createElement('img');
        avatarImg.src = role === 'user' 
            ? '/static/images/user-avatar.png' 
            : '/static/images/avatar.png';
        avatarImg.alt = role === 'user' ? 'User' : 'Assistant';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        
        // Split content by paragraphs and create paragraph elements
        const paragraphs = content.split('\n').filter(p => p.trim());
        paragraphs.forEach(paragraph => {
            const p = document.createElement('p');
            p.textContent = paragraph;
            textDiv.appendChild(p);
        });
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = getCurrentTime();
        
        // Assemble message
        avatarDiv.appendChild(avatarImg);
        contentDiv.appendChild(textDiv);
        contentDiv.appendChild(timeDiv);
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
        
        // Add to chat
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    /**
     * Show loading overlay
     */
    function showLoading() {
        loadingOverlay.style.display = 'flex';
    }
    
    /**
     * Hide loading overlay
     */
    function hideLoading() {
        loadingOverlay.style.display = 'none';
    }
    
    /**
     * Get current time in HH:MM format
     * @returns {string} Current time
     */
    function getCurrentTime() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }
    
    /**
     * Generate a random session ID
     * @returns {string} Random session ID
     */
    function generateSessionId() {
        return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    }
});