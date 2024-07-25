import Fastify, { FastifyInstance } from "fastify";
import { Home } from "./controllers";

class Server {
  constructor(private readonly canLog: boolean = true) {}

  private readonly fastify = Fastify({
    logger: this.canLog,
  }) as FastifyInstance;

  public start = (): FastifyInstance => {
    new Home(this.fastify);

    return this.fastify;
  };
}

export { Server };
