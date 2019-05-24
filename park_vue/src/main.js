import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
//import 'element-ui/lib/theme-default/index.css'
import 'element-ui/lib/theme-chalk/index.css'
import './assets/css/page.less'
import './assets/css/list_fliter.less'
import router from './router'
import store from './store'
// import store from './vuex/store'
import Vuex from 'vuex'

import {httpServer} from "./api/index"
import * as pbFunc from "./assets/utils";

Vue.prototype.pbFunc = pbFunc;
Vue.prototype.$$http = httpServer;

//import NProgress from 'nprogress'
//import 'nprogress/nprogress.css'
// import routesJs from './routesJs'
// import Mock from './mock'

// Mock.bootstrap();
import 'font-awesome/css/font-awesome.min.css'

Vue.use(ElementUI);
Vue.use(Vuex);

//NProgress.configure({ showSpinner: false });

new Vue({
    el: '#app',
    //template: '<App/>',
    router,
    store,
    //components: { App }
    render: h => h(App)
})
    // .$mount('#app')
