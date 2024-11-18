module.exports = {
  apps: [
    {
      name: "units-cashier",
      script: "node_modules/next/dist/bin/next",
      args: "start -p 8080",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "1G",
      env: {
        NODE_ENV: "production"
      }
    }
  ]
};

