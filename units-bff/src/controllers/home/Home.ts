import { FastifyInstance, FastifyRequest } from "fastify";
import { Builder } from "../Builder";
import { ValidatorCompiler } from "../../utils";
import { sayHelloSchema } from "./schemas";
import { SayHelloDTO } from "./dto";

class Home {
  constructor(private readonly fastify: FastifyInstance) {
    const ControllerConstructor = new Builder(fastify);

    ControllerConstructor.createRoute("get")("", {
      handler: this.get,
    });

    ControllerConstructor.createRoute("post")("", {
      schema: {
        body: sayHelloSchema,
      },
      handler: this.postSayHello,
      validatorCompiler: ValidatorCompiler,
    });
  }

  private get = async (_request, reply) => {
    reply.send("Welcome to Units-BFF!");
  };

  private postSayHello = (request: FastifyRequest, reply) => {
    const { name } = request.body as SayHelloDTO;
    reply.send(`Hello ${name}!`);
  };
}

export { Home };
