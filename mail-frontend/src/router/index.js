import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/showpage'
        },
        {
            path: '/',
            component: () => import(/* webpackChunkName: "home" */ '../components/common/Home.vue'),
            meta: { title: '自述文件' },
            children: [
                // {
                //     path: '/dashboard',
                //     component: () => import(/* webpackChunkName: "dashboard" */ '../components/page/Dashboard.vue'),
                //     meta: { title: '系统首页' }
                // },
                {
                    path: '/showpage',
                    component: () => import(/* webpackChunkName: "showpage" */ '../components/ShowPage.vue'),
                    meta: { title: '首页' , permission: true}
                },
                {
                    path: '/usermanage',
                    component: () => import(/* webpackChunkName: "usermanage" */ '../components/UserManage.vue'),
                    meta: { title: '用户管理' , permission: true}
                },
                {
                    path: '/servercontrol',
                    component: () => import(/* webpackChunkName: "servercontrol" */ '../components/ServerControl.vue'),
                    meta: { title: '服务器管理' , permission: true}
                },
                {
                    path: '/serverconfig',
                    component: () => import(/* webpackChunkName: "serverconfig" */ '../components/ServerConfig.vue'),
                    meta: { title: '配置管理' , permission: true}
                },
                {
                    path: '/logmanage',
                    component: () => import(/* webpackChunkName: "logmanage" */ '../components/LogManage.vue'),
                    meta: { title: '日志管理' , permission: true}
                },
                {
                    path: '/help',
                    component: () => import(/* webpackChunkName: "help" */ '../components/Help.vue'),
                    meta: { title: '帮助文档' , permission: true}
                },
                {
                    path: '/icon',
                    component: () => import(/* webpackChunkName: "icon" */ '../components/page/Icon.vue'),
                    meta: { title: '自定义图标' , permission: true}
                },
                {
                    path: '/table',
                    component: () => import(/* webpackChunkName: "table" */ '../components/page/BaseTable.vue'),
                    meta: { title: '基础表格' , permission: true}
                },
                {
                    path: '/tabs',
                    component: () => import(/* webpackChunkName: "tabs" */ '../components/page/Tabs.vue'),
                    meta: { title: 'tab选项卡' , permission: true}
                },
                {
                    path: '/form',
                    component: () => import(/* webpackChunkName: "form" */ '../components/page/BaseForm.vue'),
                    meta: { title: '基本表单' , permission: true}
                },
                {
                    // 富文本编辑器组件
                    path: '/editor',
                    component: () => import(/* webpackChunkName: "editor" */ '../components/page/VueEditor.vue'),
                    meta: { title: '富文本编辑器' , permission: true}
                },
                {
                    // markdown组件
                    path: '/markdown',
                    component: () => import(/* webpackChunkName: "markdown" */ '../components/page/Markdown.vue'),
                    meta: { title: 'markdown编辑器' , permission: true}
                },
                {
                    // 图片上传组件
                    path: '/upload',
                    component: () => import(/* webpackChunkName: "upload" */ '../components/page/Upload.vue'),
                    meta: { title: '文件上传' , permission: true}
                },
                {
                    // vue-schart组件
                    path: '/charts',
                    component: () => import(/* webpackChunkName: "chart" */ '../components/page/BaseCharts.vue'),
                    meta: { title: 'schart图表' , permission: true}
                },
                {
                    // 拖拽列表组件
                    path: '/drag',
                    component: () => import(/* webpackChunkName: "drag" */ '../components/page/DragList.vue'),
                    meta: { title: '拖拽列表' , permission: true}
                },
                {
                    // 拖拽Dialog组件
                    path: '/dialog',
                    component: () => import(/* webpackChunkName: "dragdialog" */ '../components/page/DragDialog.vue'),
                    meta: { title: '拖拽弹框' , permission: true}
                },
                // {
                //     // 国际化组件
                //     path: '/i18n',
                //     component: () => import(/* webpackChunkName: "i18n" */ '../components/page/I18n.vue'),
                //     meta: { title: '国际化' }
                // },
                {
                    // 权限页面
                    path: '/permission',
                    component: () => import(/* webpackChunkName: "permission" */ '../components/page/Permission.vue'),
                    meta: { title: '权限测试', permission: true }
                },
                {
                    path: '/404',
                    component: () => import(/* webpackChunkName: "404" */ '../components/page/404.vue'),
                    meta: { title: '404' }
                },
                {
                    path: '/403',
                    component: () => import(/* webpackChunkName: "403" */ '../components/page/403.vue'),
                    meta: { title: '403' }
                },
                // {
                //     path: '/donate',
                //     component: () => import(/* webpackChunkName: "donate" */ '../components/page/Donate.vue'),
                //     meta: { title: '支持作者' }
                // }
            ]
        },
        {
            // path: '/login',
            // component: () => import(/* webpackChunkName: "login" */ '../components/page/Login.vue'),
            // meta: { title: '登录' }
            path: '/loginpage',
            component: () => import(/* webpackChunkName: "login" */ '../components/LoginPage.vue'),
            meta: { title: '登录' }
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
});
