// Sugarcane FRP JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Clear form functionality
    const clearBtn = document.getElementById('clearBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            document.getElementById('season').value = '';
            document.getElementById('frpForm').submit();
        });
    }
});
