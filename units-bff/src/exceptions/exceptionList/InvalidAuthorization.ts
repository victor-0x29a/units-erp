import { FastifyError } from "../FastifyError";

class InvalidAuthorization extends FastifyError {
  constructor(errors = ["Invalid authorization"], details?: unknown) {
    super(1008, errors, 401, "Invalid authorization", details);
  }
}

export { InvalidAuthorization };
