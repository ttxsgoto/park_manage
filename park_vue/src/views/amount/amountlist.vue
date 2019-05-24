<style scoped lang="less">
</style>
<template>
    <div>
        <div class="nav-tab">
          <!-- <el-tabs v-model="activeName" type="card" @tab-click="handleClick"> -->
            <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
                <el-tab-pane label="会员管理" name="members"> </el-tab-pane>
                <el-tab-pane label="费用管理" name="payment">
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
                                <el-col :span="8">
                                    <el-form-item label="费用时间:" label-width="105px">
                                        <el-date-picker v-model="CreatedTime" type="datetimerange" @change="startSearch"
                                                        range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期"
                                                        value-format="yyyy-MM-dd HH:mm:ss"
                                                        :default-time="['00:00:00', '23:59:59']">
                                        </el-date-picker>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="6">
                                    <el-form-item label="操作人:">
                                        <el-select v-model="searchFilters.creator" @change="startSearch" placeholder="请选择">
                                            <el-option v-for="(item,key) in selectData.CreatorList" :key="key"
                                                       :label="item.username" :value="item.id"></el-option>
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                        </el-form>
                    </div>
                </el-tab-pane>
                <div class="operation-btn text-right" style="border:5px;text-align:right;float:right">
                    <el-button type="primary" @click="arapDialogEdit('add')">进入</el-button>
                    <el-button type="danger" @click="arapDialogEdit('del')">离开</el-button>
                </div>
                <h4>会员费用</h4>
                <div class="table-list">
                    <el-table :data="tableData" stripe style="width: 100%" size="mini" max-height="600"
                              v-loading="pageLoading" :class="{'tabal-height-500':!tableData.length}"
                              @selection-change="handleSelectionChange">
                        <el-table-column v-for="(item,key) in thTableList" :key="key" :prop="item.param"
                                         align="center" :label="item.title" :width="item.width">
                        </el-table-column>
                    </el-table>
                    <no-data v-if="!pageLoading && !tableData.length"></no-data>
                </div>
                <h4>停车费用</h4>
                <div class="table-list">
                    <el-table :data="tableData02" stripe style="width: 100%" size="mini" max-height="600"
                              v-loading="pageLoading" :class="{'tabal-height-500':!tableData02.length}"
                              @selection-change="handleSelectionChange">
                        <el-table-column v-for="(item,key) in thTableList02" :key="key" :prop="item.param"
                                         align="center" :label="item.title" :width="item.width">
                        </el-table-column>
                    </el-table>
                    <no-data v-if="!pageLoading && !tableData02.length"></no-data>
                </div>

                <h4>总费用 {{ this.all_sum }}</h4>
                <div class="page-list text-center">
                    <el-pagination background layout="prev, pager, next, jumper" :total="pageData02.totalCount"
                                   :page-size="pageData02.pageSize" :current-page.sync="pageData02.currentPage"
                                   @current-change="pageChange"
                                   v-if="(!pageLoading && pageData.totalCount>10) || (!pageLoading &&pageData02.totalCount>10)">
                    </el-pagination>
                </div>
            </el-tabs>
        </div>
        <amount-dialog :arap-dialog="arapDialog" v-on:closeDialogBtn="closeDialog"
                       :arap-row="arapRow"></amount-dialog>
    </div>
