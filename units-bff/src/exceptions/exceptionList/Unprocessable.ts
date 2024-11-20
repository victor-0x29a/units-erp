import { FastifyError } from "../FastifyError";

class Unprocessable extends FastifyError {
  constructor(errors = ["Unprocessable"]) {
    super(1010, errors, 422, "Unprocessable");
  }
}

export { Unprocessable };
