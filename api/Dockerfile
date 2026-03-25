FROM node:24-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install --omit=dev

# Copy application code
COPY src/ ./src/

# Expose API port
EXPOSE 3001

# Start application
CMD ["npm", "start"]
