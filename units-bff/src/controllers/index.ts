import { Home } from "./home";
import { Employee } from "./employee";
import { CashRegister } from "./cash-register/CashRegister";

const controllers = [
  [Home, "/"],
  [Employee, "/v1/employee"],
  [CashRegister, "/v1/cash-register"],
] as const;

export default controllers;
