import Fastify, { FastifyInstance } from "fastify";
import controllers from './controllers';
import { errorHandler } from './middlewares';
import { CAN_LOG } from "./constants";

export const createServer = (): FastifyInstance => {
  const fastify = Fastify({
    logger: CAN_LOG,
  }) as FastifyInstance;

  controllers.forEach((Controller) => {
    new Controller(fastify);
  });

  fastify.setErrorHandler(errorHandler);

  return fastify;
};