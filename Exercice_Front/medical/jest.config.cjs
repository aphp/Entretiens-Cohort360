/** @type {import('jest').Config} */
module.exports = {
    testEnvironment: "jest-environment-jsdom", // Assurez-vous que le module est correctement référencé
    transform: {
        "^.+\\.tsx?$": "ts-jest",
    },
    moduleNameMapper: {
        "\\.(css|less|scss|sass)$": "identity-obj-proxy", // Ignore les imports CSS
    },
    setupFilesAfterEnv: ["<rootDir>/src/setupTests.ts"], // Fichier de configuration pour Jest
    testMatch: ["**/__tests__/**/*.+(ts|tsx|js)", "**/?(*.)+(spec|test).+(ts|tsx|js)"],
};