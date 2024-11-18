import { FastifyRequest, FastifyReply, DoneFuncWithErrOrRes } from "fastify";
import { InvalidAuthorization, ExpiredAuthorization, InternalError, InsufficientPermissions } from "../exceptions";
import { Roles } from "../types/employee";
import { SignatureManager } from "../external";

export const protectByEmployeeRole = (
  requiredPermissions: Roles[],
  signatureManager: SignatureManager
) => {
  return async (request: FastifyRequest, _reply: FastifyReply, done: DoneFuncWithErrOrRes) => {
    const { authorization: authorizationToken } = request.headers;

    if (!authorizationToken) {
      throw new InvalidAuthorization();
    }

    return signatureManager.checkIsValid(authorizationToken)
      .then(() => {
        const decodedToken = signatureManager.decode(authorizationToken);

        const isAdmin = decodedToken.employeeRole === "ADMIN";

        if (isAdmin) {
          return done();
        }

        if (!requiredPermissions.includes(decodedToken.employeeRole)) {
          throw new InsufficientPermissions(requiredPermissions);
        }

        return done();
      })
      .catch((error: InternalError | InvalidAuthorization | ExpiredAuthorization) => {
        throw error;
      });
  };
};
