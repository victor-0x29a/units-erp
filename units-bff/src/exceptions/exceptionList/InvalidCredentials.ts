import { FastifyError } from "../FastifyError";

class InvalidCredentials extends FastifyError {
  constructor(errors = ["Invalid credentials"]) {
    super(1001, errors, 401, "Invalid credentials");
  }
}

export { InvalidCredentials };
