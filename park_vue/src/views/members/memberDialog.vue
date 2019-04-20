<style scoped lang="less">
</style>
<template>
    <div>
        <el-dialog :title="title" :visible="arapDialog.isShow" width="30%" center :before-close="closeBtn"
                   :close-on-click-modal="false">
            <div class="tms-dialog-form">
                <el-form class="tms-dialog-content" label-width="110px" :rules="rules" :model="formRules" status-icon
                         ref="formRules">
                    <el-form-item label="会员姓名:" prop="username">
                        <el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.username"></el-input>
                    </el-form-item>

                    <el-form-item label="会员电话:" prop="phone">
                        <el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.phone"></el-input>
                    </el-form-item>

                    <el-form-item label="身份证号码:" prop="identity_card">
                        <el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.identity_card"></el-input>
                    </el-form-item>

                    <el-form-item label="车牌号码:" prop="plate_number">
                        <el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.plate_number"></el-input>
                    </el-form-item>

                    <el-form-item label="车位号:" prop="postion_id">
                        <el-select v-model="formRules.postion_id" :loading="supplierLoading" clearable
                                   placeholder="请输入选择" :disabled="isDisabled || isUpdate">
                            <el-option v-for="(item,key) in PostionListSelect" :key="key" :label="item.id"
                                       :value="item.id"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="会员类型:" prop="member_type">
                        <el-select v-model="formRules.member_type" filterable placeholder="请输入选择"
                                   :disabled="isDisabled">
                            <el-option v-for="item in MemberTypeSelect" :key="item.id" :label="item.name"
                                       :value="item.id"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="车辆类型:" prop="type">
                        <el-select v-model="formRules.type" placeholder="请输入选择" :disabled="isDisabled">
                            <el-option v-for="item in CarTypeSelect" :key="item.id" :label="item.name"
                                       :value="item.id"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="车辆颜色:" prop="color">
                        <el-input placeholder="请输入车辆颜色" :disabled="isDisabled" v-model="formRules.color"></el-input>
                    </el-form-item>


                    <!--<el-form-item label="付款日期:" prop="payment_datetime">-->
                    <!--<el-date-picker v-model="formRules.payment_datetime" :picker-options="pickerOptionsDate" type="date" placeholder="选择日期" value-format="yyyy-MM-dd hh:mm:ss"></el-date-picker>-->
                    <!--</el-form-item>-->
                    <!--<el-form-item label="付款金额:" prop="amount">-->
                    <!--<el-input placeholder="请输入" v-model="formRules.amount"></el-input>-->
                    <!--</el-form-item>-->
                    <!--<el-form-item label="备注:" prop="desc">-->
                    <!--<el-input placeholder="请输入" type="textarea" resize="none" :rows="3" v-model="formRules.desc"></el-input>-->
                    <!--</el-form-item>-->
                </el-form>
            </div>
            <span slot="footer" class="dialog-footer">
        <el-button @click="closeBtn">取消</el-button>
                <span v-show="!isDetail">
        <el-button type="primary" @click="adjustBtn" :loading="submitBtn.isLoading" :disabled="submitBtn.isDisabled">{{submitBtn.btnText}}</el-button>
                </span>
      </span>
        </el-dialog>
    </div>
