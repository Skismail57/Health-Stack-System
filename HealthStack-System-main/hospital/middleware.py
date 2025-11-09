"""
IP Whitelist Middleware
Restricts access to specific IP addresses
"""
from django.http import HttpResponseForbidden
from django.conf import settings


class IPWhitelistMiddleware:
    """
    Middleware to restrict access to whitelisted IP addresses
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Define allowed IPs
        self.allowed_ips = getattr(settings, 'ALLOWED_IPS', [])
    
    def __call__(self, request):
        # Get client IP
        ip = self.get_client_ip(request)
        
        # If whitelist is empty, allow all (development mode)
        if not self.allowed_ips:
            return self.get_response(request)
        
        # Check if IP is allowed
        if ip not in self.allowed_ips:
            return HttpResponseForbidden(
                '<h1>Access Denied</h1>'
                f'<p>Your IP address ({ip}) is not authorized to access this application.</p>'
                '<p>Please contact the administrator.</p>'
            )
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
