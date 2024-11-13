import { EmployeeLoginPayloadRequest } from "../../interfaces";
import { privateDomains } from "../../core";
import { ExternalError, InvalidCredentials } from "../../exceptions";
import { ErrorResponse } from "../../core/types/global/response";
const { employeeDomain } = privateDomains;


class EmployeeService {
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
}

export { EmployeeService };
