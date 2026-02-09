import type { Route } from "./+types/home";
import { useSearchParams } from "react-router";
import { patientContext, medicationContext } from "~/context";
import type { Medication, Patient } from "~/types";
import { fetchPrescriptionList } from "~/backend";
import { buildMedicationLabel, buildPatientLabel, medicationStatuses, prescriptionStatuses } from "~/ui";

// export async function action({ request }: Route.ActionArgs) {
//   const formData = await request.formData();
//   console.debug("in action", "formData", formData);
//   return { ok: true };
// }

function extractExistingParams(searchParams: URLSearchParams) {
  // TODO à simplifier
  const entries = Array.from(searchParams.entries());
  return entries.reduce((acc, a) => ((acc[a[0]] = acc[a[0]] || []).push(a[1]), acc), {});
}


export async function clientLoader({ request, context }: Route.LoaderArgs) {
  const parameters = new URL(request.url).searchParams;
  const filter = extractExistingParams(parameters);
  console.debug("clientLoader", "filter", filter)

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
  return { prescriptionList }
}

export default function PrescriptionList({
  loaderData,
  actionData,
  params,
  matches,
}: Route.ComponentProps) {

  // console.debug("in home", "actionData", actionData);
  // console.debug("in home", "params", params);

  const { prescriptionList } = loaderData;
  const [searchParams, setSearchParams] = useSearchParams()
  const filterStatus = searchParams.get("status") || "";
  const filterPatientLastName = searchParams.get("patient_lastname") || "";
  const filterMedicationLabel = searchParams.get("medication_label") || "";

  // useEffect(() => {
  //   console.debug("in searchP effect", "searchParams", searchParams);
  // }, [searchParams])

  const onFilter = (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    console.debug("onFilter", "formData", formData);

    const newParams = {
      status: formData.get("status") || "",
      medication_label: formData.get("medication_label") || "",
      patient_lastname: formData.get("patient_lastname") || ""
    };
    setSearchParams(newParams);

    console.debug("onFilter", "newParams", newParams);
    console.debug("onFilter", "push history", searchParams.toString());
    history.pushState({}, "", searchParams.toString());
  }

  return (
    <>
      <h1>Les prescriptions</h1>
      <div>
        <form onSubmit={onFilter}>
          <fieldset>
            <legend>Filtrage</legend>
            <label>Par nom de patient
              <input type="text" name="patient_lastname" defaultValue={filterPatientLastName} />
            </label>
            <label>Par médicament
              <input type="text" name="medication_label" defaultValue={filterMedicationLabel} />
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
      </div>
      {/* <Form method="post" navigate={false}>
        <input type="text" name="q" />
        <button type="submit">Filter</button>
      </Form> */}
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

