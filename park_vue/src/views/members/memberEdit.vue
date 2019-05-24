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
                this.$$http('list_members_detail', {id: this.peopleId}).then((results) => {
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
                        this.$$http('update_members', postData).then((results) => {
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
