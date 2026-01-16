import random
import string
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from medical.models import Patient, Medication


def random_date(start_year=1940, end_year=2020):
    start_dt = date(start_year, 1, 1)
    end_dt = date(end_year, 12, 31)
    days = (end_dt - start_dt).days
    return start_dt + timedelta(days=random.randint(0, days))


class Command(BaseCommand):
    Patient.objects.all().delete()
    Medication.objects.all().delete()
    help = "Seed the database with demo Patients and Medications"

    def add_arguments(self, parser):
        parser.add_argument("--patients", type=int, default=10)
        parser.add_argument("--medications", type=int, default=5)

    def handle(self, *args, **options):
        n_patients = options["patients"]
        n_meds = options["medications"]

        last_names = [
            "Martin", "Bernard", "Thomas", "Petit", "Robert",
            "Richard", "Durand", "Dubois", "Moreau", "Laurent",
        ]
        first_names = [
            "Jean", "Jeanne", "Marie", "Luc", "Lucie",
            "Paul", "Camille", "Pierre", "Sophie", "Emma",
        ]

        created_patients = []
        for _ in range(n_patients):
            p = Patient.objects.create(
                last_name=random.choice(last_names),
                first_name=random.choice(first_names),
                birth_date=random_date(),
            )
            created_patients.append(p)

        base_labels = [
            "Paracetamol", "Ibuprofen", "Amoxicillin", "Aspirin", "Omeprazole",
            "Metformin", "Loratadine", "Cetirizine", "Azithromycin", "Atorvastatin",
        ]
        created_meds = []
        for i in range(n_meds):
            code = f"MED{random.randint(1000, 9999)}{random.choice(string.ascii_uppercase)}"
            label = f"{random.choice(base_labels)} {random.choice([15, 20, 25, 50, 100, 200, 250, 300, 400, 500, 800, 1000])}" + random.choice(
                ["mg", "g", "µg"])
            status = random.choices([Medication.STATUS_ACTIF, Medication.STATUS_SUPPR], weights=[0.8, 0.2])[0]
            m = Medication.objects.create(code=code, label=label, status=status)
            created_meds.append(m)

        self.stdout.write(self.style.SUCCESS(
            f"Created {len(created_patients)} patients and {len(created_meds)} medications."
        ))
