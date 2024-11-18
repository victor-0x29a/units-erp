import { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import { EmployeeService } from "../../services";
import { Builder } from "../Builder";
import { MountErrorResponse, ValidatorCompiler } from "../../utils";
// import { employeeLoginSchema } from "./schemas";
// import type { EmployeeLoginPayloadRequest } from "../../interfaces/employee";
import { createCashRegisterClockSchema } from "./schemas";
import { FastifyError } from "../../exceptions/FastifyError";

class CashRegister {
  service: EmployeeService;

  constructor(private readonly fastify: FastifyInstance) {
    this.service = new EmployeeService();

    const ControllerConstructor = new Builder(fastify);

    ControllerConstructor.createRoute("post")("/", {
      handler: this.createRegister,
      validatorCompiler: ValidatorCompiler,
    });
  }

  private createRegister = async (request: FastifyRequest, reply: FastifyReply) => {
  };
}

export { CashRegister };
