import { useQuery } from "@tanstack/react-query"
import { fetchPrescriptions } from "../api/prescription.service"
import type { PrescriptionFilters } from "../api/prescription.service"

export const usePrescriptions = (filters?: PrescriptionFilters) => {
  return useQuery({
    queryKey: ["prescriptions", filters],
    queryFn: () => fetchPrescriptions(filters),
  })
}