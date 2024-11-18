import { FastifyInstance/*, FastifyRequest, FastifyReply */ } from "fastify";
// import { Builder } from "../Builder";
// import { protectByEmployeeRole } from "../../middlewares";
// import { ValidatorCompiler } from "../../utils";
import { CashRegisterService } from "../../services/cash-register/cash-register.service";
import { CashRegisterClock } from "../../entity";

class CashRegister {
  service: CashRegisterService;

  constructor(private readonly fastify: FastifyInstance) {
    this.service = new CashRegisterService(CashRegisterClock);

    // const ControllerConstructor = new Builder(fastify);

    // ControllerConstructor.createRoute("post")("/", {
    //   handler: this.createRegister,
    //   validatorCompiler: ValidatorCompiler,
    //   onRequest: [protectByEmployeeRole(["OPERATOR"])],
    // });
  }
  // private createRegister = async (request: FastifyRequest, reply: FastifyReply) => {
  // };
}

export { CashRegister };
