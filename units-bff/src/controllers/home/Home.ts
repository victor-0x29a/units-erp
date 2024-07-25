import { FastifyInstance } from "fastify";
import { Builder } from "../Builder";

class Home {
  constructor(private readonly fastify: FastifyInstance) {
    const Builtin = new Builder(fastify);
    Builtin.createRoute("get")("/", this.get);
  }

  private get = async (_request, reply) => {
    reply.send("Welcome to Units-BFF!");
  };
}

export { Home };
