import { useMemo } from "react"
import { MaterialReactTable } from "material-react-table"
import type { MRT_ColumnDef } from "material-react-table"
import type { Prescription } from "../types/prescription"
import { Button, Box } from "@mui/material"
import { jsPDF } from "jspdf"
import autoTable from "jspdf-autotable"
import { mkConfig, generateCsv, download } from "export-to-csv"

interface Props {
  data: Prescription[]
  isLoading: boolean
  onEdit: (row: Prescription) => void
  onDelete: (row: Prescription) => void
}

export const PrescriptionTable = ({
  data,
  isLoading,
  onEdit,
  onDelete,
}: Props) => {
  const columns = useMemo<MRT_ColumnDef<Prescription>[]>(
    () => [
      { accessorKey: "id", header: "ID" },
      { accessorKey: "patient_name", header: "Patient" },
      { accessorKey: "medication_label", header: "Medication" },
      { accessorKey: "dosage", header: "Dosage" },
      { accessorKey: "start_date", header: "Start Date" },
      { accessorKey: "end_date", header: "End Date" },
      { accessorKey: "status", header: "Status" },
    ],
    []
  )

  const handleExportCSV = () => {
    const csvConfig = mkConfig({ useKeysAsHeaders: true })
    const csv = generateCsv(csvConfig)(data)
    download(csvConfig)(csv)
  }

  const handleExportPDF = () => {
    const doc = new jsPDF()
    autoTable(doc, {
      head: [columns.map((c) => c.header as string)],
      body: data.map((row) => [
        row.id,
        row.patient_name,
        row.medication_label,
        row.dosage,
        row.start_date,
        row.end_date ?? "-",
        row.status,
      ]),
    })
    doc.save("prescriptions.pdf")
  }

  return (
    <MaterialReactTable
      columns={columns}
      data={data}
      state={{ isLoading }}
      enableRowActions
      renderRowActions={({ row }) => (
        <Box sx={{ display: "flex", gap: 1 }}>
          <Button
            size="small"
            onClick={() => onEdit(row.original)}
          >
            Edit
          </Button>
          <Button
            size="small"
            color="error"
            onClick={() => onDelete(row.original)}
          >
            Delete
          </Button>
        </Box>
      )}
      renderTopToolbarCustomActions={() => (
        <Box sx={{ display: "flex", gap: 2 }}>
          <Button onClick={handleExportCSV}>
            Export CSV
          </Button>
          <Button onClick={handleExportPDF}>
            Export PDF
          </Button>
        </Box>
      )}
    />
  )
}