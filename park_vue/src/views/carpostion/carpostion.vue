<style scoped lang="less">
</style>
<template>
    <div>
        <div class="nav-tab">
            <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
                <!-- <el-tab-pane label="车位管理" name="payment"> -->
                <div class="tab-screen">
                    <el-form class="search-filters-form" label-width="80px" :model="searchFilters" status-icon>
                        <el-row :gutter="0">
                            <el-col :span="12">
                                <el-input placeholder="请输入" v-model="searchFilters.keyword"
                                          @keyup.native.13="startSearch" class="search-filters-screen">
                                    <el-select v-model="searchFilters.field" slot="prepend" placeholder="请选择">
                                        <el-option v-for="(item,key) in selectData.fieldSelect" :key="key"
                                                   :label="item.value" :value="item.id"></el-option>
                                    </el-select>
                                    <el-button slot="append" icon="el-icon-search" @click="startSearch"></el-button>
                                </el-input>
                            </el-col>
                        </el-row>
                        <el-row :gutter="10">
                            <!--<el-col :span="8">-->
                            <!--<el-form-item label="装车完成时间:" label-width="105px">-->
                            <!--<el-date-picker v-model="planArriveTime" type="datetimerange" @change="startSearch" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd HH:mm:ss" :default-time="['00:00:00', '23:59:59']"></el-date-picker>-->
                            <!--&lt;!&ndash; <el-date-picker v-model="planArriveTime" type="daterange" @change="startSearch" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd"></el-date-picker> &ndash;&gt;-->
                            <!--</el-form-item>-->
                            <!--</el-col>-->
                            <!--<el-col :span="6">-->
                            <!--<el-form-item label="运单状态:">-->
                            <!--<el-select v-model="searchFilters.waybill_status" filterable @change="startSearch" placeholder="请选择">-->
                            <!--<el-option v-for="(item,key) in selectData.waybillStatusSelect" :key="key" :label="item.value" :value="item.id"></el-option>-->
                            <!--</el-select>-->
                            <!--</el-form-item>-->
                            <!--</el-col>-->
                            <el-col :span="5">
                                <el-form-item label="是否使用:">
                                    <el-select v-model="searchFilters.is_valid" @change="startSearch" placeholder="请选择">
                                        <el-option v-for="(item,key) in selectData.isValidSelect" :key="key"
                                                   :label="item.value" :value="item.id"></el-option>
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="5">
                                <el-form-item label="会员位:">
                                    <el-select v-model="searchFilters.is_member" filterable @change="startSearch"
                                               placeholder="请选择">
                                        <el-option v-for="(item,key) in selectData.isMemberSelect" :key="key"
                                                   :label="item.value" :value="item.id"></el-option>
                                    </el-select>
                                </el-form-item>
                            </el-col>
                        </el-row>
                    </el-form>
                </div>
                <div class="operation-btn text-right" style="border:5px;text-align:right;float:right">
                    <!-- <el-button type="primary" plain @click="" >导入</el-button> -->
                    <!--<el-button type="primary">导出</el-button>-->
                    <!--<el-button type="primary" @click="arapDialogEdit('add')">新增</el-button>-->
                </div>
                <div class="table-list">
                    <el-table :data="tableData" stripe style="width: 100%" size="mini" max-height="600"
                              v-loading="pageLoading" :class="{'tabal-height-500':!tableData.length}">
                        <el-table-column v-for="(item,key) in thTableList" :key="key" :prop="item.param"
                                         align="center" :label="item.title" :width="item.width">
                            <!--<template slot-scope="scope">-->
                            <!--<div v-if="item.param==='payment_datetime'">{{scope.row[item.param]|dateFilter}}-->
                            <!--</div>-->
                            <!--<div v-else>-->
                            <!--<div v-if="item.param==='desc'" class='td-hover' :title="scope.row[item.param]">-->
                            <!--{{scope.row[item.param]}}-->
                            <!--</div>-->
                            <!--<div v-else>-->
                            <!--{{scope.row[item.param]}}-->
                            <!--</div>-->
                            <!--</div>-->
                            <!--</template>-->
                        </el-table-column>
                        <el-table-column label="操作" align="center">
                            <template scope="scope">
                                <el-button type="primary" size="mini" @click="arapDialogEdit('update',scope.row)">
                                    详情
                                </el-button>
                                <!--<el-button type="primary" size="mini" @click="arapDialogEdit('update',scope.row)">-->
                                    <!--修改-->
                                <!--</el-button>-->
                            </template>
                        </el-table-column>
                    </el-table>
                    <no-data v-if="!pageLoading && !tableData.length"></no-data>
                </div>
                <div class="page-list text-center">
                    <el-pagination background layout="prev, pager, next, jumper" :total="pageData.totalCount"
                                   :page-size="pageData.pageSize" :current-page.sync="pageData.currentPage"
                                   @current-change="pageChange" v-if="!pageLoading && pageData.totalCount>10">
                    </el-pagination>
                </div>
                <!-- </el-tab-pane> -->
            </el-tabs>
        </div>
        <postion-detail :arap-dialog="arapDialog" v-on:closeDialogBtn="closeDialog"
        :arap-row="arapRow"></postion-detail>
    </div>
