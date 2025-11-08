/**
 * Drag-and-drop file upload para avisos de privacidad
 */
(function() {
    'use strict';
    
    document.addEventListener('DOMContentLoaded', function() {
        const fileInput = document.querySelector('input[type="file"][name="file"]');
        if (!fileInput) return;
        
        const formRow = fileInput.closest('.form-row');
        if (!formRow) return;
        
        // Crear área de drag-and-drop
        const dropZone = document.createElement('div');
        dropZone.className = 'privacy-notice-dropzone';
        dropZone.innerHTML = `
            <div class="dropzone-content">
                <p class="dropzone-icon">📄</p>
                <p class="dropzone-text">Arrastra tu archivo .md aquí o haz clic para seleccionar</p>
                <p class="dropzone-hint">Solo archivos Markdown (.md)</p>
            </div>
            <div class="dropzone-file-info" style="display: none;">
                <p class="file-name"></p>
                <button type="button" class="dropzone-clear">✕ Eliminar</button>
            </div>
        `;
        
        // Insertar después del input original
        formRow.appendChild(dropZone);
        
        const dropContent = dropZone.querySelector('.dropzone-content');
        const fileInfo = dropZone.querySelector('.dropzone-file-info');
        const fileName = dropZone.querySelector('.file-name');
        const clearBtn = dropZone.querySelector('.dropzone-clear');
        
        // Hacer que el dropzone abra el file input al hacer clic
        dropContent.addEventListener('click', function() {
            fileInput.click();
        });
        
        // Prevenir comportamiento por defecto del drag
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        // Resaltar zona de drop
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, function() {
                dropZone.classList.add('dragover');
            }, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, function() {
                dropZone.classList.remove('dragover');
            }, false);
        });
        
        // Manejar drop
        dropZone.addEventListener('drop', function(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                handleFiles(files);
            }
        });
        
        // Manejar selección de archivo
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                handleFiles(this.files);
            }
        });
        
        // Manejar archivos
        function handleFiles(files) {
            const file = files[0];
            
            // Validar extensión
            if (!file.name.endsWith('.md')) {
                alert('Solo se permiten archivos .md (Markdown)');
                return;
            }
            
            // Mostrar información del archivo
            fileName.textContent = `📄 ${file.name} (${formatBytes(file.size)})`;
            dropContent.style.display = 'none';
            fileInfo.style.display = 'block';
            dropZone.classList.add('has-file');
        }
        
        // Botón para limpiar
        clearBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            fileInput.value = '';
            dropContent.style.display = 'block';
            fileInfo.style.display = 'none';
            dropZone.classList.remove('has-file');
        });
        
        // Función auxiliar para formatear bytes
        function formatBytes(bytes, decimals = 2) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const dm = decimals < 0 ? 0 : decimals;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
        }
        
        // Si ya hay un archivo cargado, mostrar su información
        if (fileInput.value || fileInput.files.length > 0) {
            const existingFile = fileInput.files[0];
            if (existingFile) {
                handleFiles([existingFile]);
            }
        }
    });
})();
