FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including dev for potential test use)
RUN npm install

# Copy entire project
COPY . .

# Make sure database directory is accessible
RUN mkdir -p /app/data

# Expose Express port
EXPOSE 3000

# Start the app
CMD ["node", "app.js"]
