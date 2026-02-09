import { medicationStatuses } from "~/ui";
import type { Route } from "./+types/home";

import { medicationContext } from "~/context";


export async function clientLoader({ context }: Route.ClientLoaderArgs) {
  const medicationMap = await context.get(medicationContext);

  const medicationList = [];
  for (const m of (medicationMap?.values()) || []) {
    medicationList.push({
      "id": m.id,
      "code": m.code,
      "label": m.label,
      "status_as_emoji": medicationStatuses[m.status],

    });
  }
  return { medicationList }
}


export default function MedicationList({ loaderData }: Route.ComponentProps) {

  const { medicationList } = loaderData;
  return (
    <>
      <h1>Les médicaments</h1>
      {!loaderData && <div>Loading...</div>}
      {loaderData && <table>
        <thead>
          <tr>
            <th>id</th>
            <th>Code</th>
            <th>&Eacute;tat</th>
            <th>Nom</th>
          </tr>
        </thead>
        <tbody>
          {medicationList.map(p => {
            return (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{p.code}</td>
                <td>{p.status_as_emoji}</td>
                <td>{p.label}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
      }
    </>
  );
}

