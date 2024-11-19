import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";


export default [
  {
    rules: {
      "@typescript-eslint/no-unused-vars": ["error", { "varsIgnorePattern": "^_", "argsIgnorePattern": "^_" }],
      "semi": ["error", "always"],
      "indent": [1, 2],
    },
    files: ["**/*.{js,mjs,cjs,ts}"]
  },
  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
];