</template>
<script>
    import PostionDetail from './carpostiondetailDialog';

    export default {
        name: 'carpostionList',
        components: {
            PostionDetail: PostionDetail
        },
        computed: {},
        data() {
            return {
                pageLoading: false,
                pageData: {
                    currentPage: 1,
                    totalCount: '',
                    pageSize: 10,
                },
                activeName: 'payment',
                searchPostData: {}, //搜索参数
                searchFilters: {
                    is_valid: this.$route.query.is_valid ? this.$route.query.is_valid : '',
                    is_member: this.$route.query.is_member ? this.$route.query.is_member : '',
                    keyword: '',
                    field: 'plate_number',
                },
                payerTime: [], //付款时间
                selectData: {
                    fieldSelect: [
                        {id: 'plate_number', value: '车牌号'},
                    ],
                    isValidSelect: [
                        {id: '', value: '全部'},
                        {id: 'True', value: '已使用'},
                        {id: 'False', value: '未使用'}
                    ],
                    isMemberSelect: [
                        {id: '', value: '全部'},
                        {id: 'True', value: '是'},
                        {id: 'False', value: '否'}
                    ],
                },
                thTableList: [{
                    title: '车位号',
                    param: 'id',
                    width: '100'
                }, {
                    title: '车牌号',
                    param: 'plate_number',
                    width: '200'
                }, {
                    title: '可使用',
                    param: 'is_valid_ch',
                    width: '100'
                }, {
                    title: '会员位',
                    param: 'is_member_ch',
                    width: '200'
                }, {
                    title: '添加时间',
                    param: 'created_time',
                    width: ''
                }],
                tableData: [],
                arapDialog: {
                    isShow: false,
                    type: 'add'
                }, //弹窗
                arapRow: {} //内容
            }
        },
        methods: {
            closeDialog: function (isSave) {
                this.arapDialog.isShow = false;
                if (isSave) {
                    this.getList();
                }
            },
            // 调账
            arapDialogEdit(type, row) {
                this.arapDialog = {
                    isShow: true,
                    type: type
                };
                if (row) {
                    this.arapRow = row;
                }

            },
            startSearch() {
                this.pageData.currentPage = 1;
                this.searchPostData = this.pbFunc.deepcopy(this.searchFilters);
                this.getList();
                if (this.pbFunc.objSize(this.$route.query)) {
                    this.$router.push({path: this.$route.path})
                }
            },
            pageChange() {
                setTimeout(() => {
                    this.getList();
                })
            },
            getList: function () {
                let postData = {
                    page: this.pageData.currentPage,
                    page_size: this.pageData.pageSize,
                    is_valid: this.searchPostData.is_valid,
                    is_member: this.searchPostData.is_member,
                    searchPostData: this.searchPostData.waybill_status
                };
                postData[this.searchPostData.field] = this.searchPostData.keyword;
                postData = this.pbFunc.fifterObjIsNull(postData);
                this.pageLoading = true;
                this.$$http01('list_car_postions', postData).then((results) => {
                    this.pageLoading = false;
                    if (results.data && results.data.code == 0) {
                        this.tableData = results.data.data.data;
                        this.pageData.totalCount = results.data.data.count;
                    }
                }).catch((err) => {
                    this.pageLoading = false;
                })

            },

        },

        handleClick: function (tab, event) {
            if (tab.name === 'meet') {
                this.$router.push({path: "/supplierManage"});
            }
        },
        pageChange: function () {
            setTimeout(() => {
                this.getList();
            })
        },
        activated() {
            this.activeName = 'payment'
        },
        created: function () {
            this.getList();
        }
    }

</script>
