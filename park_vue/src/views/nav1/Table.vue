<template>
    <section>
        <!--工具条-->
        <!--<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">-->
        <!--<el-form :inline="true" :model="filters">-->
        <!--<el-form-item>-->
        <!--<el-input v-model="filters.name" placeholder="姓名"></el-input>-->
        <!--</el-form-item>-->
        <!--<el-form-item>-->
        <!--<el-button type="primary" v-on:click="getUsers">查询</el-button>-->
        <!--</el-form-item>-->
        <!--<el-form-item>-->
        <!--<el-button type="primary" @click="handleAdd">新增</el-button>-->
        <!--</el-form-item>-->
        <!--</el-form>-->
        <!--</el-col>-->
        <div class="tab-screen">
            <el-form class="search-filters-form" label-width="80px" :model="seachListParam" status-icon
                     ref="seachHeadCarListFrom">
                <el-row :gutter="0">
                    <el-col :span="12">
                        <el-input placeholder="请输入" v-model="fifterParam.keyword" class="search-filters-screen"
                                  @keyup.native.13="searchList">
                            <!--<el-select v-model="fifterParam.field" slot="prepend" placeholder="请选择">-->
                            <!--<el-option v-for="(item,key) in selectData.fieldSelect" :key="key"-->
                            <!--:label="item.value" :value="item.id"></el-option>-->
                            <!--</el-select>-->
                            <el-select v-model="fifterParam.field" slot="prepend" placeholder="请选择">
                                <el-option
                                        v-for="(item,key) in selectData.fieldSelect"
                                        :key="key"
                                        :label="item.value"
                                        :value="item.id">
                                </el-option>
                            </el-select>
                            <el-button slot="append" icon="el-icon-search" @click="searchList"></el-button>
                            <!--<el-button slot="append" @click="searchList"></el-button>-->
                        </el-input>
                    </el-col>
                </el-row>
            </el-form>
        </div>
        <div class="operation-btn text-right">
            <!-- <el-button type="primary" @click="exportList">导出</el-button> -->
            <!--<el-button type="success" @click="addCustomerPayManage">新增</el-button>-->
        </div>
        <!--<el-select v-model="fifterParam.field" placeholder="请选择">-->
        <!--<el-option-->
        <!--v-for="(item,key) in selectData.fieldSelect"-->
        <!--:key="key"-->
        <!--:label="item.value"-->
        <!--:value="item.id">-->
        <!--</el-option>-->
        <!--</el-select>-->

        <!--列表-->
        <!--<el-table :data="users" highlight-current-row v-loading="listLoading" @selection-change="selsChange"-->
        <!--style="width: 100%;">-->

        <!--<el-table-column type="selection" width="55">-->
        <!--</el-table-column>-->
        <!--<el-table-column type="index" width="60">-->
        <!--</el-table-column>-->
        <!--<el-table-column prop="name" label="姓名" width="120" sortable>-->
        <!--</el-table-column>-->
        <!--<el-table-column prop="sex" label="性别" width="100" :formatter="formatSex" sortable>-->
        <!--</el-table-column>-->
        <!--<el-table-column prop="age" label="年龄" width="100" sortable>-->
        <!--</el-table-column>-->
        <!--<el-table-column prop="birth" label="生日" width="120" sortable>-->
        <!--</el-table-column>-->
        <!--<el-table-column prop="addr" label="地址" min-width="180" sortable>-->
        <!--</el-table-column>-->
        <!--<el-table-column label="操作" width="150">-->
        <!--<template scope="scope">-->
        <!--<el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>-->
        <!--<el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>-->
        <!--</template>-->
        <!--</el-table-column>-->
        <!--/新开始/-->
        <el-table :data="tableData" highlight-current-row v-loading="listLoading" @selection-change="selsChange"
                  style="width: 100%;">
            <el-table-column label="付款方名称" align="center" prop="payer">
            </el-table-column>
            <el-table-column label="客户名称" align="center">
                <template slot-scope="scope">
                    <el-row v-if="scope.row.consumer&&scope.row.consumer.length>0" :title="scope.row.customerTitle">
                        <el-col v-for="(item,index) in scope.row.consumer" v-if="index<5">
                            {{item.consumer_name}}
                        </el-col>
                        <el-col v-else>......</el-col>
                    </el-row>
                    <span v-else>-</span>
                </template>
            </el-table-column>
            <el-table-column label="客户简称" align="center">
                <template slot-scope="scope">
                    <el-row v-if="scope.row.consumer&&scope.row.consumer.length>0"
                            :title="scope.row.customerShortTitle">
                        <el-col v-for="(item,index) in scope.row.consumer" v-if="index<5">
                            {{item.short_name}}
                        </el-col>
                        <el-col v-else>......</el-col>
                    </el-row>
                    <span v-else>-</span>
                </template>
            </el-table-column>
            <el-table-column label="业务员" align="center">
                <template slot-scope="scope">
                    <el-row v-if="scope.row.consumer&&scope.row.consumer.length>0" :title="scope.row.saleManTitle">
                        <el-col v-for="(item,index) in scope.row.consumer" v-if="index<5">
                            {{item.sale_man_name}}
                        </el-col>
                        <el-col v-else>......</el-col>
                    </el-row>
                    <span v-else>-</span>
                </template>
            </el-table-column>
            <el-table-column label="添加时间" align="center" prop="created_at">
            </el-table-column>
            <!--<el-table-column label="操作" align="center" width="150" fixed="right">-->
            <!--<template slot-scope="scope">-->
            <!--<el-button size="mini" type="primary" @click="jumpPage({operator:'show',rowData:scope.row})">查看-->
            <!--</el-button>-->
            <!--</template>-->
            <!--</el-table-column>-->
            <el-table-column label="操作" width="150">
                <template scope="scope">
                    <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <!--工具条-->
        <!--<div class="page-list text-center">-->
        <!--<el-pagination.css background layout="prev, pager, next,jumper" :page-count="pageData.totalPage" :page-size="pageData.pageSize" :current-page.sync="pageData.currentPage" @current-change="pageChange" v-if="!pageLoading && pageData.totalPage>1">-->
        <!--</el-pagination.css>-->
        <!--</div>-->
        <!--<el-col :span="24" class="toolbar">-->
        <div class="page-list text-center">
            <el-button class="pagination-button" type="danger" @click="batchRemove" :disabled="this.sels.length===0">
                批量删除
            </el-button>
            <el-pagination layout="prev, pager, next, jumper"
                           :page-count="pageData.totalPage"
                           :page-size="pageData.pageSize"
                           :current-page.sync="pageData.currentPage"
                           @current-change="pageChange" v-if="!pageLoading && pageData.totalPage>1">
            </el-pagination>
        </div>
        <!--@current-change="handleCurrentChange" :page-size="20"-->
        <!--:total="total" style="float:right;">-->
        <!--</el-col>-->

        <!--编辑界面-->
        <el-dialog title="编辑" v-model="editFormVisible" :close-on-click-modal="false">
            <el-form :model="editForm" label-width="80px" :rules="editFormRules" ref="editForm">
                <el-form-item label="姓名" prop="name">
                    <el-input v-model="editForm.name" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="性别">
                    <el-radio-group v-model="editForm.sex">
                        <el-radio class="radio" :label="1">男</el-radio>
                        <el-radio class="radio" :label="0">女</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="年龄">
                    <el-input-number v-model="editForm.age" :min="0" :max="200"></el-input-number>
                </el-form-item>
                <el-form-item label="生日">
                    <el-date-picker type="date" placeholder="选择日期" v-model="editForm.birth"></el-date-picker>
                </el-form-item>
                <el-form-item label="地址">
                    <el-input type="textarea" v-model="editForm.addr"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="editFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
            </div>
        </el-dialog>

        <!--新增界面-->
        <el-dialog title="新增" v-model="addFormVisible" :close-on-click-modal="false">
            <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                <el-form-item label="姓名" prop="name">
                    <el-input v-model="addForm.name" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="性别">
                    <el-radio-group v-model="addForm.sex">
                        <el-radio class="radio" :label="1">男</el-radio>
                        <el-radio class="radio" :label="0">女</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="年龄">
                    <el-input-number v-model="addForm.age" :min="0" :max="200"></el-input-number>
                </el-form-item>
                <el-form-item label="生日">
                    <el-date-picker type="date" placeholder="选择日期" v-model="addForm.birth"></el-date-picker>
                </el-form-item>
                <el-form-item label="地址">
                    <el-input type="textarea" v-model="addForm.addr"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
            </div>
        </el-dialog>
    </section>
