import { type RouteConfig, index, prefix, route, layout } from "@react-router/dev/routes";

export default [
    layout("./routes/layout.tsx", [
    index("routes/home.tsx"),
        ...prefix("patients", [
            index("./routes/patients/home.tsx"),
        ]),
        ...prefix("medications", [
            index("./routes/medications/home.tsx"),
            route(":pid", "./routes/medications/display.tsx")]),
        ...prefix("prescriptions", [
            index("./routes/prescriptions/home.tsx"),
            route(":pid", "./routes/prescriptions/display.tsx"),
            route(":pid/edit", "./routes/prescriptions/edit.tsx")]),
    ]),

] satisfies RouteConfig;
