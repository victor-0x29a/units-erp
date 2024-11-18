import { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import { Builder } from "../Builder";
import { protectByEmployeeRole } from "../../middlewares";
import { MountErrorResponse, ValidatorCompiler } from "../../utils";
import { CashRegisterService } from "../../services/cash-register/cash-register.service";
import { CashRegisterClock } from "../../entity";
import { SignatureManager } from "../../external";
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
  }
  private createRegister = async (request: FastifyRequest, reply: FastifyReply) => {
    const {
      employeeDocument
    } = this
      .signatureManager
      .decode(request.headers.authorization);

    return this.service
      .createClockRegister(employeeDocument)
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