</template>
<script>
    import AmountDialog from './amountDialog';

    export default {
        name: 'AmountList',
        components: {
            AmountDialog: AmountDialog
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
                pageData02: {
                    currentPage: 1,
                    totalCount: '',
                    pageSize: 10,
                },
                activeName: 'payment',
                searchPostData: {}, //搜索参数
                multipleSelection: [],
                all_sum: 0.00, // 总金额
                CreatedTime: ['2019-01-01 00:00:00', '2019-12-30 23:59:00'], // 费用时间
                multiSelectString: '',
                searchFilters: {
                    plan_arrive_time: [],
                    creator: this.$route.query.creator ? this.$route.query.creator : '',
                    keyword: '',
                    field: 'plate_number',
                },
                payerTime: [], //付款时间
                selectData: {
                    fieldSelect: [
                        // {id: 'username', value: '会员姓名'},
                        {id: 'plate_number', value: '车牌号'}
                    ],
                    CreatorList: [],
                    isMemberSelect: [
                        {id: '', value: '全部'},
                        {id: 'True', value: '是'},
                        {id: 'False', value: '否'}
                    ],
                },
                thTableList: [{
                    title: '车牌号码',
                    param: 'member.plate_number',
                    width: '100'
                }, {
                    title: '金额',
                    param: 'money',
                    width: '80'
                }, {
                    title: '会员姓名',
                    param: 'member.username',
                    width: '100'
                }, {
                    title: '会员电话',
                    param: 'member.phone',
                    width: '180'
                }, {
                    title: '会员类型',
                    param: 'member.member_type_ch',
                    width: '100'
                }, {
                    title: '车辆类型',
                    param: 'member.type_ch',
                    width: '100'
                }, {
                    title: '费用时间',
                    param: 'created_time',
                    width: '200'
                }, {
                    title: '操作人',
                    param: 'member.creator_name',
                    width: '100',
                }],
                tableData: [],
                thTableList02: [{
                    title: '车牌号码',
                    param: 'plate_number',
                    width: '100'
                }, {
                    title: '金额',
                    param: 'money',
                    width: '80'
                }, {
                    title: '停车位',
                    param: 'postion',
                    width: '200'
                }, {
                    title: '进入时间',
                    param: 'enter_time',
                    width: '200'
                }, {
                    title: '离开时间',
                    param: 'leave_time',
                    width: '200'
                }, {
                    title: '停车时长',
                    param: 'time_duration',
                    width: '200'
                }, {
                    title: '会员',
                    param: 'is_member_ch',
                    width: '200'
                }, {
                    title: '操作人',
                    param: 'creator_name',
                    width: '200'
                }],
                tableData02: [],
                arapDialog: {
                    isShow: false,
                    type: 'add'
                }, //弹窗
                arapRow: {}, //内容
                data1: []
            }
        },
        methods: {
          handleClick: function(tab, event) {
            if (tab.name === 'members') {
              this.$router.push({ path: "/members/list" });
            }
          },
            closeDialog: function (isSave) {
                this.arapDialog.isShow = false;
                if (isSave) {
                    // this.get_temp_list();
                    // setTimeout(() => {
                    // let nowDate = new Date();
                    // let nowDateDetail = this.pbFunc.getDateDetail(nowDate);
                    // let nowDateStr = nowDateDetail.year + '-' + nowDateDetail.month + '-' + nowDateDetail.day + ' ' + nowDateDetail.hour + ':' + nowDateDetail.minute + ':' + nowDateDetail.second;
                    //
                    // this.CreatedTime = ['2019-01-01 08:00:00', nowDateStr];
                    // this.searchPostData = this.pbFunc.deepcopy(this.searchFilters);
                    // this.getList();
                    this.getList();
                    // })
                }
            },
            handleSelectionChange(val) {
                this.multipleSelection = val;
                if (val.length > 0) {
                    this.calculation();
                }
            },
            calculation() {
                let SelectList = [];
                this.multipleSelection.forEach(item => {
                    SelectList.push(item.id)
                });
                this.multiSelectString = SelectList.toLocaleString()
            },
            //删除
            handleDel(id) {
                if (this.multipleSelection == '') {
                    this.$alert('请选择需要删除的列', '提示', {
                        confirmButtonText: '确定',
                    })
                } else if (this.multipleSelection.length > 1) {
                    this.$alert('每次只能删除一个会员', '提示', {
                        confirmButtonText: '确定',
                    })
                } else {
                    this.$confirm('确认删除该记录吗?', '提示', {
                        type: 'warning'
                    }).then(() => {
                        this.$$http('del_members', {id: id}).then((results) => {
                            if (results.data && results.data.code == 0) {
                                this.$message({
                                    message: '删除会员成功',
                                    type: 'success'
                                });
                                this.getList();
                            }
                        }).catch((err) => {
                            this.$message.error({
                                type: 'info',
                                mesage: '删除职位失败'
                            });
                        });
                    })
                }
            },
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
            get_temp_list() {
                let postData = {
                    page: this.pageData02.currentPage,
                    page_size: this.pageData02.pageSize,
                };
                this.$$http('list_member_amount', postData).then((results) => {
                    this.pageLoading = false;
                    if (results.data && results.data.code == 0) {
                        this.tableData = results.data.data.data;
                        this.all_sum = results.data.all_sum;
                        this.pageData.totalCount = results.data.data.count;
                    }
                }).catch((err) => {
                    this.pageLoading = false;
                });
            },
            getList: function () {
                let postData = {
                    page: this.pageData02.currentPage,
                    page_size: this.pageData02.pageSize,
                    plate_number: this.searchPostData.plate_number,
                    creator: this.searchPostData.creator,
                };
                if (this.CreatedTime instanceof Array && this.CreatedTime.length > 0) {
                    let nowDateDetail = this.pbFunc.getDateDetail(new Date(this.CreatedTime[0]));
                    let nowDateDetail1 = this.pbFunc.getDateDetail(new Date(this.CreatedTime[1]));
                    let startDateStr = nowDateDetail.year + '-' + nowDateDetail.month + '-' + nowDateDetail.day + ' ' + nowDateDetail.hour + ':' + nowDateDetail.minute + ':' + nowDateDetail.second;
                    let endDateStr = nowDateDetail1.year + '-' + nowDateDetail1.month + '-' + nowDateDetail1.day + ' ' + nowDateDetail1.hour + ':' + nowDateDetail1.minute + ':' + nowDateDetail1.second;
                    postData.created_time_start = startDateStr;
                    postData.created_time_end = endDateStr;
                }
                postData[this.searchPostData.field] = this.searchPostData.keyword;
                postData = this.pbFunc.fifterObjIsNull(postData);
                this.pageLoading = true;
                this.$$http('list_member_amount', postData).then((results) => {
                    this.pageLoading = false;
                    if (results.data && results.data.code == 0) {
                        this.tableData = results.data.data.data;
                        this.all_sum = results.data.all_sum;
                        this.pageData.totalCount = results.data.data.count;
                    }
                }).catch((err) => {
                    this.pageLoading = false;
                });
                this.$$http('list_temp_amount', postData).then((results) => {
                    this.pageLoading = false;
                    if (results.data && results.data.code == 0) {
                        this.tableData02 = results.data.data.data;
                        this.pageData02.totalCount = results.data.data.count;
                    }
                }).catch((err) => {
                    this.pageLoading = false;
                });
                this.$$http('list_users', postData).then((results) => {
                    this.pageLoading = false;
                    if (results.data && results.data.code == 0) {
                        this.data1 = results.data.data;
                        this.data1.push('');
                        this.selectData.CreatorList = this.data1;
                    }
                }).catch((err) => {
                    this.pageLoading = false;
                })
            }
        },

        pageChange: function () {
            setTimeout(() => {
                this.getList();
            })
        },
        activated() {
          this.activeName = 'members'
        },
        created: function () {
            let nowDate = new Date();
            let nowDateDetail = this.pbFunc.getDateDetail(nowDate);
            let nowDateStr = nowDateDetail.year + '-' + nowDateDetail.month + '-' + nowDateDetail.day + ' ' + nowDateDetail.hour + ':' + nowDateDetail.minute + ':' + nowDateDetail.second;

            this.CreatedTime = ['2019-01-01 08:00:00', nowDateStr];
            this.searchPostData = this.pbFunc.deepcopy(this.searchFilters);
            console.log('xxxxxx', this.searchPostData)
            this.getList();
        }
    }
</script>
