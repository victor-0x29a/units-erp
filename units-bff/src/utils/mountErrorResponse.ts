import { FastifyError } from "../exceptions/FastifyError";

export const mountErrorResponse = (error: FastifyError) => {
  return {
    code: error.code,
    message: error.message,
    errors: error.errors,
    extraData: error.extraData,
  };
};
