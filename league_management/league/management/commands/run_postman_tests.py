import os
import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run Postman collection tests using Newman'

    def handle(self, *args, **kwargs):
        collection_path = os.path.join('postman_collections', 'league_management_tests.postman_collection.json')

        if not os.path.exists(collection_path):
            self.stderr.write(f'Collection file not found: {collection_path}')
            return

        command = f'newman run {collection_path}'

        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.stdout.write(result.stdout.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            self.stderr.write(e.stderr.decode('utf-8'))
            self.stderr.write(f'Tests failed with exit code {e.returncode}')
