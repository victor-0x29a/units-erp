import Fastify, { FastifyInstance } from "fastify";
import { Home } from "./controllers";

class Server {
  constructor(
    private readonly port: number,
    private readonly canLog: boolean = true
  ) {}

  private readonly fastify = Fastify({
    logger: this.canLog,
  }) as FastifyInstance;

  public start = (): void => {
    new Home(this.fastify);

    this.fastify.listen({
      port: this.port,
    });
  };
}

export { Server };
