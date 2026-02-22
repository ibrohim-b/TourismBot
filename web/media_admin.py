"""
Custom form fields and utilities for admin media management
"""
from wtforms import StringField
from wtforms.widgets import TextInput
from markupsafe import Markup
from pathlib import Path

class MediaWidget(TextInput):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        
        media_type = kwargs.pop('data-media-type', 'images')
        entity_type = kwargs.pop('data-entity-type', 'general')
        entity_id = kwargs.pop('data-entity-id', '')

        field_id = field.id
        field_name = field.name
        field_value = field.data or ''
        
        hidden_input_html = f'<input type="text" id="{field_id}" name="{field_name}" value="{field_value}" style="display:none;">'
        ui_html = f'''
        <div class="media-field-wrapper" data-field="{field_id}">
            <div class="media-input-group">
                <input type="file" id="file_{field_id}" class="media-file-input"
                       data-field="{field_id}" data-media-type="{media_type}"
                       data-entity-type="{entity_type}" data-entity-id="{entity_id}" />
                <label for="file_{field_id}" class="media-upload-label">
                    📁 Choose File or Drag &amp; Drop
                </label>
                <div class="media-upload-progress" id="progress_{field_id}" style="display:none;">
                    <div class="progress-bar"></div>
                    <span class="progress-text">Uploading...</span>
                </div>
            </div>
            <div class="media-preview-container" id="preview_{field_id}">
                {get_media_preview(field_value, media_type) if field_value else ''}
            </div>
            <div class="media-path" id="path_{field_id}">{field_value or 'No file selected'}</div>
        </div>
        '''

        return Markup(hidden_input_html + ui_html)


def get_media_preview(file_path, media_type):
    """Generate HTML preview for media file"""
    if not file_path:
        return ''
    
    root_dir = Path(__file__).parent.parent
    full_path = root_dir / file_path
    
    if not full_path.exists():
        return f'<div class="media-preview-error">File not found: {file_path}</div>'
    
    if media_type == 'images':
        return f'<img src="/{file_path}" alt="Preview" class="media-preview-image">'
    elif media_type == 'audio':
        return f'<audio controls class="media-preview-audio"><source src="/{file_path}"></audio>'
    elif media_type == 'videos':
        return f'<video controls class="media-preview-video"><source src="/{file_path}"></video>'
    else:
        return f'<a href="/{file_path}" target="_blank" class="media-preview-link">📄 {Path(file_path).name}</a>'


class MediaField(StringField):
    """Custom field for media upload and management"""
    
    def __init__(self, label=None, media_type='images', entity_type='general', **kwargs):
        super().__init__(label, **kwargs)
        self.media_type = media_type
        self.entity_type = entity_type
        self.widget = MediaWidget()


MEDIA_CSS = '''
<style>
.media-field-wrapper {
    margin: 15px 0;
}

.media-input-group {
    position: relative;
    margin-bottom: 15px;
}

.media-file-input {
    display: none;
}

.media-upload-label {
    display: block;
    padding: 30px;
    border: 2px dashed #667eea;
    border-radius: 8px;
    background: #f8f9ff;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
    font-weight: 500;
    color: #667eea;
}

.media-upload-label:hover {
    background: #eef1ff;
    border-color: #764ba2;
}

.media-upload-label.dragover {
    background: #eef1ff;
    border-color: #764ba2;
    box-shadow: 0 0 10px rgba(102, 126, 234, 0.2);
}

.media-upload-progress {
    margin: 10px 0;
    padding: 10px;
    background: #f5f5f5;
    border-radius: 5px;
}

.progress-bar {
    height: 4px;
    background: #667eea;
    border-radius: 2px;
    animation: progress 1.5s ease-in-out infinite;
}

@keyframes progress {
    0% { width: 0%; }
    50% { width: 70%; }
    100% { width: 100%; }
}

.progress-text {
    font-size: 12px;
    color: #666;
}

.media-preview-container {
    margin: 15px 0;
    text-align: center;
}

.media-preview-image {
    max-width: 100%;
    max-height: 300px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.media-preview-audio {
    width: 100%;
    margin: 10px 0;
}

.media-preview-video {
    max-width: 100%;
    max-height: 300px;
    border-radius: 8px;
}

.media-preview-link {
    display: inline-block;
    padding: 10px 15px;
    background: #667eea;
    color: white;
    border-radius: 5px;
    text-decoration: none;
    margin: 10px 0;
}

.media-preview-link:hover {
    background: #764ba2;
}

.media-preview-error {
    padding: 10px;
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
    border-radius: 5px;
    font-size: 12px;
}

.media-path {
    padding: 8px 12px;
    background: #f5f5f5;
    border-radius: 5px;
    font-size: 12px;
    color: #666;
    word-break: break-all;
    font-family: monospace;
}

.media-path.success {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.media-path.error {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.media-upload-status {
    padding: 10px 12px;
    margin: 10px 0;
    border-radius: 5px;
    font-size: 13px;
}

.media-upload-status.success {
    background: #d4edda;
    color: #155724;
}

.media-upload-status.error {
    background: #f8d7da;
    color: #721c24;
}
</style>
'''

