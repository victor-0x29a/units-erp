import { FastifyInstance } from "fastify";
import type { FastifyHandler } from "./controllers";

class Builder {
  constructor(private readonly fastify: FastifyInstance) {}

  public createRoute =
    (method: string) => (path: string, handler: FastifyHandler) => {
      return this.fastify[method](path, handler);
    };
}

export { Builder };
