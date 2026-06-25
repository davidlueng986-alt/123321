module.exports = {
  apps: [
    {
      name: "finsight-ai",
      script: "start-server.sh",
      interpreter: "bash",
      cwd: "/home/user/webapp",
      watch: false,
      autorestart: false,
      env: {
        NODE_ENV: "development",
      },
    },
  ],
}
