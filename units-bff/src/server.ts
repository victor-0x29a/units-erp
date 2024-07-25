import Fastify from "fastify";

class Server {
  constructor(
    private readonly port: number,
    private readonly canLog: boolean = true
  ) {}

  private readonly fastify = Fastify({
    logger: this.canLog,
  });

  public start = (): void => {
    this.fastify.listen({
      port: this.port,
    });
  };
}

export { Server };
