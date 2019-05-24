<style scoped lang="less">
</style>

<template>
    <div>
        <el-form class="tms-dialog-conten" label-width="110px" :rules="rules" :model="formRules" status-icon
                 ref="formRules">
            <el-row>
                <el-col :span="15">
                    <el-form-item v-if="visible" label="原始密码:" prop="old_pwd">
                        <el-input placeholder="请输入" type="password" :disabled="isDisabled" v-model="formRules.old_pwd"
                        style="width: 300px;">
                        <i slot="suffix" title="隐藏密码" @click="changePass('show')" style="cursor:pointer;"
                          class="iconfont icon-xianshizy"></i>
                        </el-input>
                    </el-form-item>
                    <el-form-item v-else label="原始密码:"  class="is-required" prop="old_pwd">
                        <el-input placeholder="请输入" type="text" :disabled="isDisabled" v-model="formRules.old_pwd"
                        style="width: 300px;">
                        <!-- <i slot="suffix" class="el-icon-view" @click="showPwd"></i> -->
                        <i slot="suffix" title="隐藏密码" @click="changePass('hide')" style="cursor:pointer;"
                          class="iconfont icon-yincangby"></i>
                        </el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="15">
                    <el-form-item label="新密码:" prop="new_pwd">
                        <el-input placeholder="请输入" type="password" :disabled="isDisabled" v-model="formRules.new_pwd"
                        style="width: 300px;">
                        </el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="15">
                    <el-form-item label="确认密码:"  prop="sure_pwd" size="small">
                        <el-input placeholder="请输入" type="password" :disabled="isDisabled" v-model="formRules.sure_pwd"
                        style="width: 300px;">
                        </el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="15" >
                  <el-form-item>
                      <!-- <el-button @click="closeBtn">取消</el-button>-->
                      <el-button type="primary" @click="adjustBtn" :loading="submitBtn.isLoading"
                                 :disabled="submitBtn.isDisabled">{{submitBtn.btnText}}
                      </el-button>
                  </el-form-item>
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
                    old_pwd: '',
                    new_pwd: '',
                    sure_pwd: '',
                },
                visible: true,
                pageLoading: false,
                isDisabled: false,
                isDetail: false,
                isUpdate: false,
                rules: {
                    old_pwd: [
                        {required: true, message: '请输入原密码', trigger: 'blur'},
                    ],
                    new_pwd: [
                        {required: true, message: '请输入新密码', trigger: 'blur'},
                        {min: 6, max: 18, message: '密码最小长度大于6位', trigger: 'blur'}
                    ],
                    sure_pwd: [
                        {required: true, message: '请确认密码', trigger: 'blur'},
                        {min: 6, max: 18, message: '密码最小长度大于6位', trigger: 'blur'}
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
            changePass(value) {
              this.visible = !(value === 'show');
            },    //判断渲染，true:暗文显示，false:明文显示
            showPwd () {
              this.pwdType === 'password' ? this.pwdType = '' : this.pwdType = 'password';
              let e = document.getElementsByClassName('el-icon-view')[0];
              this.pwdType == '' ? e.setAttribute('style', 'color: #409EFF') : e.setAttribute('style', 'color: #c0c4cc');
            },
            // getSupplier: function () {
            //     this.supplierLoading = true;
            //     this.$$http('list_members_detail', {id: this.peopleId}).then((results) => {
            //         this.supplierLoading = false;
            //         if (results.data && results.data.code == 0) {
            //             this.formRules = results.data.data;
            //             this.isUpdate = true;
            //         }
            //     }).catch((err) => {
            //         this.supplierLoading = false;
            //     })
            // },
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
            // this.getSupplier();
        }
    }
</script>
