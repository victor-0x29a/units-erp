import { Home } from "./home";
import { Employee } from "./employee";

const controllers = [
  [Home, "/"],
  [Employee, "/v1/employee"]
] as const;

export default controllers;
