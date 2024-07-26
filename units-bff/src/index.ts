import { CAN_LOG, SERVER_PORT } from "./constants";
import { Server } from "./server";

new Server(CAN_LOG).start().listen({ port: SERVER_PORT });
