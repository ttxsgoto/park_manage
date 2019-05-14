import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router);


import Login from '../views/Login.vue'
import NotFound from '../views/404.vue'
import Home from '../views/Home.vue'
import Main from '../views/Main.vue'
import Table from '../views/nav1/Table.vue'
import Form from '../views/nav1/Form.vue'
import user from '../views/nav1/user.vue'
import Page4 from '../views/nav2/Page4.vue'
import Page5 from '../views/nav2/Page5.vue'
import Page6 from '../views/nav3/Page6.vue'
import echarts from '../views/charts/echarts.vue'
import arap from '../views/arap/arap'
import paymentManage from '../views/arap/supplierMeetManage/paymentManage'
// import carpostion from '../views/carpostion/carpostion'
// import members from '../views/members/memberlist'
// import amount from '../views/amount/amountlist'

let routes = [
    {
        path: '/login',
        component: Login,
        name: '',
        hidden: true
    },
    {
        path: '/404',
        component: NotFound,
        name: '',
        hidden: true
    },
    {
        path: '/setting',
        component: Home,
        name: '个人设置',
        hidden: true,
        children: [
            {
                name: '个人设置',
                path: '/setting',
                component: (resolve) => require(['../views/Setting'], resolve),
                // component: carpostion,
            },
        ]
    },
    // { path: '/main', component: Main },
    {
        path: '/',
        component: Home,
        name: '订单管理',
        iconCls: 'el-icon-message',//图标样式class
        children: [
            {path: '/main', component: Main, name: '主页', hidden: true},
            {path: '/table', component: Table, name: 'Table'},
            {path: '/form', component: Form, name: 'Form'},
            {path: '/user', component: user, name: '列表'},
        ]
    },
    // {
    //     path: '/',
    //     component: Home,
    //     name: '导航二',
    //     iconCls: 'fa fa-id-card-o',
    //     children: [
    //         {path: '/page4', component: Page4, name: '页面4'},
    //         {path: '/page5', component: Page5, name: '页面5'}
    //     ]
    // },
    // {
    //     path: '/',
    //     component: Home,
    //     name: '',
    //     iconCls: 'fa fa-address-card',
    //     leaf: true,//只有一个节点
    //     children: [
    //         {path: '/page6', component: Page6, name: '导航三'}
    //     ]
    // },
    // {
    //     path: '/',
    //     component: Home,
    //     name: 'Charts',
    //     iconCls: 'fa fa-bar-chart',
    //     children: [
    //         {path: '/echarts', component: echarts, name: 'echarts'}
    //     ]
    // },
    {
        path: '/arpa',
        component: Home,
        name: '应收应付',
        iconCls: 'el-icon-message',//图标样式class
        children: [
            {
                name: '供应商管理',
                path: '/supplierManage',
                component: arap,
            },
            {
                name: '付款方管理',
                path: '/paymentManage',
                component: Table,
            },
            {
                name: 'Form',
                path: '/form',
                component: Form,
            },
            {
                name: '列表',
                path: '/user',
                component: user,
            },
        ]
    },
    {
        path: '/paymentManage',
        component: Home,
        name: '付款方管理',
        hidden: true,
        children: [
            {
                name: '付款方管理',
                path: '/paymentManage',
                component: paymentManage,
            }
        ]
    },
    {
        path: '/carpostion',
        component: Home,
        name: '车位管理',
        iconCls: 'el-icon-menu',
        leaf: true,//只有一个节点
        children: [
            {
                name: '车位管理',
                path: '/carpostion',
                component: (resolve) => require(['../views/carpostion/carpostion'], resolve),
                // component: carpostion,
            },
        ]
    },
    {
        path: '/',
        component: Home,
        name: '会员管理',
        iconCls: 'fa fa-id-card-o',
        // leaf: true,//只有一个节点
        children: [
            {
                name: '会员管理',
                path: '/members/list',
                component: (resolve) => require(['../views/members/memberlist'], resolve),
                // component: members,
            },
            {
                name: '费用管理',
                path: '/amount/list',
                // leaf: true,
                hidden: true,
                component: (resolve) => require(['../views/amount/amountlist'], resolve),
            },
        ]
    },
    {
        path: '/',
        component: Home,
        name: '人员管理',
        iconCls: 'el-icon-menu',
        leaf: true,//只有一个节点
        children: [
            {
                name: '人员管理',
                path: '/people',
                component: (resolve) => require(['../views/members/memberlist_2'], resolve),
            },
            {
                name: '人员管理添加',
                path: '/people/add',
                // leaf: true,
                hidden: true,
                component: (resolve) => require(['../views/members/memberAdd'], resolve),
            },
            {
                name: '人员管理详情',
                path: 'people/:id/',
                hidden: true,
                component: (resolve) => require(['../views/members/memberDetails'], resolve),
            },
            {
                name: '人员管理编辑',
                path: 'people_/:id/',
                hidden: true,
                component: (resolve) => require(['../views/members/memberEdit'], resolve),
            }
        ]
    },
    // {
    //     path: '/',
    //     component: Home,
    //     name: '费用管理',
    //     // iconCls: 'el-icon-message',//图标样式class
    //     iconCls: 'fa fa-bar-chart',//图标样式class
    //     // leaf: true,//只有一个节点
    //     hidden: true,
    //     children: [
    //         {path: '/amount', component: (resolve) => require(['../views/amount/amountlist'], resolve), name: '费用管理',},
    //     ]
    // },
    // {
    //     path: '/',
    //     component: Home,
    //     name: '出入管理',
    //     iconCls: 'fa fa-id-card-o',
    //     leaf: true,//只有一个节点
    //     children: [
    //         {path: '/members', component: members, name: '出入管理',},
    //     ]
    // },
    {
        path: '*',
        hidden: true,
        redirect: {path: '/404'}
    }
];

const router = new Router({
    routes
});

router.beforeEach((to, from, next) => {
    //NProgress.start();
    if (to.path == '/login') {
        sessionStorage.removeItem('user');
    }
    let user = JSON.parse(sessionStorage.getItem('user'));
    if (!user && to.path != '/login') {
        next({path: '/login'})
    } else {
        next()
    }
});

export default router;
