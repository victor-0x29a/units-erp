import { privateDomains } from "../../core";
import { ExternalError, InvalidCredentials, Unprocessable } from "../../exceptions";
import { ErrorResponse } from "../../core/types/global/response";
import { EmployeeLoginPayloadRequest, EmployeeFillPwdPayloadRequest } from "../../interfaces";
import { SignatureManager } from "../../external";
const { employeeDomain } = privateDomains;


class EmployeeService {
  constructor(private signatureManager: SignatureManager) {}

  public async login(loginPayload: EmployeeLoginPayloadRequest) {
    return employeeDomain.login(loginPayload)
      .then((employeeToken) => employeeToken)
      .catch((error: ErrorResponse) => {
        if ([404, 401, 422].includes(error.statusCode)) {
          return Promise.reject(new InvalidCredentials());
        }
        return Promise.reject(new ExternalError(error));
      });
  }
  public async fillPassword(
    employeeAuthorizationToken: string,
    fillPwdPayload: EmployeeFillPwdPayloadRequest
  ) {
    const {
      employeeDocument,
      isTemporary
    } = this.signatureManager.decode(employeeAuthorizationToken);

    if (!isTemporary) {
      return Promise.reject(
        new Unprocessable(["You can't change your password."])
      );
    }

    return employeeDomain.fillPassword(employeeDocument, fillPwdPayload)
      .catch((error: ErrorResponse) => Promise.reject(new ExternalError(error)));
  }
}

export { EmployeeService };
