import { type RouteConfig, index, prefix, route , layout } from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    ...prefix("patients", [
        index("./routes/patients/home.tsx"),
        layout("./routes/patients/layout.tsx", [
            route(":pid", "./routes/patients/display.tsx")]),
    ]),
    ...prefix("medications", [
        index("./routes/medications/home.tsx"),
        layout("./routes/medications/layout.tsx", [
            route(":pid", "./routes/medications/display.tsx")]),
    ]),
    ...prefix("prescriptions", [
        index("./routes/prescriptions/home.tsx"),
        route("search", "./routes/prescriptions/search.tsx"),
        layout("./routes/prescriptions/layout.tsx", [
            route(":pid", "./routes/prescriptions/display.tsx"),
            route(":pid/edit", "./routes/prescriptions/edit.tsx")]),
    ]),

] satisfies RouteConfig;
