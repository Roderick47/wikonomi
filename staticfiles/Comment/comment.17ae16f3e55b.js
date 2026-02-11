// Comment System JavaScript

// Update the comment count badge
function updateCommentCount() {
    const badge = document.getElementById('comment-count');
    if (badge) {
        let currentCount = parseInt(badge.innerText) || 0;
        badge.innerText = currentCount + 1;
    }
}

// Scroll to the newly added comment
function scrollToNewComment() {
    const container = document.getElementById('comments-container');
    if (container && container.firstElementChild) {
        container.firstElementChild.scrollIntoView({ behavior: 'smooth', block: 'center' });
        // Highlight effect
        container.firstElementChild.style.transition = 'background-color 2s ease-out';
        container.firstElementChild.style.backgroundColor = '#fff3cd'; // Bootstrap warning color (light yellow)
        setTimeout(() => {
            container.firstElementChild.style.backgroundColor = '';
        }, 2000);
    }
}

// Remove empty state message if it exists
function removeEmptyState() {
    // Look for the empty state inside the comments container
    const emptyState = document.querySelector('#comments-container .empty-state');
    if (emptyState) {
        emptyState.remove();
    }
    // Also check if there's a load-more container interacting with it? 
    // Usually the empty state is the only child if no comments.
}

// Function to handle successful comment submission
function handleCommentSuccess(evt) {
    if (evt.detail && evt.detail.successful) {
        const form = evt.target;
        if (form) {
            form.reset();
        }
        removeEmptyState();
        updateCommentCount();
        scrollToNewComment();
    }
}

// Expose functions globally if needed for inline event handlers, 
// though event delegation is cleaner. 
// For now, we will use these helper functions in hx-on attributes.
window.handleCommentSuccess = handleCommentSuccess;

// Show the reply form for a specific comment
function showReplyForm(commentId) {
    const formContainer = document.getElementById(`reply-form-${commentId}`);
    if (formContainer) {
        // Close other open reply forms if you want single-threaded focus, 
        // but for now let's just toggle this one.
        if (formContainer.style.display === 'none') {
            formContainer.style.display = 'block';
            const textarea = formContainer.querySelector('textarea');
            if (textarea) textarea.focus();
        } else {
            formContainer.style.display = 'none';
        }
    }
}

// Hide the reply form after submission
function hideReplyForm(commentId) {
    const formContainer = document.getElementById(`reply-form-${commentId}`);
    if (formContainer) {
        formContainer.style.display = 'none';
    }
}

// Toggle replies visibility with Lazy Loading
function toggleReplies(commentId) {
    console.log("toggleReplies called for:", commentId);
    const container = document.getElementById(`replies-${commentId}`);
    const icon = document.getElementById(`toggle-icon-${commentId}`);

    if (!container) {
        console.error("Replies container not found for:", commentId);
        return;
    }

    const isExpanded = container.classList.contains('expanded');
    const isLoaded = container.dataset.loaded === 'true';
    console.log("State:", { isExpanded, isLoaded });

    // If expanding and not loaded, fetch replies
    if (!isExpanded && !isLoaded) {
        console.log("Fetching replies via HTMX...");
        // Show loading indicator
        if (icon) {
            icon.className = 'fas fa-spinner fa-spin'; // Replace icon with spinner
        }

        // Use URL from data attribute
        const url = container.dataset.repliesUrl;
        if (!url) {
            console.error("Replies URL not found in data-replies-url attribute");
            // Fallback just in case, or show error
            // icon restoration
            if (icon) icon.className = 'fas fa-chevron-down';
            return;
        }
        console.log("Request URL:", url);

        htmx.ajax('GET', url, {
            target: `#replies-${commentId}`,
            swap: 'innerHTML'
        }).then(() => {
            console.log("HTMX request successful");
            container.dataset.loaded = 'true';
            // Once loaded, expand
            container.classList.add('expanded');
            if (icon) {
                icon.className = 'fas fa-chevron-up'; // Restore expanded icon
            }
        }).catch((err) => {
            console.error("Failed to load replies", err);
            // Restore icon on error?
            if (icon) {
                icon.className = 'fas fa-chevron-down';
            }
        });
    } else {
        console.log("Toggling visibility directly.");
        // Just toggle
        container.classList.toggle('expanded');
        if (icon) {
            if (container.classList.contains('expanded')) {
                icon.className = 'fas fa-chevron-up';
            } else {
                icon.className = 'fas fa-chevron-down';
            }
        }
    }
}

