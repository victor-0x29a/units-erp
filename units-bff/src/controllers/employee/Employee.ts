import { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import { EmployeeService } from "../../services";
import { Builder } from "../Builder";
import { mountErrorResponse, ValidatorCompiler } from "../../utils";
import { employeeFillPasswordSchema, employeeLoginSchema } from "./schemas";
import type { EmployeeLoginPayloadRequest } from "../../interfaces/employee";
import { FastifyError } from "../../exceptions/FastifyError";
import { SignatureManager } from "../../external";

class Employee {
  service: EmployeeService;

  constructor(private readonly fastify: FastifyInstance) {
    this.service = new EmployeeService(new SignatureManager());
    const ControllerConstructor = new Builder(fastify);

    ControllerConstructor.createRoute("post")("/login", {
      schema: {
        body: employeeLoginSchema,
      },
      handler: this.employeeLogin,
      validatorCompiler: ValidatorCompiler,
    });

    ControllerConstructor.createRoute("put")("/fill-password", {
      schema: {
        body: employeeFillPasswordSchema,
      },
      handler: this.fillEmployeePassword,
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
        return reply.status(error.statusCode).send(mountErrorResponse(error));
      });
  };
  private fillEmployeePassword = async (request: FastifyRequest, reply: FastifyReply) => {
    const { authorization } = request.headers;
    const fillPwdPayload = request.body as EmployeeLoginPayloadRequest;

    return this.service.fillPassword(authorization, fillPwdPayload)
      .then(() => reply.status(204).send())
      .catch((error: FastifyError) => reply.status(error.statusCode).send(mountErrorResponse(error)));
  };
}

export { Employee };
