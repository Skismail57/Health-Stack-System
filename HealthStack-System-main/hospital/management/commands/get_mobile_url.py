"""
Management command to get the mobile access URL
Usage: python manage.py get_mobile_url
"""
from django.core.management.base import BaseCommand
import socket
import qrcode
from io import BytesIO
import sys


class Command(BaseCommand):
    help = 'Get the URL to access HealthStack from mobile devices on your network'

    def add_arguments(self, parser):
        parser.add_argument(
            '--port',
            type=int,
            default=8000,
            help='Port number (default: 8000)',
        )
        parser.add_argument(
            '--qr',
            action='store_true',
            help='Generate QR code for easy mobile access',
        )

    def handle(self, *args, **options):
        port = options['port']
        show_qr = options['qr']
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('  📱 HEALTHSTACK MOBILE ACCESS'))
        self.stdout.write(self.style.SUCCESS('='*70 + '\n'))
        
        # Get local IP address
        try:
            # Create a socket to determine the local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except Exception:
            local_ip = '127.0.0.1'
        
        # Get hostname
        hostname = socket.gethostname()
        
        # Create URLs
        local_url = f'http://localhost:{port}'
        network_url = f'http://{local_ip}:{port}'
        
        self.stdout.write('🌐 Access URLs:\n')
        self.stdout.write(f'  Local (this computer):')
        self.stdout.write(self.style.SUCCESS(f'    {local_url}'))
        self.stdout.write('')
        self.stdout.write(f'  📱 Mobile/Network (same WiFi):')
        self.stdout.write(self.style.SUCCESS(f'    {network_url}'))
        self.stdout.write('')
        
        # Show hostname
        self.stdout.write(f'  💻 Computer Name: {hostname}')
        self.stdout.write(f'  📍 IP Address: {local_ip}')
        self.stdout.write('')
        
        # Instructions
        self.stdout.write('='*70)
        self.stdout.write(self.style.WARNING('\n📋 MOBILE ACCESS INSTRUCTIONS:\n'))
        self.stdout.write('1. Make sure your mobile is on the SAME WiFi network')
        self.stdout.write('2. Open browser on your mobile (Chrome, Safari, etc.)')
        self.stdout.write(f'3. Type this URL: {network_url}')
        self.stdout.write('4. Bookmark it for easy access!')
        self.stdout.write('')
        
        # PWA Instructions
        self.stdout.write(self.style.WARNING('📲 INSTALL AS APP (PWA):\n'))
        self.stdout.write('Android:')
        self.stdout.write('  1. Open the URL in Chrome')
        self.stdout.write('  2. Tap the menu (⋮) > "Add to Home screen"')
        self.stdout.write('  3. Tap "Install"')
        self.stdout.write('')
        self.stdout.write('iOS (iPhone/iPad):')
        self.stdout.write('  1. Open the URL in Safari')
        self.stdout.write('  2. Tap the Share button')
        self.stdout.write('  3. Scroll down and tap "Add to Home Screen"')
        self.stdout.write('  4. Tap "Add"')
        self.stdout.write('')
        
        # QR Code
        if show_qr:
            try:
                self.generate_qr_code(network_url)
            except ImportError:
                self.stdout.write(self.style.WARNING(
                    '⚠️  QR code generation requires: pip install qrcode[pil]'
                ))
        else:
            self.stdout.write('💡 Tip: Run with --qr flag to generate a QR code')
            self.stdout.write('   python manage.py get_mobile_url --qr')
        
        self.stdout.write('')
        self.stdout.write('='*70)
        
        # Network requirements
        self.stdout.write(self.style.WARNING('\n⚠️  REQUIREMENTS:\n'))
        self.stdout.write('✅ Django server must be running:')
        self.stdout.write(f'   python manage.py runserver 0.0.0.0:{port}')
        self.stdout.write('')
        self.stdout.write('✅ Firewall must allow incoming connections on port ' + str(port))
        self.stdout.write('✅ Mobile and computer on SAME WiFi network')
        self.stdout.write('')
        
        # Troubleshooting
        self.stdout.write(self.style.ERROR('🔧 TROUBLESHOOTING:\n'))
        self.stdout.write('If mobile cannot connect:')
        self.stdout.write('  • Check WiFi - both devices on same network?')
        self.stdout.write('  • Windows Firewall - allow Python/Django')
        self.stdout.write('  • Try: python manage.py runserver 0.0.0.0:8000')
        self.stdout.write('  • Check antivirus/security software')
        self.stdout.write('')

    def generate_qr_code(self, url):
        """Generate QR code for mobile scanning"""
        try:
            import qrcode
            
            self.stdout.write(self.style.SUCCESS('📱 QR CODE:\n'))
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            # Print as ASCII art
            qr.print_ascii(invert=True)
            
            self.stdout.write('')
            self.stdout.write('👆 Scan this QR code with your mobile camera')
            self.stdout.write('')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'QR Code generation failed: {str(e)}'))
