import { FastifyError } from "../FastifyError";

class RetroactiveAction extends FastifyError {
  constructor(errors = ["Retroactive action"]) {
    super(1004, errors, 423, "Retroactive action");
  }
}

export { RetroactiveAction };
