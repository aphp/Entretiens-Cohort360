"""
Seed demo data for development and testing.

Usage:
    python manage.py seed_demo --patients 100 --medications 30
"""

import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from medical.models import Medication, Patient


class Command(BaseCommand):
    help = "Seed the database with demo Patient and Medication data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--patients",
            type=int,
            default=100,
            help="Number of patients to create (default: 100)",
        )
        parser.add_argument(
            "--medications",
            type=int,
            default=30,
            help="Number of medications to create (default: 30)",
        )

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # Create patients
        first_names = [
            "Jean", "Marie", "Pierre", "Sophie", "Michel",
            "Isabelle", "François", "Catherine", "Philippe", "Anne",
            "Bernard", "Monique", "Jacques", "Nicole", "Alain",
        ]
        last_names = [
            "Martin", "Bernard", "Dubois", "Thomas", "Robert",
            "Richard", "Petit", "Durand", "Leroy", "Moreau",
            "Simon", "Laurent", "Lefebvre", "Michel", "Garcia",
        ]

        patients_created = 0
        for i in range(options["patients"]):
            birth_date = date(1940, 1, 1) + timedelta(days=random.randint(0, 25000))
            Patient.objects.create(
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                birth_date=birth_date,
                status="actif",
            )
            patients_created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Created {patients_created} patients")
        )

        # Create medications
        medication_types = [
            ("Paracetamol", ["500mg", "1000mg"]),
            ("Ibuprofene", ["200mg", "400mg"]),
            ("Amoxicilline", ["250mg", "500mg", "1g"]),
            ("Metformine", ["500mg", "850mg", "1000mg"]),
            ("Omeprazole", ["10mg", "20mg", "40mg"]),
            ("Aspirine", ["100mg", "300mg", "500mg"]),
            ("Atorvastatine", ["10mg", "20mg", "40mg"]),
            ("Ramipril", ["2.5mg", "5mg", "10mg"]),
            ("Amlodipine", ["5mg", "10mg"]),
            ("Levothyroxine", ["25mcg", "50mcg", "100mcg"]),
        ]

        medications_created = 0
        med_count = 0
        for med_name, dosages in medication_types:
            for dosage in dosages:
                if med_count >= options["medications"]:
                    break
                code = f"MED{str(med_count + 1).zfill(3)}"
                Medication.objects.create(
                    code=code,
                    label=f"{med_name} {dosage}",
                    status="actif",
                )
                medications_created += 1
                med_count += 1
            if med_count >= options["medications"]:
                break

        self.stdout.write(
            self.style.SUCCESS(f"Created {medications_created} medications")
        )

        self.stdout.write(self.style.SUCCESS("Database seeding complete!"))
