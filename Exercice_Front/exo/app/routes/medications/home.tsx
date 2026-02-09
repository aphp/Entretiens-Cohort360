import type { Route } from "./+types/home";

import { medicationContext } from "~/context";

export async function clientLoader({ context }: Route.ClientLoaderArgs) {
  return await context.get(medicationContext);
}


export default function MedicationList({ loaderData }: Route.ComponentProps) {

  return (
    <main >
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
          {[...loaderData.values()].map(p => {
            return (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{p.code}</td>
                <td>{p.status}</td>
                <td>{p.label}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
      }
    </main>
  );
}

