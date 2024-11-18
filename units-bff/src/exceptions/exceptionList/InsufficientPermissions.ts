import { FastifyError } from "../FastifyError";

class InsufficientPermissions extends FastifyError {
  constructor(errors = ["Insufficient permissions"], details?: unknown) {
    super(1009, errors, 403, "Insufficient permissions", details);
  }
}

export { InsufficientPermissions };
