import Fastify, { FastifyInstance } from "fastify";
import controllers from './controllers';
import { errorHandler } from './middlewares';
import { CAN_LOG } from "./constants";

export const createServer = (): FastifyInstance => {
  const fastify = Fastify({
    logger: CAN_LOG,
  }) as FastifyInstance;

  controllers.forEach((controllerOpts) => {
    const Controller = controllerOpts[0];
    const prefix = controllerOpts[1];
    fastify.register((instance, opts, done) => {
      new Controller(instance);
      done();
    }, {
      prefix
    });
  });

  fastify.setErrorHandler(errorHandler);

  return fastify;
};
