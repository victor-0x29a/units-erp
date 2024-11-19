import { FastifyError } from "../FastifyError";

class Conflict extends FastifyError {
  constructor(errors = ["Conflict error"]) {
    super(1006, errors, 422, "Conflict error");
  }
}

export { Conflict };
