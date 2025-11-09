var loader_script = '<div id="pre-loader">' +
    '<div class="spinner-border text-primary" role="status">' +
    '<span class="sr-only">Loading...</span>' +
    '</div>' +
    '</div>';
window.start_loader = function() {
    if ($('body>#pre-loader').length <= 0) {
        $('body').append(loader_script)
    }
}
window.end_loader = function() {
    var loader = $('body>#pre-loader')
    if (loader.length > 0) {
        loader.remove()
    }
}

// Global CSRF protection for AJAX
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
if (typeof $ !== 'undefined' && csrftoken) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            const safeMethod = /^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type);
            if (!safeMethod && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });
}