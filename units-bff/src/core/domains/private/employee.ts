import { createService } from "../../service";
import { EmployeeLoginPayloadRequest } from '../../types/domains/private/Employee';


const EmployeeService = createService('/v1/employee');

const login = (employeeLoginPayload: EmployeeLoginPayloadRequest): Promise<string> =>  EmployeeService.post('/login', employeeLoginPayload)
  .then((request) => request.headers.authorization);

export {
  login
};
