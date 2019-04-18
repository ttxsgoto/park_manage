const api01 = {
    login01: {
        url: '/auth_ttxs/jwt/login/',
        method: 'post',
        notNeedToken: true,
        desc: '登录',
        param: {
            username: {
                desc: '用户名',
            },
            password: {
                desc: '密码',
            }
        }
    },
    list_car_postions: {
        url: '/park/car_postions/',
        method: 'get',
        desc: '车位列表',
        param: {}
    },
    list_members: {
        url: '/park/members/',
        method: 'get',
        desc: '会员列表',
        param: {}
    },
    add_members: {
        url: '/park/members/',
        method: 'post',
        desc: '新增会员',
        param: {}
    },
    update_members: {
        url: '/park/members/:id/',
        method: 'put',
        desc: '修改会员',
        param: {}
    }
};

export default api01
