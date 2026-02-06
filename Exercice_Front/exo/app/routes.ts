import { type RouteConfig, index, prefix, route , layout } from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    ...prefix("patients", [
        index("./patients/home.tsx"),
        layout("./patients/layout.tsx", [
            route(":pid", "./patients/display.tsx")]),
    ]),
    ...prefix("medications", [
        index("./medications/home.tsx"),
        layout("./medications/layout.tsx", [
            route(":pid", "./medications/display.tsx")]),
    ]),
    ...prefix("prescriptions", [
        index("./prescriptions/home.tsx"),
        layout("./prescriptions/layout.tsx", [
            route(":pid", "./prescriptions/display.tsx"),
            route(":pid/edit", "./prescriptions/edit.tsx")]),
    ]),

] satisfies RouteConfig;
