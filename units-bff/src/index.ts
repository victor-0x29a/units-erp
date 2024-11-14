import { createServer } from './fastify';
import { SERVER_PORT } from './constants';
import { sequelize } from './data-source';

sequelize.authenticate()
  .then(() => {
    createServer().listen({
      port: SERVER_PORT
    });
  })
  .catch((error) => {
    console.log('Error connecting to the database: ', error);
  });
