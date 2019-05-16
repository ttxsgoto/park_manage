// 初始化操作
import Vue from 'vue'
import Vuex from 'vuex'
import * as actons from './actions'
import * as getters from './getters'
import state from './state01'
import mutations from './mutations'
import createLogger from 'vuex/dist/logger'

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
    actons,
    getters,
    state,
    mutations,
    strict: debug,
    plugins: debug ? [createLogger()] : []

})
