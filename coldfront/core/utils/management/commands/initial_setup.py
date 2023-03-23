import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from coldfront.core.utils.common import import_from_settings

base_dir = settings.BASE_DIR

PUBLICATION_ENABLE = import_from_settings('PUBLICATION_ENABLE', False)
GRANT_ENABLE = import_from_settings('GRANT_ENABLE', False)

class Command(BaseCommand):
    help = 'Run setup script to initialize the Coldfront database'

    def add_arguments(self, parser):
         parser.add_argument("-f", "--force_overwrite", help="Force intial_setup script to run with no warning.", action="store_true")

    def handle(self, *args, **options):
            if options['force_overwrite']:
                run_setup()

            else:
                print("""WARNING: Running this command initializes the ColdFront database and may modify/delete data in your existing ColdFront database. This command is typically only run once.""")
                user_response = input("Do you want to proceed?(yes):")
            
                if user_response == "yes":
                    run_setup()
                else:
                    print("Please enter 'yes' if you wish to run intital setup.")

def run_setup():
    call_command('migrate')
    call_command('import_field_of_science_data')
    if GRANT_ENABLE:
        call_command('add_default_grant_options')
    call_command('add_default_project_choices')
    call_command('add_resource_defaults')
    call_command('add_allocation_defaults')
    if PUBLICATION_ENABLE:
        call_command('add_default_publication_sources')
    call_command('add_scheduled_tasks')              

