const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 3000,
    host: '0.0.0.0',
    allowedHosts: 'all',
    client: {
      webSocketURL: 'wss://imdbfinal.codeise.com/ws'
    }
  }
})
