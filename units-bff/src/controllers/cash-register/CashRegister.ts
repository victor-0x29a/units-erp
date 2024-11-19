import { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import { Builder } from "../Builder";
import { SignatureManager } from "../../external";
import { protectByEmployeeRole } from "../../middlewares";
import { MountErrorResponse, ValidatorCompiler } from "../../utils";
import { CashRegisterService } from "../../services/cash-register/cash-register.service";
import { CashRegisterClock } from "../../entity";
import { hitClockSchema } from "./schemas";
import { FastifyError } from "../../exceptions/FastifyError";

class CashRegister {
  service: CashRegisterService;
  signatureManager: SignatureManager;

  constructor(private readonly fastify: FastifyInstance) {
    this.service = new CashRegisterService(CashRegisterClock);
    this.signatureManager = new SignatureManager();

    const ControllerConstructor = new Builder(fastify);

    ControllerConstructor.createRoute("post")("/", {
      handler: this.createRegister,
      validatorCompiler: ValidatorCompiler,
      onRequest: [protectByEmployeeRole(["OPERATOR"], this.signatureManager)],
    });

    ControllerConstructor.createRoute("post")("/hit-clock/:clockRegisterId", {
      handler: this.hitClock,
      validatorCompiler: ValidatorCompiler,
      onRequest: [protectByEmployeeRole(["OPERATOR"], this.signatureManager)],
      schema: {
        params: hitClockSchema,
      },
    });
  }
  private createRegister = async (request: FastifyRequest, reply: FastifyReply) => {
    const {
      employeeDocument
    } = this
      .signatureManager
      .decode(request.headers.authorization);

    return this.service
      .createClockRegister(employeeDocument)
      .then((model) => {
        const modelData = model.toJSON();
        return reply
          .status(201)
          .send({
            cashRegisterId: modelData.id,
          });
      })
      .catch((error: FastifyError) => {
        return reply
          .status(error.statusCode)
          .send(
            MountErrorResponse(error.code, error.message, error.errors)
          );
      });
  };
  private hitClock = async (request: FastifyRequest, reply: FastifyReply) => {
    const { clockRegisterId } = request.params as {
      clockRegisterId: string;
    };

    return this.service
      .toggleClock(Number(clockRegisterId))
      .then(() => reply.status(204).send())
      .catch((error: FastifyError) => {
        return reply
          .status(error.statusCode)
          .send(
            MountErrorResponse(error.code, error.message, error.errors)
          );
      });
  };
}

export { CashRegister };
