import { useEffect } from "react"
import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
} from "@mui/material"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation, useQueryClient, useQuery } from "@tanstack/react-query"

import {
  createPrescription,
  updatePrescription,
} from "../api/prescription.service"
import { fetchPatients } from "../api/patient.service"
import { fetchMedications } from "../api/medication.service"
import type { Prescription } from "../types/prescription"

const schema = z.object({
  patient: z.number(),
  medication: z.number(),
  dosage: z.string().min(1),
  start_date: z.string(),
  end_date: z.string().optional(),
  status: z.enum(["active", "completed", "cancelled"]),
})

type FormValues = z.infer<typeof schema>

interface Props {
  open: boolean
  onClose: () => void
  selectedPrescription?: Prescription | null
}

export const PrescriptionForm = ({
  open,
  onClose,
  selectedPrescription,
}: Props) => {
  const queryClient = useQueryClient()

  const { data: patients = [] } = useQuery({
    queryKey: ["patients"],
    queryFn: fetchPatients,
  })

  const { data: medications = [] } = useQuery({
    queryKey: ["medications"],
    queryFn: fetchMedications,
  })

  const mutation = useMutation({
    mutationFn: (data: FormValues) => {
      if (selectedPrescription) {
        return updatePrescription(selectedPrescription.id, data)
      }
      return createPrescription(data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["prescriptions"] })
      onClose()
    },
  })

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      patient: selectedPrescription?.patient ?? undefined,
      medication: selectedPrescription?.medication ?? undefined,
      dosage: selectedPrescription?.dosage ?? "",
      start_date: selectedPrescription?.start_date ?? "",
      end_date: selectedPrescription?.end_date ?? "",
      status: selectedPrescription?.status ?? "active",
    },
  })

  useEffect(() => {
    if (open) {
      reset({
        patient: selectedPrescription?.patient ?? undefined,
        medication: selectedPrescription?.medication ?? undefined,
        dosage: selectedPrescription?.dosage ?? "",
        start_date: selectedPrescription?.start_date ?? "",
        end_date: selectedPrescription?.end_date ?? "",
        status: selectedPrescription?.status ?? "active",
      })
    }
  }, [open, selectedPrescription, reset])

  const onSubmit = (data: FormValues) => {
    mutation.mutate({
      ...data,
      end_date: data.end_date || null,
    })
  }

  return (
    <Dialog open={open} onClose={onClose} fullWidth>
      <DialogTitle>
        {selectedPrescription ? "Edit Prescription" : "Add Prescription"}
      </DialogTitle>

      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogContent>
          <TextField
            select
            fullWidth
            label="Patient"
            margin="normal"
            {...register("patient", { valueAsNumber: true })}
            error={!!errors.patient}
          >
            {patients.map((p) => (
              <MenuItem key={p.id} value={p.id}>
                {p.last_name} {p.first_name}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            select
            fullWidth
            label="Medication"
            margin="normal"
            {...register("medication", { valueAsNumber: true })}
            error={!!errors.medication}
          >
            {medications.map((m) => (
              <MenuItem key={m.id} value={m.id}>
                {m.label}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            fullWidth
            label="Dosage"
            margin="normal"
            {...register("dosage")}
            error={!!errors.dosage}
          />

          <TextField
            fullWidth
            type="date"
            margin="normal"
            {...register("start_date")}
            InputLabelProps={{ shrink: true }}
          />

          <TextField
            fullWidth
            type="date"
            margin="normal"
            {...register("end_date")}
            InputLabelProps={{ shrink: true }}
          />

          <TextField
            select
            fullWidth
            label="Status"
            margin="normal"
            {...register("status")}
          >
            <MenuItem value="active">Active</MenuItem>
            <MenuItem value="completed">Completed</MenuItem>
            <MenuItem value="cancelled">Cancelled</MenuItem>
          </TextField>
        </DialogContent>

        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button
            type="submit"
            variant="contained"
            disabled={mutation.isPending}
          >
            {selectedPrescription ? "Update" : "Save"}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  )
}