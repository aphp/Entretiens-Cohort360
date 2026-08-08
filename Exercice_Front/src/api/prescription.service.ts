import { api } from "./axios"
import type { Prescription } from "../types/prescription"

export interface PrescriptionFilters {
  patient?: number
  medication?: number
  status?: string
  start_date_gte?: string
  start_date_lte?: string
  end_date_gte?: string
  end_date_lte?: string
}

export const fetchPrescriptions = async (
  filters?: PrescriptionFilters
): Promise<Prescription[]> => {
  const { data } = await api.get<Prescription[]>("/Prescription", {
    params: filters,
  })
  return data
}

export const createPrescription = async (
  payload: Omit<Prescription, "id">
): Promise<Prescription> => {
  const { data } = await api.post<Prescription>("/Prescription", payload)
  return data
}

export const updatePrescription = async (
  id: number,
  payload: any
) => {
  const { data } = await api.put(`/Prescription/${id}`, payload)
  return data
}

export const deletePrescription = async (id: number) => {
  await api.delete(`/Prescription/${id}`)
}