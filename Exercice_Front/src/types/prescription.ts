export type PrescriptionStatus = "active" | "completed" | "cancelled"

export interface Prescription {
  id: number
  patient: number
  medication: number
  dosage: string
  start_date: string
  end_date?: string | null
  status: PrescriptionStatus
}