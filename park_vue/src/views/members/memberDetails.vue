<style scoped lang="less">
</style>

<template>
    <!--输入框形式-->
    <!--<div>-->
    <!--<el-form class="tms-dialog-content" label-width="110px" :rules="rules" :model="formRules" status-icon-->
    <!--ref="formRules">-->
    <!--<el-row :gutter="40">-->
    <!--<el-col :span="10">-->
    <!--<el-form-item label="会员姓名:" prop="username">-->
    <!--<el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.username"></el-input>-->
    <!--</el-form-item>-->
    <!--</el-col>-->
    <!--<el-col :span="10">-->
    <!--<el-form-item label="会员电话:" prop="phone">-->
    <!--<el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.phone"></el-input>-->
    <!--</el-form-item>-->
    <!--</el-col>-->
    <!--<el-col :span="10">-->
    <!--<el-form-item label="身份证号码:" prop="identity_card">-->
    <!--<el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.identity_card"></el-input>-->
    <!--</el-form-item>-->
    <!--</el-col>-->

    <!--<el-col :span="10">-->
    <!--<el-form-item label="车牌号码:" prop="plate_number">-->
    <!--<el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.plate_number"></el-input>-->
    <!--</el-form-item>-->
    <!--</el-col>-->

    <!--<el-col :span="10">-->
    <!--<el-form-item label="车位号:" prop="postion_id">-->
    <!--<el-select v-model="formRules.postion_id" :loading="supplierLoading" clearable-->
    <!--placeholder="请输入选择" :disabled="isDisabled">-->
    <!--<el-option v-for="(item,key) in PostionListSelect" :key="key" :label="item.id"-->
    <!--:value="item.id"></el-option>-->
    <!--</el-select>-->
    <!--</el-form-item>-->
    <!--</el-col>-->
    <!--<el-col :span="10">-->
    <!--<el-form-item label="会员类型:" prop="member_type">-->
    <!--<el-select v-model="formRules.member_type" filterable placeholder="请输入选择"-->
    <!--:disabled="isDisabled">-->
    <!--<el-option v-for="item in MemberTypeSelect" :key="item.id" :label="item.name"-->
    <!--:value="item.id"></el-option>-->
    <!--</el-select>-->
    <!--</el-form-item>-->
    <!--</el-col>-->
    <!--<el-col :span="10">-->
    <!--<el-form-item label="车辆类型:" prop="type">-->
    <!--<el-select v-model="formRules.type" placeholder="请输入选择" :disabled="isDisabled">-->
    <!--<el-option v-for="item in CarTypeSelect" :key="item.id" :label="item.name"-->
    <!--:value="item.id"></el-option>-->
    <!--</el-select>-->
    <!--</el-form-item>-->
    <!--</el-col>-->

    <!--<el-col :span="10">-->
    <!--<el-form-item label="车辆颜色:" prop="color">-->
    <!--<el-input placeholder="请输入车辆颜色" :disabled="isDisabled" v-model="formRules.color"></el-input>-->
    <!--</el-form-item>-->
    <!--</el-col>-->
    <!--&lt;!&ndash;<el-col :span="16" :offset="11">&ndash;&gt;-->
    <!--&lt;!&ndash;&lt;!&ndash;<el-button @click="closeBtn">取消</el-button>&ndash;&gt;&ndash;&gt;-->
    <!--&lt;!&ndash;<el-button type="primary" @click="adjustBtn" :loading="submitBtn.isLoading"&ndash;&gt;-->
    <!--&lt;!&ndash;:disabled="submitBtn.isDisabled">{{submitBtn.btnText}}&ndash;&gt;-->
    <!--&lt;!&ndash;</el-button>&ndash;&gt;-->
    <!--&lt;!&ndash;</el-col>&ndash;&gt;-->
    <!--</el-row>-->
    <!--</el-form>-->
    <!--</div>-->
    <!--输入框形式 end-->

    <div>
        <!--<el-container>-->
        <!--<el-header>-->
        <!--<el-row>-->
        <!--<el-col :span="3">-->
        <!--<router-link :to="{path: '/basicDataManage/customerManage/customerPayManageAll'}">-->
        <!--<div class="go-return icon-back"></div>-->
        <!--</router-link>-->
        <!--</el-col>-->
        <!--<el-col :span="18">-->
        <!--<p>客户详情</p>-->
        <!--</el-col>-->
        <!--</el-row>-->
        <!--</el-header>-->
        <!--</el-container>-->
        <el-main>
            <div>
                <el-form class="addheaduserform" label-width="145px" :model="formRules" status-icon>
                    <el-row :gutter="40">
                        <el-col :span="10">
                            <el-form-item label="会员姓名:">
                                <div class="detail-form-item whiteSpan">{{formRules.username}}</div>
                            </el-form-item>
                        </el-col>

                        <el-col :span="10">
                            <el-form-item label="会员电话:" prop="phone">
                                <div class="detail-form-item whiteSpan">{{formRules.phone}}</div>
                            </el-form-item>
                        </el-col>

                        <el-col :span="10">
                            <el-form-item label="身份证号码:" prop="identity_card">
                                <div class="detail-form-item whiteSpan">{{formRules.identity_card}}</div>
                            </el-form-item>
                        </el-col>

                        <el-col :span="10">
                            <el-form-item label="车牌号码:" prop="plate_number">
                                <div class="detail-form-item whiteSpan">{{formRules.plate_number}}</div>
                            </el-form-item>
                        </el-col>

                        <el-col :span="10">
                            <el-form-item label="车位号:" prop="postion_id">
                                <div class="detail-form-item whiteSpan">{{formRules.postion_id}}</div>
                            </el-form-item>
                        </el-col>

                        <el-col :span="10">
                            <el-form-item label="会员类型:" prop="member_type">
                                <div class="detail-form-item whiteSpan">{{formRules.member_type}}</div>
                            </el-form-item>
                        </el-col>

                        <el-col :span="10">
                            <el-form-item label="车辆类型:" prop="type">
                                <div class="detail-form-item whiteSpan">{{formRules.type}}</div>
                            </el-form-item>
                        </el-col>

                        <el-col :span="10">
                            <el-form-item label="车辆颜色:" prop="color">
                                <div class="detail-form-item whiteSpan">{{formRules.color}}</div>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
            </div>
        </el-main>

    </div>

</template>
<script>
    export default {
        name: 'memberDetail',
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
            }
        },
        computed: {
            peopleId: function () {
                return this.$route.params.id;
            }
        },
        methods: {
            getSupplier: function () {
                this.submitBtn = {
                    btnText: '保存',
                    isDisabled: true,
                    isLoading: false
                }
                this.supplierLoading = true;

                this.$$http('list_members_detail', {id: this.peopleId}).then((results) => {
                    this.supplierLoading = false;
                    if (results.data && results.data.code == 0) {
                        this.formRules = results.data.data;
                        this.isDisabled = true;
                    }
                }).catch((err) => {
                    this.supplierLoading = false;
                })
            },
        },
        created: function () {
            this.pbFunc.format();
            this.getSupplier();
        }
    }
</script>
