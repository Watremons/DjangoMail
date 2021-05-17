const os = require('os');
function getNetworkIp() {
    let needHost = ''; // 打开的host
    try {
        // 获得网络接口列表
        let network = os.networkInterfaces();
        for (let dev in network) {
            let iface = network[dev];
            for (let i = 0; i < iface.length; i++) {
                let alias = iface[i];
                if (alias.family === 'IPv4' && alias.address !== '127.0.0.1' && !alias.internal) {
                    needHost = alias.address;
                }
            }
        }
    } catch (e) {
        needHost = 'localhost';
    }
    return needHost;
}

module.exports = {
    publicPath: './',
    assetsDir: 'static',
    productionSourceMap: false,
    devServer: {
        host: '0.0.0.0',
        public: getNetworkIp() + ":8080",
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