</template>
<script>
    export default {
        name: 'carpostionList',
        props: {
            arapDialog: {
                type: Object,
                required: true
            },
            closeDialogBtn: Function,
            arapRow: {
                type: Object,
                required: true
            },
        },
        data: function () {
            return {
                formRules: {
                    username: '',
                    phone: '',
                    identity_card: '',
                    plate_number: '',
                    postion_id: '',
                    member_type: '',
                    type: '',
                    color: ''
                },
                isDisabled: false,
                isDetail: false,
                isUpdate: false,
                MemberTypeSelect: [
                    {id: 'quarter', name: '包季'},
                    {id: 'year', name: '包年'},
                ],
                CarTypeSelect: [
                    {id: 1, name: '轿车'},
                    {id: 2, name: 'SUV'},
                    {id: 3, name: 'MPV'},
                    {id: 4, name: '跑车'},
                    {id: 5, name: '皮卡'},
                    {id: 6, name: '微面'},
                ],
                rules: {
                    username: [
                        {required: true, message: '请输入会员姓名', trigger: 'blur'},
                    ],
                    phone: [
                        {required: true, message: '请输入会员电话', trigger: 'blur'},
                        {min: 11, max: 12, message: '必须为11位电话号码', trigger: 'blur'}
                    ],
                    identity_card: [
                        {required: true, message: '请输入18位身份证号码', trigger: 'blur'},
                        {min: 18, max: 18, message: '必须为18位身份证号码', trigger: 'blur'}
                    ],
                    plate_number: [
                        {required: true, message: '请输入车牌号码', trigger: 'blur'}
                    ],
                    member_type: [
                        {required: true, message: '请选择会员类型', trigger: 'blur'},
                    ],
                    postion_id: [
                        {type: 'number', required: true, message: '请选择车位号', trigger: 'blur'},
                    ],
                    type: [
                        {type: 'number', required: true, message: '请选择车辆类型', trigger: 'blur'},
                    ],
                },
                submitBtn: {
                    btnText: '保存',
                    isDisabled: false,
                    isLoading: false
                },
                PostionListSelect: [], //供应商列表
                supplierLoading: false,
                differenceValue: { //差价
                    active_tonnage: '', //实际装车吨位
                    unit_price: '' //单价
                },
                title: '新增会员'

            }
        },
        computed: {},
        methods: {
            closeBtn: function () {
                this.$emit('closeDialogBtn', false);
            },
            getSupplier: function () {
                let postData = {
                    page: 1,
                    page_size: 200,
                    is_valid: 'True'
                }
                this.supplierLoading = true;
                this.$$http01('list_car_postions', postData).then((results) => {
                    this.supplierLoading = false;
                    if (results.data && results.data.code == 0) {
                        this.PostionListSelect = results.data.data.data;
                    }
                }).catch((err) => {
                    this.supplierLoading = false;
                })
            },

            adjustBtn: function () {
                this.$refs['formRules'].validate((valid) => {
                    if (valid) {
                        this.submitBtn = {
                            btnText: '保存中',
                            isDisabled: true,
                            isLoading: true
                        }
                        let postData = this.formRules;
                        let apiName = 'add_members';
                        if (this.arapDialog.type === 'update') {
                            postData.id = this.arapRow.id;
                            apiName = 'update_members';
                        } else if (this.arapDialog.type == 'detail') {
                            this.submitBtn = {
                                btnText: '保存',
                                isDisabled: false,
                                isLoading: false
                            }
                        } else {
                            apiName = 'add_members';
                        }
                        this.$$http01(apiName, postData).then((results) => {
                            this.submitBtn = {
                                btnText: '保存',
                                isDisabled: false,
                                isLoading: false
                            }
                            if (results.data && results.data.code == 0) {
                                this.$message({
                                    message: this.arapDialog.type === 'add' ? '新增成功' : '修改成功',
                                    type: 'success'
                                });
                                this.$emit('closeDialogBtn', true);
                            }
                            if (results.data.code == -1) {
                                this.$alert(results.data.msg)
                            } else {
                                reject(results);
                            }

                        }).catch((err) => {
                            this.submitBtn = {
                                btnText: '保存',
                                isDisabled: false,
                                isLoading: false
                            }
                            this.$message.error(this.arapDialog.type === 'add' ? '新增失败' : '修改失败');
                        })

                    } else {
                        this.submitBtn.isDisabled = false;
                    }
                });
            },
        },
        watch: {
            arapDialog(curVal, oldVal) {
                // this.formRules = {
                //     supplier: '', //供应商
                //     payment_datetime: '', //付款日期
                //     amount: '', //付款金额
                //     desc: '', //调账备注
                // };
                if (curVal.type === 'detail') {
                    // this.formRules = {
                    //     supplier: this.arapRow.supplier, //供应商
                    //     payment_datetime: this.arapRow.payment_datetime, //付款日期
                    //     amount: this.arapRow.amount, //付款金额
                    //     desc: this.arapRow.desc, //调账备注
                    // };
                    this.isDisabled = true;
                    this.isDetail = true;
                    this.formRules = this.arapRow;
                    this.title = '会员信息';
                } else if (curVal.type == 'update') {
                    this.isDisabled = false;
                    this.isDetail = false;
                    this.isUpdate = true;
                    this.formRules = this.arapRow;
                    this.title = '修改会员信息';
                } else {
                    this.isDisabled = false;
                    this.isDetail = false;
                    this.isUpdate = false;
                    this.formRules = {};
                    this.title = '新增会员信息';
                }
                if (this.$refs['formRules']) {
                    this.$refs['formRules'].clearValidate();
                }

            },
        },
        created: function () {
            this.pbFunc.format();
            this.getSupplier();
        }
    }

</script>
