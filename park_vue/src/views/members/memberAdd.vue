<style scoped lang="less">
</style>

<template>
    <div>
        <el-form class="tms-dialog-content" label-width="110px" :rules="rules" :model="formRules" status-icon
                 ref="formRules">
            <el-row :gutter="40">
                <el-col :span="10">
                    <el-form-item label="会员姓名:" prop="username">
                        <el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.username"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="10">
                    <el-form-item label="会员电话:" prop="phone">
                        <el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.phone"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="10">
                    <el-form-item label="身份证号码:" prop="identity_card">
                        <el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.identity_card"></el-input>
                    </el-form-item>
                </el-col>

                <el-col :span="10">
                    <el-form-item label="车牌号码:" prop="plate_number">
                        <el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.plate_number"></el-input>
                    </el-form-item>
                </el-col>

                <el-col :span="10">
                    <el-form-item label="车位号:" prop="postion_id">
                        <el-select v-model="formRules.postion_id" :loading="supplierLoading" clearable
                                   placeholder="请输入选择" :disabled="isDisabled || isUpdate">
                            <el-option v-for="(item,key) in PostionListSelect" :key="key" :label="item.id"
                                       :value="item.id"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="10">
                    <el-form-item label="会员类型:" prop="member_type">
                        <el-select v-model="formRules.member_type" filterable placeholder="请输入选择"
                                   :disabled="isDisabled">
                            <el-option v-for="item in MemberTypeSelect" :key="item.id" :label="item.name"
                                       :value="item.id"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="10">
                    <el-form-item label="车辆类型:" prop="type">
                        <el-select v-model="formRules.type" placeholder="请输入选择" :disabled="isDisabled">
                            <el-option v-for="item in CarTypeSelect" :key="item.id" :label="item.name"
                                       :value="item.id"></el-option>
                        </el-select>
                    </el-form-item>
                </el-col>

                <el-col :span="10">
                    <el-form-item label="车辆颜色:" prop="color">
                        <el-input placeholder="请输入车辆颜色" :disabled="isDisabled" v-model="formRules.color"></el-input>
                    </el-form-item>
                </el-col>

                <el-col :span="16" :offset="11">
                    <!--<el-button @click="closeBtn">取消</el-button>-->
                    <el-button type="primary" @click="adjustBtn" :loading="submitBtn.isLoading"
                               :disabled="submitBtn.isDisabled">{{submitBtn.btnText}}
                    </el-button>
                </el-col>
            </el-row>
        </el-form>
    </div>
</template>
<script>
    export default {
        name: 'carpostionList',
        // props: {
        //     arapDialog: {
        //         type: Object,
        //         required: true
        //     },
        //     closeDialogBtn: Function,
        //     arapRow: {
        //         type: Object,
        //         required: true
        //     },
        // },
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
                pageLoading: false,
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
                PostionListSelect: [], //车牌号列表
                supplierLoading: false,
                differenceValue: { //差价
                    active_tonnage: '', //实际装车吨位
                    unit_price: '' //单价
                },
                title: '新增会员'
            }
        },
        computed: {
            activeStep: function () {
                return 0;
            },
        },
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
                this.$$http('list_car_postions', postData).then((results) => {
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
                        };
                        let postData = this.formRules;
                        this.$$http('add_members', postData).then((results) => {
                            this.submitBtn = {
                                btnText: '保存',
                                isDisabled: false,
                                isLoading: false
                            }
                            if (results.data && results.data.code == 0) {
                                this.$message({
                                    // message: this.arapDialog.type === 'add' ? '新增成功' : '修改成功',
                                    message: '新增成功',
                                    type: 'success'
                                });
                                console.log('--1111111')
                                this.$router.push({ path: "/people" });
                                // this.$emit('closeDialogBtn', true);
                            }
                            if (results.data.code == -1) {
                                this.$alert(results.data.msg)
                            } else {
                                console.log('22222222')
                                reject(results);
                            }
                        }).catch((err) => {
                            console.log('3333333333');
                            this.submitBtn = {
                                btnText: '保存',
                                isDisabled: false,
                                isLoading: false
                            }
                        })
                    } else {
                        console.log('4444444444')
                        this.submitBtn.isDisabled = false;
                    }
                });
            },
        },
        watch: {
            arapDialog(curVal, oldVal) {
                if (curVal.type === 'detail') {
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
