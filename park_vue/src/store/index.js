import Vue from 'vue';
import Vuex from 'vuex';

// import * as actions from './actions'
// import * as getters from './getters'
import state from './state';
import getters from './getters';
import actions from './actions';
import mutations from './mutations';
Vue.use(Vuex);
import createLogger from 'vuex/dist/logger'


const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
  strict: debug,
  plugins: debug ? [createLogger()] : []
});
