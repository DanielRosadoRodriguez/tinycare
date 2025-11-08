(function() {
    'use strict';
    
    document.addEventListener('DOMContentLoaded', function() {
        // Encontrar todos los checkboxes de is_active en la tabla de cambelist
        const checkboxes = document.querySelectorAll('#result_list input[type="checkbox"][name$="-is_active"]');
        
        checkboxes.forEach(function(checkbox) {
            checkbox.addEventListener('click', function(e) {
                if (this.checked) {
                    // Si este checkbox se marca, desmarcar todos los demás
                    checkboxes.forEach(function(otherCheckbox) {
                        if (otherCheckbox !== checkbox) {
                            otherCheckbox.checked = false;
                        }
                    });
                }
            });
        });
    });
})();
