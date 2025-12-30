let uploadedImage = null;
let existingRemoved = false;

document.addEventListener('DOMContentLoaded', function () {
    // Query DOM elements at runtime
    const imageInput = document.getElementById('imageInput');
    const previewContainer = document.getElementById('imagePreview');
    const btnRemoveSelected = document.getElementById('btnRemoveSelected');
    const btnDeleteSaved = document.getElementById('btnDeleteSaved');

    console.debug('addpro.js initialized', { imageInputExists: !!imageInput, previewExists: !!previewContainer });

    if (imageInput) {
        imageInput.addEventListener('change', function (e) {
            console.debug('imageInput.change triggered', e);
            const file = e.target.files[0];
            if (!file) return;

            if (file.size > 10 * 1024 * 1024) {
                alert(`${file.name} is too large. Max size is 10MB`);
                e.target.value = '';
                return;
            }

            if (!file.type.match('image.*')) {
                alert(`${file.name} is not an image file`);
                e.target.value = '';
                return;
            }

            const reader = new FileReader();
            reader.onload = function (evt) {
                uploadedImage = {
                    file: file,
                    url: evt.target.result
                };
                console.debug('file read, rendering preview', uploadedImage);
                // update filename indicator if present
                try {
                    const sel = window.__addpro_selectedFilename || document.getElementById('selectedFilename');
                    if (sel) { sel.textContent = file.name; sel.style.display = 'block'; window.__addpro_selectedFilename = sel; }
                } catch (e) { /* ignore */ }
                renderImagePreview();
            };
            reader.readAsDataURL(file);
        });
    }

    // wire action buttons (may not be present on every page)
    if (btnRemoveSelected) btnRemoveSelected.addEventListener('click', removeImage);
    if (btnDeleteSaved) btnDeleteSaved.addEventListener('click', removeExistingImage);

    // Expose btn variables to outer scope for functions that reference them
    window.__addpro_btns = { btnRemoveSelected, btnDeleteSaved };

    // Initial render to set proper button visibility based on server-rendered markup
    renderImagePreview();
});

