import { CAN_LOG, SERVER_PORT } from "./constants";
import { Server } from "./server";

new Server(SERVER_PORT, CAN_LOG).start();
