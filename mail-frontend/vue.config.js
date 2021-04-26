module.exports = {
    publicPath: './',
    assetsDir: 'static',
    productionSourceMap: false,
    devServer: {
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