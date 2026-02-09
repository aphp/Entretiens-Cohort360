import type { Medication, Patient } from "./types";

export const medicationStatuses = { "actif": "🟢", "suppr": "🔴" };
export const prescriptionStatuses = { "valide": "🟢", "en_attente": "🟡", "suppr": "🔴" }

export function buildPatientLabel(patient: Patient): string {
    if (!patient) {
        return "";
    }
    const dob = Date.parse(patient.birth_date as string);
    const ageInMs = new Date().getTime() - dob;
    const age = Math.floor(ageInMs / 1000 / 60 / 60 / 24 / 365.25);
    return `${patient.first_name} ${patient.last_name} ${age} ans`
}

export function buildMedicationLabel(medication: Medication): string {
    if (!medication) {
        return "";
    }
    return `${medicationStatuses[medication.status]} ${medication.label}`
}