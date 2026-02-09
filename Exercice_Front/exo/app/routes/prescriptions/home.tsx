import type { Route } from "./+types/home";
import { useSearchParams } from "react-router";
import { patientContext, medicationContext } from "~/context";
import { createPrescription, fetchPrescriptionList } from "~/backend";
import { buildMedicationLabel, buildPatientLabel, prescriptionStatuses } from "~/ui";
import { useState } from "react";


function extractExistingParams(searchParams: URLSearchParams) {
  // TODO à simplifier
  const entries = Array.from(searchParams.entries());
  return entries.reduce((acc, a) => ((acc[a[0]] = acc[a[0]] || []).push(a[1]), acc), {});
}


export async function clientLoader({ request, context }: Route.LoaderArgs) {
  const parameters = new URL(request.url).searchParams;
  const filter = extractExistingParams(parameters);

  const patientMap = await context.get(patientContext);
  const medicationMap = await context.get(medicationContext);
  const rawPrescriptionList = await fetchPrescriptionList(filter);

  const prescriptionList = rawPrescriptionList.map(pr => {
    const patientLabel = buildPatientLabel(patientMap.get(pr.patient));
    const medicationLabel = buildMedicationLabel(medicationMap.get(pr.medication));
    return {
      "id": pr.id,
      "patient": patientLabel,
      "medication": medicationLabel,
      "begin_date": pr.begin_date,
      "end_date": pr.end_date,
      "status": pr.status,
      "comment": pr.comment
    }
  });

  const medicationCodeOptions = [];
  const medicationLabelOptions = [];
  for (const m of (medicationMap?.values() || [])) {
    medicationCodeOptions.push([m.id, m.code])
    medicationLabelOptions.push([m.id, m.label])
  }

  const patientOptions = [];
  for (const p of (patientMap?.values() || [])) {
    patientOptions.push([p.id, buildPatientLabel(p)])
  }


  return { prescriptionList, medicationCodeOptions, medicationLabelOptions, patientOptions }
}

export default function PrescriptionList({
  loaderData,
  actionData,
  params,
  matches,
}: Route.ComponentProps) {

  const { prescriptionList, medicationCodeOptions, medicationLabelOptions, patientOptions } = loaderData;
  const [searchParams, setSearchParams] = useSearchParams()
  const filterStatus = searchParams.get("status") || "";
  const filterPatientLastName = searchParams.get("patient_lastname") || "";
  const filterMedicationLabel = searchParams.get("medication_label") || "";
  const filterMedicationId = searchParams.get("medication_id") || "";

  const [afterCreateState, setAfterCreateState] = useState<boolean | null>(null);
  const [afterCreateMessage, setAfterCreateMessage] = useState<string | null>(null);

  const onFilter = (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    setAfterCreateState(null);
    setAfterCreateMessage(null);

    const newParams = {
      status: formData.get("status") || "",
      medication_label: formData.get("medication_label") || "",
      medication_id: formData.get("medication_id") || "",
      patient_lastname: formData.get("patient_lastname") || ""
    };
    setSearchParams(newParams);

    history.pushState({}, "", searchParams.toString());
  }



  const onCreate = (event) => {
    event.preventDefault();
    setAfterCreateState(null);
    setAfterCreateMessage(null);
    const formData = new FormData(event.target);
    createPrescription(formData).then(async (response) => {

      if (response.status === 400) {
        throw await response.json();
      } else if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }
      return await response.json();
    }).then((responseData) => {
      setAfterCreateState(true);
      setAfterCreateMessage(`Prescription créée (id=${responseData.id})`);
    }).catch((rejectionData) => {
      let errorMsg;
      if (Array.isArray(rejectionData)) {
        errorMsg = rejectionData[0];
      } else {
        const parts = [];
        for (const key in rejectionData) {
          for (const msg of rejectionData[key]) {
            parts.push(`${msg} (${key})`)
          }
        }
        errorMsg = parts.join(" ; ");
      }

      setAfterCreateState(false);
      setAfterCreateMessage(`Prescription non créée : ${errorMsg}`);
    })
  }


  return (
    <>
      <h1>Les prescriptions</h1>
      <div className="forms">
        <form onSubmit={onFilter}>
          <fieldset>
            <legend>Filtrage</legend>
            <label>Par nom de patient
              <input type="text" name="patient_lastname" defaultValue={filterPatientLastName} />
            </label>
            <label>Par nom de médicament
              <input type="text" name="medication_label" defaultValue={filterMedicationLabel} />
            </label>
            <label>Par code médicament
              <select name="medication_id" defaultValue={filterMedicationId}>
                <option value="">-</option>
                {medicationCodeOptions
                  .sort((a, b) => a[1].localeCompare(b[1]))
                  .map(([id, code]) => (
                    <option key={id} value={id}>{code}</option>
                  ))}
              </select>
            </label>
            <label>Par état de prescription
              <select name="status" defaultValue={filterStatus}>
                <option value="">-</option>
                <option value="valide">🟢</option>
                <option value="en_attente">🟡</option>
                <option value="suppr">🔴</option>
              </select>
            </label>
            <button>Filtrer</button>
          </fieldset>
        </form>
        <form onSubmit={onCreate}>
          <fieldset>
            <legend>Création</legend>
            <label>Patient
              <select name="patient">
                {patientOptions
                  .sort((a, b) => a[1].localeCompare(b[1]))
                  .map(([id, label]) => (
                    <option key={id} value={id}>{label}</option>
                  ))}
              </select>
            </label>
            <label>Code médicament
              <select name="medication" defaultValue={filterMedicationId}>
                {medicationCodeOptions
                  .sort((a, b) => a[1].localeCompare(b[1]))
                  .map(([id, code]) => (
                    <option key={id} value={id}>{code}</option>
                  ))}
              </select>
            </label>
            <label>Période
              <input type="date" name="begin_date" />
              <input type="date" name="end_date" />
            </label>
            <label>&Eacute;tat
              <select name="status" defaultValue={filterStatus}>
                <option value="valide">🟢</option>
                <option value="en_attente">🟡</option>
                <option value="suppr">🔴</option>
              </select>
            </label>
            <label>Commentaire
              <input type="text" name="comment" placeholder="(optionnel)" />
            </label>
            <button>Créer</button>
            {(afterCreateState !== null) && (
              <span className={afterCreateState ? 'okMessage' : 'errorMessage'}>{afterCreateMessage}</span>
            )}
          </fieldset>
        </form>
      </div>
      <table>
        <thead>
          <tr>
            <th>id</th>
            <th>&Eacute;tat</th>
            <th>Patient</th>
            <th>Médicament</th>
            <th>Début</th>
            <th>Fin</th>
            <th>Commentaire</th>
          </tr>
        </thead>
        <tbody>
          {prescriptionList.map(p => {
            return (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{prescriptionStatuses[p.status]}</td>
                <td>{p.patient}</td>
                <td>{p.medication}</td>
                <td>{p.begin_date}</td>
                <td>{p.end_date}</td>
                <td>{p.comment}</td>
              </tr>
            )
          })}
          {prescriptionList.length === 0 && (
            <tr><td colSpan={7}>Aucun résultat</td></tr>
          )
          }
        </tbody>
      </table>
    </>
  );
}

