export type CashRegisterClock = {
    id?: number;
    employee_document: string;
    clock_in: Date;
    clock_out: Date | null;
    clock_lunch_out: Date | null;
    clock_lunch_in: Date | null;
}
