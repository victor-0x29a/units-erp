import { Roles } from "../../../types/employee";

export type SignPayload = {
    storeUnit: number;
    isTemporary: boolean;
    employeeDocument: string;
    employeeRole: Roles;
}

export type DecodedToken = {
    iat: number;
    exp: number;
    is_temporary: boolean;
    employee_document: string;
    employee_role: Roles;
    store_unit: number;
}

export type ParsedDecodedToken = {
    iat: number;
    exp: number;
    isTemporary: boolean;
    employeeDocument: string;
    employeeRole: Roles;
    storeUnit: number;
}
