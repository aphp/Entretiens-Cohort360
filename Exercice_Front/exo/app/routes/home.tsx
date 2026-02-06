import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Cohort360" },
    { name: "description", content: "Welcome to Cohort 360 demo app!" },
  ];
}

export default function Home() {
  return <Welcome />;
}
