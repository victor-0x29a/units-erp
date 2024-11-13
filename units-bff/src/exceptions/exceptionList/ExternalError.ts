import { ErrorResponse } from "../../core/types/global/response";
import { FastifyError } from "../FastifyError";

class ExternalError extends FastifyError {
  constructor(details?: ErrorResponse) {
    super(1002, ["External error"], 503, "External error", details);
  }
}

export { ExternalError };
