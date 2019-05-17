// 定义修改操作

import * as types from './mutation-types'


const matutaions = {
    [types.SET_MEMBER](state, member) {
        state.member = member
    }
};


export default matutaions