// Force show replies container (for when a new reply is added)
function showRepliesContainer(commentId) {
    const container = document.getElementById(`replies-${commentId}`);
    if (container) {
        // Mark as loaded since we just added content via the reply form
        if (container.dataset.loaded !== 'true') {
            container.dataset.loaded = 'true';
        }

        if (!container.classList.contains('expanded')) {
            container.classList.add('expanded');
            const icon = document.getElementById(`toggle-icon-${commentId}`);
            if (icon) {
                icon.className = 'fas fa-chevron-up';
            }
        }
    }
}

// Scroll to the newly added reply
function scrollToNewReply(form) {
    // The target is the replies container (hx-target)
    // Since we appended, the last child of the target should be the new reply
    // But 'form' here is the form element. We can get the target ID from the form's hx-target attribute 
    // or infer it if we know the comment ID.
    // However, HTMX 'this' in hx-on is the element itself.

    // Actually, in comment_item.html: hx-target="#replies-{{ comment.id }}"
    // The new content is appended.

    // Let's find the container relative to the form or by ID if possible.
    // The form is usually sibling or close to the replies container.
    // Easier: we know the structure.

    // We can just look for the last inserted element in the target container.
    const targetId = form.getAttribute('hx-target');
    if (targetId) {
        const container = document.querySelector(targetId);
        if (container && container.lastElementChild) {
            container.lastElementChild.scrollIntoView({ behavior: 'smooth', block: 'center' });
            // Highlight
            container.lastElementChild.style.transition = 'background-color 2s ease-out';
            container.lastElementChild.style.backgroundColor = '#fff3cd';
            setTimeout(() => {
                container.lastElementChild.style.backgroundColor = '';
            }, 2000);
        }
    }
}

// Update reply count text immediately
function updateReplyCount(commentId) {
    const countSpan = document.getElementById(`reply-count-text-${commentId}`);

    if (countSpan) {
        // Parse current count efficiently
        const text = countSpan.innerText;
        // Match number at start of string
        const match = text.match(/^\d+/);
        let count = match ? parseInt(match[0]) : 0;

        count++;

        // Simple pluralization logic matching Django's standard behavior or just "Replies"
        // The server returns "1 reply" or "X replies" usually.
        const newText = count === 1 ? '1 reply' : `${count} replies`;
        countSpan.innerText = newText;
    } else {
        // Going from 0 to 1 reply
        // We need to inject the span and toggle button if they don't exist
        const actionsContainer = document.getElementById(`reply-actions-${commentId}`);
        if (actionsContainer) {
            // Create the count span
            const newSpan = document.createElement('span');
            newSpan.className = 'text-muted small';
            newSpan.id = `reply-count-text-${commentId}`;
            newSpan.innerText = '1 reply';

            // Create the toggle button
            const newBtn = document.createElement('button');
            newBtn.className = 'toggle-replies-btn';
            newBtn.title = 'Toggle replies';
            newBtn.onclick = function () { toggleReplies(commentId); };

            const newIcon = document.createElement('i');
            newIcon.className = 'fas fa-chevron-up'; // Expanded by default since we just added one and showRepliesContainer is called
            newIcon.id = `toggle-icon-${commentId}`;

            newBtn.appendChild(newIcon);

            actionsContainer.appendChild(newSpan);
            actionsContainer.appendChild(newBtn);
        }
    }
}

// Expose these globally
window.showReplyForm = showReplyForm;
window.hideReplyForm = hideReplyForm;
window.toggleReplies = toggleReplies;
window.showRepliesContainer = showRepliesContainer;
window.scrollToNewReply = scrollToNewReply;
window.updateReplyCount = updateReplyCount;