// Render single image preview
function renderImagePreview() {
    const previewContainer = document.getElementById('imagePreview');
    // If a newly uploaded image exists, show it (replaces existing preview)
    if (uploadedImage) {
        previewContainer.classList.remove('empty');
        // include explicit inline sizing to prevent very high-resolution images from stretching container
        previewContainer.innerHTML = `
            <div class="preview-thumb">
                <img src="${uploadedImage.url}" alt="Preview" style="max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;display:block;" />
                <div class="remove-btn" onclick="removeImage()">×</div>
            </div>
        `;
        // mark remove flag as 0 (we're replacing existing image)
        document.getElementById('removeImageInput').value = '0';
        existingRemoved = false;
        // show remove-selected button, hide delete-saved (we're previewing a new file)
        // If buttons were not queried earlier, fallback to window-stored references
        const btns = window.__addpro_btns || {};
        const btnRemoveSelectedLocal = btns.btnRemoveSelected || document.getElementById('btnRemoveSelected');
        const btnDeleteSavedLocal = btns.btnDeleteSaved || document.getElementById('btnDeleteSaved');
        if (btnRemoveSelectedLocal) btnRemoveSelectedLocal.style.display = 'inline-block';
        if (btnDeleteSavedLocal) btnDeleteSavedLocal.style.display = 'none';
        return;
    }

    // No uploaded image; if existing image was removed, clear preview
    if (existingRemoved) {
        previewContainer.classList.add('empty');
        previewContainer.innerHTML = `<span class="image-preview-text">No images uploaded</span>`;
        const btns2 = window.__addpro_btns || {};
        const btnRemoveSelectedLocal2 = btns2.btnRemoveSelected || document.getElementById('btnRemoveSelected');
        const btnDeleteSavedLocal2 = btns2.btnDeleteSaved || document.getElementById('btnDeleteSaved');
    if (btnRemoveSelectedLocal2) btnRemoveSelectedLocal2.style.display = 'none';
    if (btnDeleteSavedLocal2) btnDeleteSavedLocal2.style.display = 'none';
    try { const sel2 = window.__addpro_selectedFilename || document.getElementById('selectedFilename'); if (sel2) sel2.style.display = 'none'; } catch (e) {}
    return;
    }

    // Fallback: leave existing preview intact (server-rendered) or show empty state
    if (previewContainer.querySelector('img')) {
        previewContainer.classList.remove('empty');
        // show delete-saved only if a server-rendered existingPreview exists
        const btns3 = window.__addpro_btns || {};
        const btnRemoveSelectedLocal3 = btns3.btnRemoveSelected || document.getElementById('btnRemoveSelected');
        const btnDeleteSavedLocal3 = btns3.btnDeleteSaved || document.getElementById('btnDeleteSaved');
    if (document.getElementById('existingPreview') && btnDeleteSavedLocal3) btnDeleteSavedLocal3.style.display = 'inline-block';
    if (btnRemoveSelectedLocal3) btnRemoveSelectedLocal3.style.display = 'none';
    try { const sel3 = window.__addpro_selectedFilename || document.getElementById('selectedFilename'); if (sel3) sel3.style.display = 'none'; } catch (e) {}
    return;
    }
    previewContainer.classList.add('empty');
    previewContainer.innerHTML = `<span class="image-preview-text">No images uploaded</span>`;
    const btns4 = window.__addpro_btns || {};
    const btnRemoveSelectedLocal4 = btns4.btnRemoveSelected || document.getElementById('btnRemoveSelected');
    const btnDeleteSavedLocal4 = btns4.btnDeleteSaved || document.getElementById('btnDeleteSaved');
    if (btnRemoveSelectedLocal4) btnRemoveSelectedLocal4.style.display = 'none';
    if (btnDeleteSavedLocal4) btnDeleteSavedLocal4.style.display = 'none';
    try { const filenameEl4 = window.__addpro_selectedFilename || document.getElementById('selectedFilename'); if (filenameEl4) filenameEl4.style.display = 'none'; } catch (e) {}
}

// Remove image
function removeImage() {
    uploadedImage = null;
    document.getElementById('imageInput').value = '';
    try { const sel = window.__addpro_selectedFilename || document.getElementById('selectedFilename'); if (sel) sel.style.display = 'none'; } catch (e) {}
    renderImagePreview();
}

// Remove the server-side existing image (sets hidden flag)
function removeExistingImage() {
    existingRemoved = true;
    // set hidden form flag so server will delete image on POST
    document.getElementById('removeImageInput').value = '1';
    // remove the server-rendered preview thumb from DOM
    const existing = document.getElementById('existingPreview');
    if (existing) existing.remove();
    try { const sel = window.__addpro_selectedFilename || document.getElementById('selectedFilename'); if (sel) sel.style.display = 'none'; } catch (e) {}
    renderImagePreview();
}

// Drag and drop
const uploadArea = document.querySelector('.image-upload-area');

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#764ba2';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = '#667eea';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#667eea';
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length === 0) return;
    
    // Only take the first file
    const file = files[0];
    const imageInput = document.getElementById('imageInput');
    
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    imageInput.files = dataTransfer.files;
    
    imageInput.dispatchEvent(new Event('change'));
});

// global fallback for inline onchange
function onImageInputChange(fileInput) {
    try {
        const file = fileInput.files[0];
        if (!file) return;
        if (file.size > 10 * 1024 * 1024) {
            alert(`${file.name} is too large. Max size is 10MB`);
            fileInput.value = '';
            return;
        }
        if (!file.type.match('image.*')) {
            alert(`${file.name} is not an image file`);
            fileInput.value = '';
            return;
        }
        const reader = new FileReader();
        reader.onload = function (evt) {
            uploadedImage = { file: file, url: evt.target.result };
            renderImagePreview();
        };
        reader.readAsDataURL(file);
    } catch (err) {
        console.error('onImageInputChange error', err);
    }
}