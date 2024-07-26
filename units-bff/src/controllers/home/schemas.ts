import { string, object } from "yup";

export const sayHelloSchema = object({
  name: string()
    .required("O nome é obrigatório")
    .typeError("O nome é obrigatório")
    .max(25, "Nome muito longo")
    .min(1, "Nome muito curto"),
}).nonNullable("Existem campos obrigatórios não preenchidos");
