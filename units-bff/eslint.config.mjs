import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";


export default [
   {
    rules: {
      "no-unused-vars": "error",
      "semi": ["error", "always"]
    },
    files: ["**/*.{js,mjs,cjs,ts}"]
   },
   pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
];
