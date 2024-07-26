import { FastifyInstance, RouteShorthandOptionsWithHandler } from "fastify";

class Builder {
  constructor(private readonly fastify: FastifyInstance) {}

  public createRoute =
    (method: string) =>
    (path: string, options: RouteShorthandOptionsWithHandler) => {
      return this.fastify[method](path, options);
    };
}

export { Builder };
