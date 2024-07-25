import { FastifyReply, FastifyRequest } from "fastify";

export type FastifyHandler = (
  request: FastifyRequest,
  reply: FastifyReply
) => void | Promise<void> | Promise<unknown>;
