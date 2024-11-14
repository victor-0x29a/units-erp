import { FastifyError } from "../FastifyError";

class MissingDoc extends FastifyError {
  constructor(errors = ["Missing doc"]) {
    super(1003, errors, 404, "Missing doc");
  }
}

export { MissingDoc };
