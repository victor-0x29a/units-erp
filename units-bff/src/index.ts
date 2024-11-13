import { createServer } from './fastify';
import { SERVER_PORT } from './constants';

createServer().listen({
  port: SERVER_PORT
});
