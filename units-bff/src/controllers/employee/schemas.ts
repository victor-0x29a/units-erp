import { string, object } from "yup";
import { cpfIsValid } from 'multiform-validator';

export const employeePasswordValidation = string()
  .min(6, 'Password must have at least 6 characters')
  .max(32, 'Password must have at most 32 characters')
  .required('Password is required');

export const employeeLoginSchema = object({
  document: string().nullable().test('document-is-valid', 'Document must be a valid CPF', function (value) {
    if (!value) return true;
    return cpfIsValid(value).isValid;
  }),
  username: string().nullable(),
  password: string().nullable().test('password-at-least-6', 'Password must have at least 6 characters', function (value) {
    if (!value) return true;

    return value.length >= 6;
  }),
}).test('have-at-least-one', 'You must provide at least one of the fields: document, username', function (value) {
  const { document, username } = value;
  return Boolean(document || username);
});

export const employeeFillPasswordSchema = object({
  password: employeePasswordValidation
}).required("Payload is required");
