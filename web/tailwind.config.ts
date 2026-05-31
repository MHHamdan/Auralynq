import type { Config } from "tailwindcss";
const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0b1020",
        panel: "#11182b",
        edge: "#1f2a44",
        brand: "#5eead4",
        brand2: "#818cf8",
      },
    },
  },
  plugins: [],
};
export default config;
