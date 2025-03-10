# frontend/Dockerfile

# Use an official Node.js runtime as a parent image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 3000
# Build the application for production
RUN npm run build

# Set environment variables to disable debugging and error messages
ENV NODE_ENV=production
ENV DEBUG=off
# Command to run the application
CMD ["npm", "run", "dev"]