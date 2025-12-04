from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Reset database by dropping all tables and running migrations'

    def handle(self, *args, **options):
        self.stdout.write('Dropping all tables...')
        
        with connection.cursor() as cursor:
            # Get all tables
            cursor.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
            """)
            tables = cursor.fetchall()
            
            # Drop all tables
            for table in tables:
                self.stdout.write(f'Dropping table: {table[0]}')
                cursor.execute(f'DROP TABLE IF EXISTS "{table[0]}" CASCADE')
        
        self.stdout.write(self.style.SUCCESS('All tables dropped successfully'))
        
        # Run migrations
        self.stdout.write('Running migrations...')
        from django.core.management import call_command
        call_command('migrate')
        
        self.stdout.write(self.style.SUCCESS('Database reset complete!'))
