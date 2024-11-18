import { Sequelize } from "sequelize";
import {
  MYSQL_DATABASE,
  MYSQL_HOSTNAME,
  MYSQL_PASSWORD,
  MYSQL_PORT,
  MYSQL_USER,
  CAN_LOG
} from "./constants";

export const sequelize = new Sequelize({
  dialect: "mysql",
  host: MYSQL_HOSTNAME,
  port: MYSQL_PORT,
  username: MYSQL_USER,
  password: MYSQL_PASSWORD,
  database: MYSQL_DATABASE,
  logging: CAN_LOG ? console.log : false,
});
