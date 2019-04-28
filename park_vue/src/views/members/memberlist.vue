<style scoped lang="less">
</style>
<template>
    <div>
        <div class="nav-tab">
            <el-tabs v-model="activeName" type="card">
                <el-tab-pane label="会员管理" name="members"></el-tab-pane>
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
                    </el-form>
                </div>
                <el-tab-pane label="费用管理" name="payment">

                </el-tab-pane>
                <div class="operation-btn text-right" style="border:5px;text-align:right;float:right">
                    <el-button type="primary" @click="arapDialogEdit('add')">新增</el-button>
                    <el-button type="danger" @click="handleDel(multiSelectString)">删除</el-button>
                </div>
                <div class="table-list">
                    <el-table :data="tableData" stripe style="width: 100%" size="mini" max-height="600"
                              v-loading="pageLoading" :class="{'tabal-height-500':!tableData.length}"
                              @selection-change="handleSelectionChange"
                    >
                        <el-table-column
                                type="selection"
                                width="55">
                        </el-table-column>
                        <el-table-column v-for="(item,key) in thTableList" :key="key" :prop="item.param"
                                         align="center" :label="item.title" :width="item.width">
                        </el-table-column>
                        <el-table-column label="操作" align="center">
                            <template scope="scope">
                                <el-button type="primary" size="mini" @click="arapDialogEdit('update',scope.row)">
                                    修改
                                </el-button>
                                <el-button type="primary" size="mini" @click="arapDialogEdit('detail',scope.row)">
                                    详情
                                </el-button>
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
            </el-tabs>
        </div>
        <member-add :arap-dialog="arapDialog" v-on:closeDialogBtn="closeDialog"
                    :arap-row="arapRow"></member-add>
    </div>
</template>
<script>
    import MemberAdd from './memberDialog';

    export default {
        name: 'carpostionList',
        components: {
            MemberAdd: MemberAdd
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
                multipleSelection: [],
                multiSelectString: '',
                searchFilters: {
                    is_valid: this.$route.query.is_valid ? this.$route.query.is_valid : '',
                    is_member: this.$route.query.is_member ? this.$route.query.is_member : '',
                    keyword: '',
                    field: 'username',
                },
                payerTime: [], //付款时间
                selectData: {
                    fieldSelect: [
                        {id: 'username', value: '会员姓名'},
                        {id: 'plate_number', value: '车牌号'}
                    ],
                    isValidSelect: [
                        {id: '', value: '全部'},
                        {id: 'True', value: '未使用'},
                        {id: 'False', value: '已使用'},
                    ],
                    isMemberSelect: [
                        {id: '', value: '全部'},
                        {id: 'True', value: '是'},
                        {id: 'False', value: '否'}
                    ],
                },
                thTableList: [{
                    title: '会员姓名',
                    param: 'username',
                    width: '100'
                }, {
                    title: '会员电话',
                    param: 'phone',
                    width: '200'
                }, {
                    title: '身份证号码',
                    param: 'identity_card',
                    width: '100'
                }, {
                    title: '车牌号码',
                    param: 'plate_number',
                    width: '100'
                }, {
                    title: '会员类型',
                    param: 'member_type_ch',
                    width: '100'
                }, {
                    title: '车辆类型',
                    param: 'type_ch',
                    width: '100'
                }, {
                    title: '颜色',
                    param: 'color',
                    width: '100'
                }, {
                    title: '车位号',
                    param: 'postion_id',
                    width: '100'
                }, {
                    title: '生效时间',
                    param: 'created_time',
                    width: '200'
                }, {
                    title: '到期时间',
                    param: 'expire_time',
                    width: '200'
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
                        this.$$http01('del_members', {id: id}).then((results) => {
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
                this.$$http01('list_members', postData).then((results) => {
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
        pageChange: function () {
            setTimeout(() => {
                this.getList();
            })
        },
        created: function () {
            this.getList();
        }
    }
</script>
