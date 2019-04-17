<style scoped lang="less">
</style>
<template>
    <div>
        <el-dialog :title="title" :visible="arapDialog.isShow" width="30%" center :before-close="closeBtn"
                   :close-on-click-modal="false">
            <div class="tms-dialog-form">
                <!--<el-form class="tms-dialog-content" label-width="110px" :rules="rules" :model="formRules" status-icon-->
                <el-form class="tms-dialog-content" label-width="110px" :model="detailData" status-icon
                         ref="detailData">
                    <el-form-item label="车位号:" prop="detailData.arapData.id">
                        <el-input placeholder="无" :disabled="isDisabled"  v-model="detailData.arapData.id"></el-input>
                    </el-form-item>
                    <el-form-item label="车牌号:" prop="detailData.arapData.plate_number">
                        <el-input placeholder="无" :disabled="isDisabled" v-model="detailData.arapData.plate_number"></el-input>
                    </el-form-item>
                    <el-form-item label="可使用:" prop="detailData.arapData.is_valid_ch">
                        <el-input placeholder="无" :disabled="isDisabled" v-model="detailData.arapData.is_valid_ch" ></el-input>
                    </el-form-item>
                    <el-form-item label="会员位:" prop="detailData.arapData.is_member_ch">
                        <el-input placeholder="无" :disabled="isDisabled" v-model="detailData.arapData.is_member_ch" ></el-input>
                    </el-form-item>
                    <el-form-item label="会员姓名:" prop="detailData.arapData.member">
                        <el-input placeholder="无" :disabled="isDisabled" v-model="detailData.arapData.member.username" ></el-input>
                    </el-form-item>
                    <el-form-item label="会员电话:" prop="detailData.arapData.member">
                        <el-input placeholder="无" :disabled="isDisabled" v-model="detailData.arapData.member.phone" ></el-input>
                    </el-form-item>
                    <el-form-item label="到期时间:" prop="detailData.arapData.member">
                        <el-input placeholder="无" :disabled="isDisabled" v-model="detailData.arapData.member.expire_time" ></el-input>
                    </el-form-item>
                    <el-form-item label="添加人员:" prop="detailData.arapData.member">
                        <el-input placeholder="无" :disabled="isDisabled" v-model="detailData.arapData.member.creator_name" ></el-input>
                    </el-form-item>
                </el-form>
            </div>
            <span slot="footer" class="dialog-footer">
        <el-button @click="closeBtn">取消</el-button>
      </span>
        </el-dialog>
    </div>
</template>
<script>
    export default {
        name: 'PostionDetailDialog',
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
                isDisabled: true,
                detailData: {
                    arapData:{}
                },
                submitBtn: {
                    btnText: '保存',
                    isDisabled: false,
                    isLoading: false
                },
                title: '车位详情'
            }
        },
        computed: {},
        methods: {
            closeBtn: function () {
                this.$emit('closeDialogBtn', false);
            },
            adjustBtn: function () {
                this.$emit('closeDialogBtn', true);
            },
        },
        watch: {
            arapDialog(curVal, oldVal) {
                if (curVal.type === 'update') {
                    console.log('-------->', this.arapRow)
                    this.detailData.arapData = this.arapRow
                } else {
                    this.title = '新增打款事项';
                }
                // if (this.$refs['formRules']) {
                //     this.$refs['formRules'].clearValidate();
                // }

            },
        },
        created: function () {
            this.pbFunc.format();
            // this.getSupplier();
        }
    }

</script>
