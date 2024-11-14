import { DataTypes } from "sequelize";
import { sequelize } from "../data-source";


const CashRegisterClock = sequelize.define('cash_register_clock', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  employee_document: {
    type: DataTypes.STRING,
    allowNull: false
  },
  clock_in: {
    type: DataTypes.DATE,
    allowNull: false
  },
  clock_lunch_out: {
    type: DataTypes.DATE,
    allowNull: true,
    defaultValue: null
  },
  clock_lunch_in: {
    type: DataTypes.DATE,
    allowNull: true,
    defaultValue: null
  },
  clock_out: {
    type: DataTypes.DATE,
    allowNull: true,
    defaultValue: null
  }
});

export {
  CashRegisterClock
};
