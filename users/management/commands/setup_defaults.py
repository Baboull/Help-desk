from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from departments.models import Department

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates default users (admin, staff, client) and a default department.'

    def handle(self, *args, **kwargs):
        # Create default department
        dept, created = Department.objects.get_or_create(
            name="General Support",
            defaults={"description": "Main support department for general inquiries."}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created department: {dept.name}"))
        else:
            self.stdout.write(self.style.WARNING(f"Department {dept.name} already exists."))

        # Create Admin
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123", role="admin")
            self.stdout.write(self.style.SUCCESS('Created admin user (admin/admin123)'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))

        # Create Staff
        if not User.objects.filter(username="staff").exists():
            staff = User.objects.create_user("staff", "staff@example.com", "staff123", role="staff")
            staff.department = dept
            staff.is_staff = True
            staff.save()
            self.stdout.write(self.style.SUCCESS('Created staff user (staff/staff123)'))
        else:
            self.stdout.write(self.style.WARNING('Staff user already exists.'))

        # Create Client
        if not User.objects.filter(username="client").exists():
            User.objects.create_user("client", "client@example.com", "client123", role="client")
            self.stdout.write(self.style.SUCCESS('Created client user (client/client123)'))
        else:
            self.stdout.write(self.style.WARNING('Client user already exists.'))

        self.stdout.write(self.style.SUCCESS('Successfully completed setup defaults!'))
