import Fastify, {
  FastifyError,
  FastifyInstance,
  FastifyReply,
  FastifyRequest,
} from "fastify";
import { Home } from "./controllers";

/* c8 ignore start */
class Server {
  constructor(private readonly canLog: boolean = true) {}

  private readonly fastify = Fastify({
    logger: this.canLog,
  }) as FastifyInstance;

  private errorHandler = (
    error: FastifyError & { errors: string[] },
    _request: FastifyRequest,
    reply: FastifyReply
  ) => {
    const errorsList = error?.errors || [];

    const isMultipleErrors = errorsList.length > 1;

    const errorTemplate = {
      code: error.code,
    };

    if (isMultipleErrors) {
      reply.status(400).send({
        ...errorTemplate,
        error: errorsList,
      });
      return;
    }

    reply.status(error.statusCode || 500).send({
      ...errorTemplate,
      error: errorsList[0] || error.message,
    });

    return;
  };

  public start = (): FastifyInstance => {
    new Home(this.fastify);

    this.fastify.setErrorHandler(this.errorHandler);

    return this.fastify;
  };
}

export { Server };
