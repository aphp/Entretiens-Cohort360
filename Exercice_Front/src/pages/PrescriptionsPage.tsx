import { useState } from "react"
import { useQueryClient } from '@tanstack/react-query'
import { useMutation } from "@tanstack/react-query"
import { Button } from "@mui/material"
import { PrescriptionForm } from "../components/PrescriptionForm"
import { usePrescriptions } from "../hooks/usePrescriptions"
import { PrescriptionTable } from "../components/PrescriptionTable"
import { Box, Typography } from "@mui/material"
import { deletePrescription } from "../api/prescription.service"

export const PrescriptionsPage = () => {
  const { data = [], isLoading, isError } = usePrescriptions()
  const [open, setOpen] = useState(false)
  const queryClient = useQueryClient()
  const [selected, setSelected] = useState<Prescription | null>(null)

  const deleteMutation = useMutation({
    mutationFn: deletePrescription,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["prescriptions"] })
    },
  })
  
  const handleDelete = (row: Prescription) => {
    if (confirm("Are you sure?")) {
      deleteMutation.mutate(row.id)
    }
  }
  
  const handleEdit = (row: Prescription) => {
    setSelected(row)
    setOpen(true)
  }
  if (isError) return <p>Error loading prescriptions.</p>

  return (
    <Box sx={{ padding: 4 }}>
      <Typography variant="h4" gutterBottom>
        Prescriptions
      </Typography>
      <Button sx={{ m: 2 }} variant="contained" onClick={() => setOpen(true)}>
        Add Prescription
      </Button>
      <PrescriptionForm
        open={open}
        onClose={() => {
          setOpen(false)
          setSelected(null)
        }}
        selectedPrescription={selected}
      />
      <PrescriptionTable 
        isLoading={isLoading}
        onEdit={handleEdit}
        onDelete={handleDelete}data={data} 
        isLoading={isLoading} />
    </Box>
  )
}