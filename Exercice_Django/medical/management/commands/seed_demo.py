import random
import string
from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError

from medical.models import Patient, Medication, Prescription


def random_date(start_year=1940, end_year=2025):
    start_dt = date(start_year, 1, 1)
    end_dt = date(end_year, 12, 31)
    max_days = (end_dt - start_dt).days
    return start_dt + timedelta(days=random.randint(0, max_days))


def random_interval_between(not_before_date, not_after_date):
    delta_days = (not_after_date - not_before_date).days
    steps = [random.randint(0, delta_days), random.randint(0, delta_days)]
    steps.sort()
    first_delta_days, second_delta_days = steps
    first_date = not_before_date + timedelta(days=first_delta_days)
    second_date = not_before_date + timedelta(days=second_delta_days)
    return (first_date, second_date)


class Command(BaseCommand):
    # TODO when the running env is handled, disable this command when env==production

    help = "Seed the database with demo Patients, Medications and Prescriptions"

    def add_arguments(self, parser):
        parser.add_argument("--patients", type=int, default=10)
        parser.add_argument("--medications", type=int, default=5)
        parser.add_argument("--prescriptions", type=int, default=30)
        parser.add_argument(
            "-k",
            "--keep",
            default=False,
            action="store_true",
            dest="keep_data",
            help="Keep existing data",
        )

    def _validate_inputs(self, n_patients, n_meds, n_prescriptions, keep_data):
        if n_prescriptions == 0:
            # No dependency on other objects; therefore no issue
            return

        if n_patients == 0 and (
            (not Patient.objects.exists())
            or (Patient.objects.exists() and not keep_data)
        ):
            raise CommandError(
                "Prescriptions cannot be created if there is no available Patient."
            )

        if n_meds == 0 and (
            (not Medication.objects.exists())
            or (Medication.objects.exists() and not keep_data)
        ):
            raise CommandError(
                "Prescriptions cannot be created if there is no available Medication."
            )

    def handle(self, *args, **options):
        n_patients = options["patients"]
        n_meds = options["medications"]
        n_prescriptions = options["prescriptions"]
        keep_data = options["keep_data"]

        self._validate_inputs(n_patients, n_meds, n_prescriptions, keep_data)

        if keep_data:
            self.stdout.write("Existing data was kept")
        else:
            Patient.objects.all().delete()
            Medication.objects.all().delete()
            Prescription.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing data was deleted"))

        last_names = [
            "Martin",
            "Bernard",
            "Thomas",
            "Petit",
            "Robert",
            "Richard",
            "Durand",
            "Dubois",
            "Moreau",
            "Laurent",
            "Michel",
            "Garcia",
            "David",
            "Bertrand",
            "Roux",
            "Vincent",
            "Fournier",
            "Morel",
            "Lefebvre",
            "Mercier",
            "Dupont",
            "Lambert",
            "Bonnet",
            "Francois",
            "Martinez",
            "Legrand",
            "Garnier",
            "Faure",
            "Andre",
            "Rousseau",
            "Simon",
            "Leroy",
            "Roux",
            "Girard",
            "Colin",
            "Lefevre",
            "Boyer",
            "Chevalier",
            "Robin",
            "Masson",
            "Picard",
            "Blanc",
            "Gautier",
            "Nicolas",
            "Henry",
            "Perrin",
            "Morin",
            "Mathieu",
            "Clement",
            "Gauthier",
            "Dumont",
            "Lopez",
            "Fontaine",
            "Schmitt",
            "Rodriguez",
            "Dufour",
            "Blanchard",
            "Meunier",
            "Brunet",
            "Roy",
        ]
        first_names = [
            "Jean",
            "Jeanne",
            "Marie",
            "Luc",
            "Lucie",
            "Paul",
            "Camille",
            "Pierre",
            "Sophie",
            "Emma",
            "Louis",
            "Louise",
            "Alice",
            "Gabriel",
            "Jules",
            "Lucas",
            "Hugo",
            "Arthur",
            "Adam",
            "Raphael",
            "Leo",
            "Nathan",
            "Tom",
            "Zoe",
            "Chloe",
            "Ines",
            "Lea",
            "Lena",
            "Eva",
            "Nina",
            "Ethan",
            "Noah",
            "Liam",
            "Rose",
            "Anna",
            "Jade",
            "Maeva",
            "Sarah",
            "Laura",
            "Clara",
            "Julie",
            "Nicolas",
            "Thomas",
            "Antoine",
            "Emilie",
            "Mathilde",
            "Charlotte",
            "Manon",
            "Julia",
            "Elise",
            "Victor",
            "Alex",
            "Samuel",
            "Valentin",
            "Axel",
            "Simon",
            "Romain",
            "Vincent",
            "Marc",
            "David",
        ]

        created_patients = Patient.objects.bulk_create(
            Patient(
                last_name=random.choice(last_names),
                first_name=random.choice(first_names),
                birth_date=random_date(),
            )
            for _ in range(n_patients)
        )

        base_labels = [
            "Paracetamol",
            "Ibuprofen",
            "Amoxicillin",
            "Aspirin",
            "Omeprazole",
            "Metformin",
            "Loratadine",
            "Cetirizine",
            "Azithromycin",
            "Atorvastatin",
            "Simvastatin",
            "Lisinopril",
            "Amlodipine",
            "Metoprolol",
            "Sertraline",
            "Fluoxetine",
            "Escitalopram",
            "Gabapentin",
            "Pregabalin",
            "Tramadol",
            "Oxycodone",
            "Hydrocodone",
            "Morphine",
            "Diazepam",
            "Alprazolam",
            "Clonazepam",
            "Zolpidem",
            "Trazodone",
            "Cyclobenzaprine",
            "Meloxicam",
            "Prednisone",
            "Methylprednisolone",
            "Hydrocortisone",
            "Fluticasone",
            "Montelukast",
            "Albuterol",
            "Fluconazole",
            "Terbinafine",
            "Metronidazole",
            "Ciprofloxacin",
            "Doxycycline",
            "Cephalexin",
            "Nitrofurantoin",
            "Pantoprazole",
            "Ranitidine",
            "Famotidine",
            "Dicyclomine",
            "Ondansetron",
            "Promethazine",
            "Meclizine",
        ]
        medications_to_create = []
        for _ in range(n_meds):
            code = f"MED{random.randint(1000, 9999)}{random.choice(string.ascii_uppercase)}"
            label = (
                f"{random.choice(base_labels)} {random.choice([15, 20, 25, 50, 100, 200, 250, 300, 400, 500, 800, 1000])}"
                + random.choice(["mg", "g", "µg"])
            )
            status = random.choices(
                [Medication.STATUS_ACTIF, Medication.STATUS_SUPPR], weights=[0.8, 0.2]
            )[0]
            medications_to_create.append(
                Medication(code=code, label=label, status=status)
            )
        created_meds = Medication.objects.bulk_create(medications_to_create)

        dummy_prescription_comments = [
            "",
            "Risque d'allergie",
            "Toutes les 4 heures",
            "Jamais à jeun",
            "Expérimental",
        ]
        prescriptions_to_create = []
        end_of_current_year = date(year=date.today().year, month=12, day=31)
        for _ in range(n_prescriptions):
            patient = random.choice(created_patients)
            prescription_begins, prescription_ends = random_interval_between(
                patient.birth_date, end_of_current_year
            )
            prescriptions_to_create.append(
                Prescription(
                    patient=patient,
                    medication=random.choice(created_meds),
                    status=random.choice([k for k, _ in Prescription.STATUS_CHOICES]),
                    begin_date=prescription_begins,
                    end_date=prescription_ends,
                    comment=random.choice(dummy_prescription_comments),
                )
            )
        created_prescriptions = Prescription.objects.bulk_create(
            prescriptions_to_create
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(created_patients)} patient(s), {len(created_meds)} medication(s) and {len(created_prescriptions)} prescription(s)."
            )
        )
