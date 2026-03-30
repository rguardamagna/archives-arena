# Use the full Node.js image to ensure native build tools are present
FROM node:20

# Set the working directory in the container
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
# Using 'install' instead of 'ci' because we added a new pkg to package.json
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port Vite runs on (default 5173)
EXPOSE 5173

# Command to run the development server
# --host 0.0.0.0 is required for Docker to expose the port
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
