import { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import { EmployeeService } from "../../services";
import { Builder } from "../Builder";
import { MountErrorResponse, ValidatorCompiler } from "../../utils";
import { employeeLoginSchema } from "./schemas";
import type { EmployeeLoginPayloadRequest } from "../../interfaces/employee";
import { FastifyError } from "../../exceptions/FastifyError";

class Employee {
  service: EmployeeService;

  constructor(private readonly fastify: FastifyInstance) {
    this.service = new EmployeeService();

    const ControllerConstructor = new Builder(fastify);

    ControllerConstructor.createRoute("post")("/login", {
      schema: {
        body: employeeLoginSchema,
      },
      handler: this.employeeLogin,
      validatorCompiler: ValidatorCompiler,
    });
  }

  private employeeLogin = async (request: FastifyRequest, reply: FastifyReply) => {
    const loginPayload = request.body as EmployeeLoginPayloadRequest;

    return this.service.login(loginPayload)
      .then((employeeToken) => {
        return reply
          .status(204)
          .header("Authorization", employeeToken)
          .send();
      })
      .catch((error: FastifyError) => {
        return reply.status(error.statusCode).send(MountErrorResponse(error.code, error.message, error.errors));
      });
  };
}

export { Employee };
