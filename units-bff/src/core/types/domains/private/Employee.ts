export interface EmployeeLoginPayloadRequest {
    username?: string;
    document?: string;
    password?: string;
}

export interface EmployeeFillPwdPayloadRequest {
    password: string;
}
