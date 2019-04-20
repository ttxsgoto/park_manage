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
    },
    del_members: {
        url: '/park/members/:id/',
        method: 'delete',
        desc: '删除会员',
        param: {
            id: {
                desc: '会员ID'
            }
        }
    },
    list_member_amount: {
        url: '/park/member_amount/',
        method: 'get',
        desc: '会员金额',
        param: {}
    },
    list_temp_amount: {
        url: '/park/temp_amount/',
        method: 'get',
        desc: '停车费用',
        param: {}
    },
    list_users: {
        url: '/park/user/',
        method: 'get',
        desc: '用户列表',
        param: {}
    },
    come_in_park: {
        url: '/park/temp_amount/',
        method: 'post',
        desc: '进入停车场',
        param: {}
    },
    come_out_park: {
        url: '/park/temp_amount/leave/',
        method: 'post',
        desc: '离开停车收费',
        param: {}
    }
};

export default api01
