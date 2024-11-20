import { createService } from "../../service";
import { EmployeeLoginPayloadRequest, EmployeeFillPwdPayloadRequest } from '../../types/domains/private/Employee';


const EmployeeService = createService('/v1/employee');

const login = (employeeLoginPayload: EmployeeLoginPayloadRequest): Promise<string> =>  EmployeeService.post('/login', employeeLoginPayload)
  .then((request) => request.headers.authorization);

const fillPassword  = (
  employeeDocument: string,
  employeeFillPwdPayload: EmployeeFillPwdPayloadRequest
): Promise<void> => EmployeeService.put(`/${employeeDocument}/password`, employeeFillPwdPayload);

export {
  login,
  fillPassword
};
