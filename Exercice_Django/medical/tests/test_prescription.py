from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from medical.models import Patient, Medication, Prescription


class ApiPrescriptionTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Patients
        self.patient1 = Patient.objects.create(last_name="Contona", first_name="Eric", birth_date="1982-03-10")
        self.patient2 = Patient.objects.create(last_name="Dion", first_name="Celine", birth_date="1980-05-20")

        # Medications
        
        self.medication1 = Medication.objects.create(code="PHYTO55", label="Phytoxil", status=Medication.STATUS_ACTIF)
        self.medication2 = Medication.objects.create(code="FER525", label="Frevex", status=Medication.STATUS_ACTIF)
        self.medication3 = Medication.objects.create(code="MAXI01", label="Maxilase", status=Medication.STATUS_SUPPR)

        # Prescriptions
        Prescription.objects.create(
            patient=self.patient1,
            medication=self.medication1,
            prescription_start_date="2023-01-01",
            prescription_end_date="2023-01-10",
            presscription_status="valide",
            commentaire="Prescription 1"
        )
        Prescription.objects.create(
            patient=self.patient2,
            medication=self.medication2,
            prescription_start_date="2023-02-01",
            prescription_end_date="2023-02-15",
            presscription_status="en_attente",
            commentaire="Prescription 2"
        )

    def test_prescription_list(self):
        """Test pour récupérer la liste des prescriptions."""
        url = reverse("prescription-list")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.json()), 2)

    def test_prescription_filter_by_name(self):
        """Test pour filtrer les prescriptions par nom."""
        url = reverse("prescription-list")
        params = {"nom": "Contona"}
        r = self.client.get(url, params)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data), 1)  
        self.assertEqual(data[0]["patient"], self.patient1.id) 

    def test_prescription_filter_by_date(self):
        """Test pour filtrer les prescriptions par une période de dates."""
        url = reverse("prescription-list")
        params = {
            "active_period_min": "2023-01-01",
            "active_period_max": "2023-01-31"
        }
        r = self.client.get(url, params)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(all(
            "2023-01-01" <= p["prescription_start_date"] <= "2023-01-31"
            for p in data
        ))
    def test_prescription_create_valid(self):
        """Test pour créer une prescription valide."""
        url = reverse("prescription-list")
        payload = {
            "patient": self.patient1.id,
            "medication": self.medication1.id,
            "prescription_start_date": "2023-03-01",
            "prescription_end_date": "2023-03-10",
            "presscription_status": "valide",
            "commentaire": "Nouvelle prescription valide"
        }
        r = self.client.post(url, payload, format="json")
        self.assertEqual(r.status_code, 201)  
        self.assertEqual(Prescription.objects.count(), 3)
    
    def test_prescription_create_invalid_patient(self):
        """Test pour vérifier que le champ patient est obligatoire."""
        url = reverse("prescription-list")
        payload = {
            "medication": self.medication1.id,
            "prescription_start_date": "2023-03-10",
            "prescription_end_date": "2023-03-30",
            "presscription_status": "valide",
            "commentaire": "Prescription avec patient manquant"
        }
        r = self.client.post(url, payload, format="json")
        self.assertEqual(r.status_code, 400)  
        self.assertIn("patient", r.json())
    
    def test_prescription_create_invalid_medication(self):
        """Test pour vérifier que le champ medication est obligatoire."""
        url = reverse("prescription-list")
        payload = {
            "patient": self.patient1.id,
            "prescription_start_date": "2023-03-10",
            "prescription_end_date": "2023-03-30",
            "presscription_status": "valide",
            "commentaire": "Prescription avec patient manquant"
        }
        r = self.client.post(url, payload, format="json")
        self.assertEqual(r.status_code, 400)  
        self.assertIn("medication", r.json())

    def test_prescription_create_invalid_start_date(self):
        """Test pour vérifier que le champ prescription_start_date est obligatoire."""
        url = reverse("prescription-list")
        payload = {
            "patient": self.patient1.id,
            "medication": self.medication1.id,
            "prescription_end_date": "2023-03-30",
            "presscription_status": "valide",
            "commentaire": "Prescription avec patient manquant"
        }
        r = self.client.post(url, payload, format="json")
        self.assertEqual(r.status_code, 400)  
        self.assertIn("prescription_start_date", r.json())

    def test_prescription_create_invalid_end_date(self):
        """Test pour vérifier que le champ prescription_end_date est obligatoire."""
        url = reverse("prescription-list")
        payload = {
            "patient": self.patient1.id,
            "medication": self.medication1.id,
            "prescription_start_date": "2023-03-10",
            "presscription_status": "valide",
            "commentaire": "Prescription avec patient manquant"
        }
        r = self.client.post(url, payload, format="json")
        self.assertEqual(r.status_code, 400)  
        self.assertIn("prescription_end_date", r.json())

    def test_prescription_create_invalid_dates(self):
        """Test pour vérifier qu'une prescription avec des dates invalides ne peut pas être créée."""
        url = reverse("prescription-list")
        payload = {
            "patient": self.patient1.id,
            "medication": self.medication1.id,
            "prescription_start_date": "2023-03-10",
            "prescription_end_date": "2023-03-01",
            "presscription_status": "valide",
            "commentaire": "Prescription avec dates invalides"
        }
        r = self.client.post(url, payload, format="json")
        self.assertEqual(r.status_code, 400)  
        self.assertIn("prescription_end_date", r.json()) 

    def test_prescription_create_commentaire_not_required(self):
        """Test pour vérifier qu'une prescription peut être crée sans commentaire."""
        url = reverse("prescription-list")
        payload = {
            "patient": self.patient1.id,
            "medication": self.medication1.id,
            "prescription_start_date": "2023-03-10",
            "prescription_end_date": "2023-05-01",
            "presscription_status": "valide",
        }
        r = self.client.post(url, payload, format="json")
        self.assertEqual(r.status_code, 201)  