</template>

<script>
    import util from '../../common/js/util'
    //import NProgress from 'nprogress'
    import {getUserListPage, removeUser, batchRemoveUser, editUser, addUser} from '../../api/api';

    export default {
        data() {
            return {
                filters: {
                    name: ''
                },
                tableData: [],
                seachListParam: {},
                total: 0,
                page: 1,
                listLoading: false,
                sels: [],//列表选中列

                // 新添加的东西
                selectData: {
                    fieldSelect: [
                        {id: 'consumer_name', value: '客户名称'},
                        {id: 'short_name', value: '客户简称'},
                        {id: 'payer', value: '付款方名称'},
                        {id: 'sale_man_name', value: '分属业务员'},
                    ]
                },
                pageStatus: false,
                pageLoading: true,
                pageData: {
                    currentPage: 1,
                    totalPage: 1,
                    pageSize: 10,
                },
                fifterParam: {
                    keyword: "",
                    field: "consumer_name",
                },
                // end

                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
                editFormRules: {
                    name: [
                        {required: true, message: '请输入姓名', trigger: 'blur'}
                    ]
                },
                //编辑界面数据
                editForm: {
                    id: 0,
                    name: '',
                    sex: -1,
                    age: 0,
                    birth: '',
                    addr: ''
                },

                addFormVisible: false,//新增界面是否显示
                addLoading: false,
                addFormRules: {
                    name: [
                        {required: true, message: '请输入姓名', trigger: 'blur'}
                    ]
                },
                //新增界面数据
                addForm: {
                    name: '',
                    sex: -1,
                    age: 0,
                    birth: '',
                    addr: ''
                }

            }
        },
        methods: {
            //性别显示转换
            formatSex: function (row, column) {
                return row.sex == 1 ? '男' : row.sex == 0 ? '女' : '未知';
            },
            handleCurrentChange(val) {
                this.page = val;
                this.searchList();
            },
            //获取用户列表
            getUsers() {
                let para = {
                    page: this.page,
                    name: this.filters.name
                };
                this.listLoading = true;
                //NProgress.start();
                getUserListPage(para).then((res) => {
                    this.total = res.data.total;
                    this.users = res.data.users;
                    this.listLoading = false;
                    //NProgress.done();
                });
            },
            searchList() {
                var vm = this;
                var sendData = this.pbFunc.deepcopy(this.seachListParam);
                sendData[this.fifterParam.field] = this.fifterParam.keyword;

                vm.pageLoading = true;
                if (vm.pageStatus) {
                    sendData = this.saveSendData;
                    sendData.page = vm.pageData.currentPage;
                } else {
                    this.saveSendData = sendData;
                    sendData.page = 1;
                }
                sendData.pageSize = vm.pageData.pageSize;
                this.$$http01('searchCustomerPayList', sendData).then(function (result) {
                    vm.pageStatus = false;
                    if (result.data.code == 0) {
                        vm.tableData = result.data.data.data;
                        vm.tableData.forEach(Titem => {
                            Titem.customerTitle = "";
                            Titem.saleManTitle = "";
                            if (Titem.consumer && Titem.consumer.length > 0) {
                                Titem.consumer.forEach(Citem => {
                                    Titem.customerTitle += Citem.consumer_name + ",";
                                    Titem.saleManTitle += Citem.sale_man_name + ",";
                                    Titem.customerShortTitle += Citem.short_name + ",";
                                });
                            }
                        });
                        // this.total = Math.ceil(result.data.data.count / vm.pageData.pageSize);
                        vm.pageData.totalPage = Math.ceil(result.data.data.count / vm.pageData.pageSize);
                        vm.pageLoading = false;
                    }
                }).catch(function (error) {
                    vm.pageLoading = false;
                });
            },
            pageChange: function () {
                setTimeout(() => {
                    this.pageStatus = true;
                    this.searchList();
                });
            },
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除该记录吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let para = {id: row.id};
                    removeUser(para).then((res) => {
                        this.listLoading = false;
                        //NProgress.done();
                        this.$message({
                            message: '删除成功',
                            type: 'success'
                        });
                        this.getUsers();
                    });
                }).catch(() => {

                });
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true;
                this.editForm = Object.assign({}, row);
            },
            //显示新增界面
            handleAdd: function () {
                this.addFormVisible = true;
                this.addForm = {
                    name: '',
                    sex: -1,
                    age: 0,
                    birth: '',
                    addr: ''
                };
            },
            //编辑
            editSubmit: function () {
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            this.editLoading = true;
                            //NProgress.start();
                            let para = Object.assign({}, this.editForm);
                            para.birth = (!para.birth || para.birth == '') ? '' : util.formatDate.format(new Date(para.birth), 'yyyy-MM-dd');
                            editUser(para).then((res) => {
                                this.editLoading = false;
                                //NProgress.done();
                                this.$message({
                                    message: '提交成功',
                                    type: 'success'
                                });
                                this.$refs['editForm'].resetFields();
                                this.editFormVisible = false;
                                this.getUsers();
                            });
                        });
                    }
                });
            },
            //新增
            addSubmit: function () {
                this.$refs.addForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            this.addLoading = true;
                            //NProgress.start();
                            let para = Object.assign({}, this.addForm);
                            para.birth = (!para.birth || para.birth == '') ? '' : util.formatDate.format(new Date(para.birth), 'yyyy-MM-dd');
                            addUser(para).then((res) => {
                                this.addLoading = false;
                                //NProgress.done();
                                this.$message({
                                    message: '提交成功',
                                    type: 'success'
                                });
                                this.$refs['addForm'].resetFields();
                                this.addFormVisible = false;
                                this.getUsers();
                            });
                        });
                    }
                });
            },
            selsChange: function (sels) {
                this.sels = sels;
            },
            //批量删除
            batchRemove: function () {
                var ids = this.sels.map(item => item.id).toString();
                this.$confirm('确认删除选中记录吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let para = {ids: ids};
                    batchRemoveUser(para).then((res) => {
                        this.listLoading = false;
                        //NProgress.done();
                        this.$message({
                            message: '删除成功',
                            type: 'success'
                        });
                        this.getUsers();
                    });
                }).catch(() => {

                });
            }
        },
        mounted() {
            // this.getUsers();
            this.searchList();
        }
    }