MEDIA_JS = '''
<script>
function initMediaUploads() {
    document.querySelectorAll('.media-file-input').forEach(input => {
        if (input.dataset.initialized) return;
        input.dataset.initialized = 'true';
        
        const fieldId = input.dataset.field;
        const label = document.querySelector(`label[for="file_${fieldId}"]`);
        const pathDiv = document.querySelector(`#path_${fieldId}`);
        const previewDiv = document.querySelector(`#preview_${fieldId}`);
        const progressDiv = document.querySelector(`#progress_${fieldId}`);
        
        if (!label || !pathDiv || !previewDiv || !progressDiv) return;
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            label.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            label.addEventListener(eventName, () => label.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            label.addEventListener(eventName, () => label.classList.remove('dragover'), false);
        });

        label.addEventListener('drop', (e) => {
            input.files = e.dataTransfer.files;
            handleMediaUpload(input, fieldId, pathDiv, previewDiv, progressDiv);
        }, false);

        input.addEventListener('change', () => {
            handleMediaUpload(input, fieldId, pathDiv, previewDiv, progressDiv);
        });
    });
}

async function handleMediaUpload(fileInput, fieldId, pathDiv, previewDiv, progressDiv) {
    const file = fileInput.files[0];
    if (!file) return;

    const mediaType = fileInput.dataset.mediaType;

    progressDiv.style.display = 'block';
    
    const formData = new FormData();
    formData.append('file', file);

    try {
        const url = `/api/media/upload?media_type=${mediaType}`;
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        progressDiv.style.display = 'none';

        if (response.ok) {
            const data = await response.json();
            
            console.log('[Media] Upload success:', data.path);
            console.log('[Media] Looking for input with id:', fieldId);
            
            const hiddenInput = document.getElementById(fieldId);
            console.log('[Media] Found input:', hiddenInput);
            
            if (hiddenInput) {
                hiddenInput.value = data.path;
                console.log('[Media] Set value to:', hiddenInput.value);
            } else {
                console.error('[Media] Input not found!');
            }

            pathDiv.textContent = data.path;
            pathDiv.classList.add('success');
            pathDiv.classList.remove('error');

            updateMediaPreview(previewDiv, data.path, mediaType);
            showMediaStatus(fieldId, 'success', '✅ File uploaded successfully!');
        } else {
            const data = await response.json();
            pathDiv.textContent = 'Error: ' + (data.detail || 'Upload failed');
            pathDiv.classList.add('error');
            pathDiv.classList.remove('success');
            showMediaStatus(fieldId, 'error', '❌ ' + (data.detail || 'Upload failed'));
        }
    } catch (error) {
        progressDiv.style.display = 'none';
        pathDiv.textContent = 'Error: ' + error.message;
        pathDiv.classList.add('error');
        pathDiv.classList.remove('success');
        showMediaStatus(fieldId, 'error', '❌ ' + error.message);
    }
}

function updateMediaPreview(container, filePath, mediaType) {
    container.innerHTML = '';
    
    if (mediaType === 'images') {
        const img = document.createElement('img');
        img.src = '/' + filePath;
        img.className = 'media-preview-image';
        img.alt = 'Preview';
        container.appendChild(img);
    } else if (mediaType === 'audio') {
        const audio = document.createElement('audio');
        audio.controls = true;
        audio.className = 'media-preview-audio';
        const source = document.createElement('source');
        source.src = '/' + filePath;
        audio.appendChild(source);
        container.appendChild(audio);
    } else if (mediaType === 'videos') {
        const video = document.createElement('video');
        video.controls = true;
        video.className = 'media-preview-video';
        const source = document.createElement('source');
        source.src = '/' + filePath;
        video.appendChild(source);
        container.appendChild(video);
    } else {
        const link = document.createElement('a');
        link.href = '/' + filePath;
        link.target = '_blank';
        link.className = 'media-preview-link';
        link.textContent = '📄 ' + filePath.split('/').pop();
        container.appendChild(link);
    }
}

function showMediaStatus(fieldId, status, message) {
    const wrapper = document.querySelector(`[data-field="${fieldId}"]`);
    if (!wrapper) return;

    const existing = wrapper.querySelector('.media-upload-status');
    if (existing) existing.remove();

    const statusDiv = document.createElement('div');
    statusDiv.className = `media-upload-status ${status}`;
    statusDiv.textContent = message;
    
    const previewDiv = wrapper.querySelector('.media-preview-container');
    if (previewDiv) {
        previewDiv.parentNode.insertBefore(statusDiv, previewDiv.nextSibling);
    }

    setTimeout(() => statusDiv.remove(), 5000);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMediaUploads);
} else {
    initMediaUploads();
}

const observer = new MutationObserver(() => initMediaUploads());
observer.observe(document.body, {
    childList: true,
    subtree: true
});
</script>
'''
