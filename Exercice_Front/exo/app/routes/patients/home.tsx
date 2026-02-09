import type { Route } from "./+types/home";
import { patientContext } from "~/context";

export async function clientLoader({ context }: Route.ClientLoaderArgs) {
  return await context.get(patientContext);
}

export default function PatientList({ loaderData }: Route.ComponentProps) {

  return (
    <main >
      <h1>Les patients</h1>
      {!loaderData && <div>Loading...</div>}
      {loaderData && <table>
        <thead>
          <tr>
            <th>id</th>
            <th>Prénom</th>
            <th>Nom</th>
            <th>Date de naissance</th>
          </tr>
        </thead>
        <tbody>
          {[...loaderData.values()].map(p => {
            return (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{p.first_name}</td>
                <td>{p.last_name}</td>
                <td>{p.birth_date}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
      }
    </main>
  );
}

