import { createService } from "../../service";
import { EmployeeLoginPayloadRequest } from '../../types/domains/private/Employee';


const EmployeeService = createService('/v1/employee');

const login = (employeeLoginPayload: EmployeeLoginPayloadRequest) => {
  return EmployeeService.post('/login', employeeLoginPayload);
};

export {
  login
};
