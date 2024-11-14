import { createServer } from './fastify';
import { SERVER_PORT, IS_DEVELOPMENT } from './constants';
import { sequelize } from './data-source';

import { CashRegisterClock } from './entity';
import { Model, ModelCtor } from 'sequelize';

function initializeEntities () {
  const entities = [CashRegisterClock] as ModelCtor<Model>[];

  entities.forEach((entity) => {
    entity.sync({
      force: true
    });
  });
}

sequelize.authenticate()
  .then(() => {
    if (IS_DEVELOPMENT) {
      initializeEntities();
    }
    createServer().listen({
      port: SERVER_PORT
    });
  })
  .catch((error) => {
    console.log('Error connecting to the database: ', error);
  });
