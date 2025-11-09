"""
Management command to share HealthStack online
Provides instructions for internet access
Usage: python manage.py share_online
"""
from django.core.management.base import BaseCommand
import subprocess
import sys


class Command(BaseCommand):
    help = 'Get instructions to share HealthStack on the internet'

    def add_arguments(self, parser):
        parser.add_argument(
            '--method',
            type=str,
            choices=['ngrok', 'serveo', 'heroku', 'all'],
            default='all',
            help='Which method to show instructions for',
        )

    def handle(self, *args, **options):
        method = options['method']
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('  🌍 SHARE HEALTHSTACK ON THE INTERNET'))
        self.stdout.write(self.style.SUCCESS('='*70 + '\n'))
        
        if method == 'all' or method == 'ngrok':
            self.show_ngrok()
        
        if method == 'all' or method == 'serveo':
            self.show_serveo()
        
        if method == 'all' or method == 'heroku':
            self.show_heroku()
        
        self.show_comparison()
        self.show_security_notes()

    def show_ngrok(self):
        """Show ngrok setup instructions"""
        self.stdout.write(self.style.WARNING('\n🚀 METHOD 1: NGROK (FASTEST - 5 MINUTES)\n'))
        
        self.stdout.write('📥 SETUP:')
        self.stdout.write('  1. Download ngrok: https://ngrok.com/download')
        self.stdout.write('  2. Sign up (free): https://dashboard.ngrok.com/signup')
        self.stdout.write('  3. Get auth token: https://dashboard.ngrok.com/get-started/your-authtoken')
        self.stdout.write('')
        
        self.stdout.write('⚙️  CONFIGURE:')
        self.stdout.write('  ngrok config add-authtoken YOUR_TOKEN')
        self.stdout.write('')
        
        self.stdout.write('▶️  RUN:')
        self.stdout.write(self.style.SUCCESS('  Terminal 1: python manage.py runserver'))
        self.stdout.write(self.style.SUCCESS('  Terminal 2: ngrok http 8000'))
        self.stdout.write('')
        
        self.stdout.write('🌐 YOUR PUBLIC URL:')
        self.stdout.write('  Ngrok will show: https://abc123.ngrok-free.app')
        self.stdout.write('  Share this URL with ANYONE - works from ANYWHERE! 🌍')
        self.stdout.write('')
        
        self.stdout.write('✅ FEATURES:')
        self.stdout.write('  • HTTPS automatic (secure)')
        self.stdout.write('  • Works on any network (WiFi, mobile data, anywhere)')
        self.stdout.write('  • Bypasses firewalls')
        self.stdout.write('  • Request inspector at http://localhost:4040')
        self.stdout.write('')
        
        self.stdout.write('⚠️  LIMITATIONS (Free):')
        self.stdout.write('  • URL changes each restart')
        self.stdout.write('  • 40 requests/minute limit')
        self.stdout.write('  • Shows ngrok banner')
        self.stdout.write('')

    def show_serveo(self):
        """Show serveo setup instructions"""
        self.stdout.write(self.style.WARNING('\n🚀 METHOD 2: SERVEO (NO INSTALLATION)\n'))
        
        self.stdout.write('▶️  RUN:')
        self.stdout.write(self.style.SUCCESS('  Terminal 1: python manage.py runserver'))
        self.stdout.write(self.style.SUCCESS('  Terminal 2: ssh -R 80:localhost:8000 serveo.net'))
        self.stdout.write('')
        
        self.stdout.write('🌐 YOUR PUBLIC URL:')
        self.stdout.write('  Serveo shows: https://abc123.serveo.net')
        self.stdout.write('')
        
        self.stdout.write('✅ FEATURES:')
        self.stdout.write('  • No installation needed')
        self.stdout.write('  • HTTPS included')
        self.stdout.write('  • Free forever')
        self.stdout.write('')
        
        self.stdout.write('⚠️  LIMITATIONS:')
        self.stdout.write('  • URL changes each restart')
        self.stdout.write('  • Less reliable than ngrok')
        self.stdout.write('')

    def show_heroku(self):
        """Show Heroku deployment instructions"""
        self.stdout.write(self.style.WARNING('\n🚀 METHOD 3: HEROKU (PERMANENT URL)\n'))
        
        self.stdout.write('📥 SETUP:')
        self.stdout.write('  1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli')
        self.stdout.write('  2. heroku login')
        self.stdout.write('  3. heroku create healthstack-demo')
        self.stdout.write('')
        
        self.stdout.write('📝 CREATE Procfile:')
        self.stdout.write('  web: daphne -b 0.0.0.0 -p $PORT healthstack.asgi:application')
        self.stdout.write('')
        
        self.stdout.write('🚀 DEPLOY:')
        self.stdout.write('  git init')
        self.stdout.write('  git add .')
        self.stdout.write('  git commit -m "Deploy"')
        self.stdout.write('  git push heroku main')
        self.stdout.write('')
        
        self.stdout.write('🌐 YOUR PUBLIC URL:')
        self.stdout.write('  https://healthstack-demo.herokuapp.com')
        self.stdout.write('')
        
        self.stdout.write('✅ FEATURES:')
        self.stdout.write('  • Permanent URL (never changes)')
        self.stdout.write('  • Free tier available')
        self.stdout.write('  • Professional hosting')
        self.stdout.write('  • Auto-scaling')
        self.stdout.write('')

    def show_comparison(self):
        """Show comparison table"""
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS('\n📊 QUICK COMPARISON:\n'))
        
        self.stdout.write('┌─────────────┬──────────┬──────────────┬───────────────┐')
        self.stdout.write('│ Method      │ Setup    │ Free         │ Best For      │')
        self.stdout.write('├─────────────┼──────────┼──────────────┼───────────────┤')
        self.stdout.write('│ Ngrok       │ 5 min    │ Yes (limited)│ Quick demos   │')
        self.stdout.write('│ Serveo      │ 2 min    │ Yes (full)   │ Testing       │')
        self.stdout.write('│ Heroku      │ 30 min   │ Yes          │ Production    │')
        self.stdout.write('└─────────────┴──────────┴──────────────┴───────────────┘')
        self.stdout.write('')

    def show_security_notes(self):
        """Show security recommendations"""
        self.stdout.write(self.style.ERROR('\n🔒 IMPORTANT SECURITY NOTES:\n'))
        
        self.stdout.write('Before exposing to internet, update settings.py:')
        self.stdout.write('')
        self.stdout.write('  ALLOWED_HOSTS = [')
        self.stdout.write('      "abc123.ngrok-free.app",  # Your ngrok URL')
        self.stdout.write('      "*.ngrok-free.app",')
        self.stdout.write('  ]')
        self.stdout.write('')
        self.stdout.write('  CSRF_TRUSTED_ORIGINS = [')
        self.stdout.write('      "https://*.ngrok-free.app",')
        self.stdout.write('  ]')
        self.stdout.write('')
        
        self.stdout.write('✅ Your authentication is already secure!')
        self.stdout.write('✅ Users must login to access data')
        self.stdout.write('✅ Role permissions are enforced')
        self.stdout.write('')
        
        self.stdout.write('='*70)
        self.stdout.write(self.style.SUCCESS('\n📱 SHARE THE LINK AND IT WORKS ANYWHERE! 🌍\n'))
