
export async function loader({ request }) {
//   await new Promise((res) => setTimeout(res, 300));
//   let url = new URL(request.url);
//   let query = url.searchParams.get("q");
//   return users.filter((user) =>
//     user.name.toLowerCase().includes(query.toLowerCase()),
//   );
    const res = await fetch(`http://localhost:8000/Prescription`);
  const patients = await res.json();
  console.debug("in search", patients);
  return patients;
}