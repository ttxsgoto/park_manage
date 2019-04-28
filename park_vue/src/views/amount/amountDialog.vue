<style scoped lang="less">
</style>
<template>
    <div>
        <el-dialog :title="title" :visible="arapDialog.isShow" width="30%" center :before-close="closeBtn"
                   :close-on-click-modal="false">
            <div class="tms-dialog-form">
                <el-form class="tms-dialog-content" label-width="110px" :rules="rules" :model="formRules" status-icon
                         ref="formRules">
                    <el-form-item label="车牌号码:" prop="plate_number">
                        <el-input placeholder="请输入" :disabled="isDisabled" v-model="formRules.plate_number"></el-input>
                    </el-form-item>
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
        name: 'AmountDialog',
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
                    plate_number: '',
                },
                isDisabled: false,
                isDetail: false,
                isUpdate: false,
                amount: 0.0,
                is_member: '',
                rules: {
                    plate_number: [
                        {required: true, message: '请输入车牌号码', trigger: 'blur'}
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
                title: '进入车辆车牌号码'
            }
        },
        computed: {},
        methods: {
            closeBtn: function () {
                this.$emit('closeDialogBtn', false);
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
                        let apiName = 'come_in_park';
                        if (this.arapDialog.type === 'add') {
                            apiName = 'come_in_park';
                        } else {
                            apiName = 'come_out_park';
                        }
                        this.$$http01(apiName, postData).then((results) => {
                            this.submitBtn = {
                                btnText: '保存',
                                isDisabled: false,
                                isLoading: false
                            };
                            if (results.data && results.data.code == 0) {
                                this.amount = results.data.amount;
                                // this.is_member =
                                this.is_member = results.data.is_member === true ? '是' : '否';
                                // console.log('本次停车费用: ' + this.amount + '; 会员: ' + this.is_member),
                                this.$message({
                                    message: this.arapDialog.type === 'add' ? '新增成功' : '离开成功',
                                    type: 'success'
                                });
                                if (this.arapDialog.type === 'del') {
                                    this.$message({
                                        message: '本次停车费用: ' + this.amount + '; 会员: ' + this.is_member,
                                        type: 'success',
                                        showClose: true
                                    });
                                }
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
                        })
                    } else {
                        this.submitBtn.isDisabled = false;
                    }
                });
            },
        },
        watch: {
            arapDialog(curVal, oldVal) {
                if (curVal.type === 'del') {
                    this.isDisabled = false;
                    this.isDetail = false;
                    this.isUpdate = false;
                    this.title = '离开车辆车牌号码';
                } else {
                    this.isDisabled = false;
                    this.isDetail = false;
                    this.isUpdate = false;
                    this.formRules = {};
                    this.title = '进入车辆车牌号码';
                }
                // if (this.$refs['formRules']) {
                //     this.$refs['formRules'].clearValidate();
                // }
            },
        },
        created: function () {
            this.pbFunc.format();
        }
    }
</script>
