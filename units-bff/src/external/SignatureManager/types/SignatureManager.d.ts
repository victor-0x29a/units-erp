export type SignPayload = {
    storeUnit: number;
    isTemporary: boolean;
    employeeDocument: string;
    employeeRole: string;
}

export type DecodedToken = {
    iat: number;
    exp: number;
    is_temporary: boolean;
    employee_document: string;
    employee_role: string;
    store_unit: number;
}

export type ParsedDecodedToken = {
    iat: number;
    exp: number;
    isTemporary: boolean;
    employeeDocument: string;
    employeeRole: string;
    storeUnit: number;
}
