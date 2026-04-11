const { Sequelize } = require('sequelize');
const path = require('path');

// Use DB_PATH from environment (Docker) or fall back to project root (local dev)
const dbPath = process.env.DB_PATH || path.join(__dirname, '..', 'job_portal.db');

const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: dbPath,
  logging: false,
});

async function connectDB() {
  try {
    await sequelize.authenticate();
    console.log('Database connected successfully at:', dbPath);
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
