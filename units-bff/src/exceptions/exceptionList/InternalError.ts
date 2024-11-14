import { FastifyError } from "../FastifyError";

class InternalError extends FastifyError {
  constructor(details?: unknown) {
    super(1005, ["Internal error"], 500, "Internal error", details);
  }
}

export { InternalError };
