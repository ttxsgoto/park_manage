<style scoped lang="less">
</style>

<template>
    <div>
        <el-form class="tms-dialog-content" label-width="110px" :rules="rules" :model="formRules" status-icon
                 ref="formRules">
            <el-row>
                <el-col :span="10">
                    <el-form-item label="原始密码:" prop="username">
                        <el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.username"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="10">
                    <el-form-item label="新密码:" prop="phone">
                        <el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.phone"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="10">
                    <el-form-item label="确认密码:" prop="identity_card">
                        <el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.identity_card"></el-input>
                    </el-form-item>
                </el-col :span="50">
                    <!-- <el-button @click="closeBtn">取消</el-button>-->
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
            }
        },
        computed: {
            activeStep: function () {
                return 0;
            },
            peopleId: function () {
                return this.$route.params.id;
            }
        },
        methods: {
            closeBtn: function () {
                this.$emit('closeDialogBtn', false);
            },
            getSupplier: function () {
                this.supplierLoading = true;
                this.$$http01('list_members_detail', {id: this.peopleId}).then((results) => {
                    this.supplierLoading = false;
                    if (results.data && results.data.code == 0) {
                        this.formRules = results.data.data;
                        this.isUpdate = true;
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
                        postData.id = this.peopleId;
                        this.$$http01('update_members', postData).then((results) => {
                            this.submitBtn = {
                                btnText: '保存',
                                isDisabled: false,
                                isLoading: false
                            };
                            if (results.data && results.data.code == 0) {
                                this.$message({
                                    message: '修改成功',
                                    type: 'success'
                                });
                                this.$router.push({path: "/people"});
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
                        })
                    } else {
                        this.submitBtn.isDisabled = false;
                    }
                });
            },
        },
        watch: {},
        created: function () {
            this.pbFunc.format();
            this.getSupplier();
        }
    }
</script>
