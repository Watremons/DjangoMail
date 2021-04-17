<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 配置管理
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <el-row>
            <el-col :span="12">
                <div class="container">
                    <!-- <div class="form-box"> -->
                        <el-form ref="form" :model="form" label-width="120px" label-position="top">
                            <el-form-item label="邮箱域名" size="small">
                                <el-input
                                v-model="form.name"
                                clearable
                                placeholder="请输入邮箱域名"
                                ></el-input>
                            </el-form-item>
                            <el-form-item label="邮件最大长度">
                                <el-input
                                v-model="form.mailMaxLength"
                                clearable
                                placeholder="请输入邮件最大长度"
                                ></el-input>
                            </el-form-item>
                            <el-form-item label="日志最大长度">
                                <el-input
                                v-model="form.logMaxLength"
                                clearable
                                placeholder="请输入日志最大长度"
                                ></el-input>
                            </el-form-item>
                            <el-form-item label="SMTP监听端口">
                                <el-input
                                v-model="form.smtpPort"
                                clearable
                                placeholder="请输入SMTP监听端口"
                                minlength="4"
                                maxlength="4"
                                show-word-limit
                                ></el-input>
                            </el-form-item>

                            <el-form-item label="POP3监听端口">
                                <el-input
                                v-model="form.pop3Port"
                                clearable
                                placeholder="请输入POP3监听端口"
                                minlength="4"
                                maxlength="4"
                                show-word-limit
                                ></el-input>
                            </el-form-item>

                            <el-form-item label="请输入SMTP服务屏蔽IP">
                                <el-input
                                type="textarea"
                                rows="5"
                                v-model="form.desc"
                                autosize
                                ></el-input>
                            </el-form-item>

                            <el-form-item label="请输入SMTP服务屏蔽用户">
                                <el-input
                                type="textarea"
                                rows="5"
                                v-model="form.desc"
                                autosize
                                ></el-input>
                            </el-form-item>

                            <el-form-item label="请输入POP3服务屏蔽IP">
                                <el-input
                                type="textarea"
                                rows="5"
                                v-model="form.desc"
                                autosize
                                ></el-input>
                            </el-form-item>

                            <el-form-item label="请输入POP3服务屏蔽用户">
                                <el-input
                                type="textarea"
                                rows="5"
                                v-model="form.desc"
                                autosize
                                ></el-input>
                            </el-form-item>


                            <el-form-item>
                                <el-button type="primary" @click="onSubmit">表单提交</el-button>
                                <el-button>取消</el-button>
                            </el-form-item>
                        </el-form>
                    <!-- </div> -->
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default {
    name: 'baseform',
    data() {
        return {
            form: {
                name: '',
                mailMaxLength: '',
                logMaxLength: '',
                smtpPort: '',
                pop3Port: '',
                delivery: true,
                type: ['步步高'],
                resource: '小天才',
                desc: '',
                options: []
            }
        };
    },
    methods: {
        onSubmit() {
            this.$message.success('提交成功！');
        }
    }
};
</script>