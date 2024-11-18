import { FastifyError } from "../FastifyError";

class ExpiredAuthorization extends FastifyError {
  constructor(errors = ["Expired authorization"], details?: unknown) {
    super(1007, errors, 401, "Expired Authorization", details);
  }
}

export { ExpiredAuthorization };
