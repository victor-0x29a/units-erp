import { Roles } from "../../types/employee";
import { FastifyError } from "../FastifyError";

class InsufficientPermissions extends FastifyError {
  constructor(requiredPermissions: Roles[] = [], errors = ["Insufficient permissions"], details?: unknown) {
    const message = `Required permissions: ${requiredPermissions.join(", ")}`;

    super(1009, errors, 403, message, details);
  }
}

export { InsufficientPermissions };
