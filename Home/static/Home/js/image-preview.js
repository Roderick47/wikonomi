/**
 * Reusable image preview script for WIKONOMI
 * Automatically displays a preview of an uploaded image with a clear button.
 */

// Inject required styles once
const styleId = 'image-preview-styles';
if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
        .image-preview-container {
            position: relative;
            display: inline-block;
        }
        .image-preview-container img {
            display: block;
        }
        .image-preview-clear {
            position: absolute;
            top: -10px;
            right: -10px;
            background: #ef4444;
            color: white;
            border: 2px solid white;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transition: transform 0.2s ease, background 0.2s ease;
            z-index: 10;
        }
        .image-preview-clear:hover {
            transform: scale(1.1);
            background: #dc2626;
        }
    `;
    document.head.appendChild(style);
}

function setupImagePreview(inputElement) {
    // Create preview container if it doesn't exist
    let previewContainer = inputElement.parentElement.querySelector('.image-preview-container');
    if (!previewContainer) {
        previewContainer = document.createElement('div');
        previewContainer.className = 'image-preview-container mt-3';
        previewContainer.style.display = 'none';

        const previewImg = document.createElement('img');
        previewImg.className = 'img-thumbnail';
        previewImg.style.maxHeight = '200px';

        // Create clear button
        const clearBtn = document.createElement('div');
        clearBtn.className = 'image-preview-clear';
        clearBtn.innerHTML = '<i class="fas fa-times small"></i>';
        clearBtn.title = 'Remove image';

        clearBtn.addEventListener('click', function () {
            inputElement.value = ''; // Clear file input
            previewContainer.style.display = 'none';
            previewImg.src = '';

            // Dispatch change event manually in case other scripts are listening
            inputElement.dispatchEvent(new Event('change'));
        });

        previewContainer.appendChild(previewImg);
        previewContainer.appendChild(clearBtn);
        inputElement.insertAdjacentElement('afterend', previewContainer);
    }

    const previewImg = previewContainer.querySelector('img');

    inputElement.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                previewImg.src = e.target.result;
                previewContainer.style.display = 'inline-block';
            }

            reader.readAsDataURL(file);
        } else {
            previewContainer.style.display = 'none';
        }
    });
}

// Auto-initialize on DOM load and also handle HTMX content updates
function initAllImagePreviews() {
    const inputs = document.querySelectorAll('.image-preview-input');
    inputs.forEach(input => {
        if (!input.dataset.previewInitialized) {
            setupImagePreview(input);
            input.dataset.previewInitialized = 'true';
        }
    });
}

document.addEventListener('DOMContentLoaded', initAllImagePreviews);
document.addEventListener('htmx:afterSettle', initAllImagePreviews);
