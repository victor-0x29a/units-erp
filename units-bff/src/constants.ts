import dotenv from "dotenv";

const environment = process.env.NODE_ENV;

dotenv.config({ path: `./.env.${environment}` });

export const SERVER_PORT = Number(process.env.SERVER_PORT || 4500);

export const CAN_LOG = Boolean(Number(process.env.CAN_LOG));
