const { Sequelize } = require('sequelize');
const path = require('path');

const dbPath = path.join(__dirname, '..', 'job_portal.db');

const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: dbPath,
  logging: false,
});

async function connectDB() {
  try {
    await sequelize.authenticate();
    console.log('Database connected successfully');
    return sequelize;
  } catch (error) {
    console.error('Unable to connect to database:', error.message);
    throw error;
  }
}

module.exports = {
  connectDB,
  sequelize,
};
