import { number, object } from "yup";

export const hitClockSchema = object({
  clockRegisterId: number().typeError("Clock register must be a number").required("Clock register is required"),
});
