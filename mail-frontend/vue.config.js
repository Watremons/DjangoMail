module.exports = {
    publicPath: './',
    assetsDir: 'static',
    productionSourceMap: false,
    devServer: {
        host: '0.0.0.0',
        port: 8080,
        https: false,
        hotOnly: false,
        disableHostCheck:true,
        open: true,
        proxy: {
            '/apis': {    
                target: 'http://127.0.0.1:8000',  // 接口域名
                changeOrigin: true,  //是否跨域
                ws: true,
                pathRewrite: {
                    '^/apis':''
                }
            }
        }
    }
}