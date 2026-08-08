export type Patient = {
    id: number;
    last_name: string;
    first_name: string;
    birth_date?: string
};

export type Medication = {
    id: number;
    code: string;
    label: string;
    status: 'actif' | 'suppr'
};

export type Prescription = {
    id: number;
    patient_id: number;
    medication_id: number;
    comment?: string;
    begin_date: string
    end_date: string
    status: 'valide' | 'en_attente' | 'suppr'
};