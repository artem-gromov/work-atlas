from django.core.management.base import BaseCommand

from tenancy.models import Domain, Tenant


class Command(BaseCommand):
    help = "Create a new tenant"

    def add_arguments(self, parser):
        parser.add_argument("--name", required=True)
        parser.add_argument("--domain", required=True)
        parser.add_argument("--schema", required=True)

    def handle(self, *args, **options):
        tenant = Tenant(schema_name=options["schema"], name=options["name"], domain_url=options["domain"])
        tenant.save()
        Domain(domain=options["domain"], tenant=tenant, is_primary=True).save()
        self.stdout.write(self.style.SUCCESS(f"Tenant {tenant.name} created"))