</script>
<style scoped lang="less">
    /*.page-list {*/
        /*margin: 20px 0;*/
    /*}*/
    /*.text-center {*/
        /*text-align: right;*/
        /*.pagination-button {*/
            /*float: left;*/
            /*width: 200px;*/
        /*}*/
    /*}*/

    /*.pagination.css {*/
    /*text-align: right; //right*/
    /*.pagination.css-button {*/
    /*float:left;*/
    /*width:200px;*/
    /*}*/
    /*}*/
    /*@import '@/assets/css/list_fliter.less'*/
    /*.search-filters-form {*/
    /*> .el-row {*/
    /*padding: 10px 0;*/
    /*}*/
    /*.el-form-item {*/
    /*margin-bottom: 0;*/
    /*}*/
    /*.search-filters-screen {*/
    /*.el-select .el-input {*/
    /*width: 180px;*/
    /*}*/
    /*.el-input-group__prepend {*/
    /*background-color: #fff;*/
    /*}*/
    /*}*/
    /*.el-input {*/
    /*width: 100%;*/
    /*}*/
    /*.el-select {*/
    /*width: 100%;*/
    /*}*/
    /*.el-date-editor--daterange {*/
    /*&.el-input__inner {*/
    /*width: 100%;*/
    /*}*/
    /*}*/
    /*}*/

</style>
<!--<style scoped>-->

<!--</style>-->