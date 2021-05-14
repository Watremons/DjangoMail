<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 配置管理
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <el-row :gutter="20">
            <el-col :span="12">
                <div class="container">
                    <!-- <div class="form-box"> -->
                        <el-form
                            ref="configForm"
                            :model="configForm"
                            label-width="120px"
                            label-position="left"
                            @submit.native.prevent
                        >
                            <el-form-item label="邮箱域名" size="small">
                                <el-input
                                v-model="configForm.server.domain"
                                clearable
                                placeholder="请输入邮箱域名"
                                ></el-input>
                            </el-form-item>
                            <el-form-item label="邮件最大长度">
                                <el-input
                                v-model="configForm.server.mailMaxSize"
                                clearable
                                placeholder="请输入邮件最大长度"
                                ></el-input>
                            </el-form-item>
                            <el-form-item label="日志最大长度">
                                <el-input
                                v-model="configForm.server.logMaxSize"
                                clearable
                                placeholder="请输入日志最大长度"
                                ></el-input>
                            </el-form-item>
                            <el-form-item label="SMTP监听端口">
                                <el-input
                                v-model="configForm.smtp.port"
                                clearable
                                placeholder="请输入SMTP监听端口"
                                minlength="4"
                                maxlength="4"
                                show-word-limit
                                ></el-input>
                            </el-form-item>

                            <el-form-item label="POP3监听端口">
                                <el-input
                                v-model="configForm.pop3.port"
                                clearable
                                placeholder="请输入POP3监听端口"
                                minlength="4"
                                maxlength="4"
                                show-word-limit
                                ></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-button type="danger" @click="resetConfig">重置</el-button>
                                <el-button type="primary" @click="onSubmit">提交</el-button>
                                <el-button>取消</el-button>
                            </el-form-item>
                        </el-form>
                    <!-- </div> -->
                </div>
            </el-col>

            <el-col :span="12">
                <div class="container">
                    SMTP屏蔽管理
                    <el-divider></el-divider>
                    <div class="handle-box">
                        屏蔽IP
                    </div>
                    <el-table
                        :data="smtpbanIP.ipList"
                        border
                        class="table"
                        ref="smtpbanIPTable"
                        header-cell-class-name="table-header"
                        stripe
                    >
                        <el-table-column prop="banIP" label="屏蔽IP" minWidth="80%" align="center"></el-table-column>
                        <el-table-column minWidth="20%" align="center">
                            <template slot="header" slot-scope="scope">
                                <el-button
                                    type="text"
                                    icon="el-icon-edit"
                                    class="green"
                                    @click="handleAdd('添加SMTP屏蔽IP')"
                                >添加屏蔽IP</el-button>
                            </template>
                            <template slot-scope="scope">
                                <el-button
                                    type="text"
                                    icon="el-icon-delete"
                                    class="red"
                                    @click="handleSmtpIpDelete(scope.$index, scope.row)"
                                >删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>

                    <div class="handle-box">
                        屏蔽用户
                    </div>
                    <el-table
                        :data="smtpbanAccount.accountList"
                        border
                        class="table"
                        ref="smtpbanAccountTable"
                        header-cell-class-name="table-header"
                        stripe
                    >
                        <el-table-column prop="banAccount" label="屏蔽用户" minWidth="80%" align="center"></el-table-column>
                        <el-table-column minWidth="20%" align="center">
                            <template slot="header" slot-scope="scope">
                                <el-button
                                    type="text"
                                    icon="el-icon-edit"
                                    class="green"
                                    @click="handleAdd('添加SMTP屏蔽用户')"
                                >添加屏蔽用户</el-button>
                            </template>
                            <template slot-scope="scope">
                                <el-button
                                    type="text"
                                    icon="el-icon-delete"
                                    class="red"
                                    @click="handleSmtpAccountDelete(scope.$index, scope.row)"
                                >删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
                <div class="container">
                    POP3屏蔽管理
                    <el-divider></el-divider>
                    <div class="handle-box">
                        屏蔽IP
                    </div>
                    <el-table
                        :data="pop3banIP.ipList"
                        border
                        class="table"
                        ref="pop3banIPTable"
                        header-cell-class-name="table-header"
                        stripe
                    >
                        <el-table-column prop="banIP" label="屏蔽IP" minWidth="80%" align="center"></el-table-column>
                        <el-table-column minWidth="20%" align="center">
                            <template slot="header" slot-scope="scope">
                                <el-button
                                    type="text"
                                    icon="el-icon-edit"
                                    class="green"
                                    @click="handleAdd('添加POP3屏蔽IP')"
                                >添加屏蔽IP</el-button>
                            </template>
                            <template slot-scope="scope">
                                <el-button
                                    type="text"
                                    icon="el-icon-delete"
                                    class="red"
                                    @click="handlePop3IpDelete(scope.$index, scope.row)"
                                >删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>

                    <div class="handle-box">
                        屏蔽用户
                    </div>
                    <el-table
                        :data="pop3banAccount.accountList"
                        border
                        class="table"
                        ref="smtpbanAccountTable"
                        header-cell-class-name="table-header"
                        stripe
                    >
                        <el-table-column prop="banAccount" label="屏蔽用户" minWidth="80%" align="center"></el-table-column>
                        <el-table-column minWidth="20%" align="center">
                            <template slot="header" slot-scope="scope">
                                <el-button
                                    type="text"
                                    icon="el-icon-edit"
                                    class="green"
                                    @click="handleAdd('添加POP3屏蔽用户')"
                                >添加屏蔽用户</el-button>
                            </template>
                            <template slot-scope="scope">
                                <el-button
                                    type="text"
                                    icon="el-icon-delete"
                                    class="red"
                                    @click="handlePop3AccountDelete(scope.$index, scope.row)"
                                >删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
            </el-col>
        </el-row>

        <!-- 新增信息弹出框 -->
        <el-dialog title="添加" :visible.sync="addVisible" width="30%">
            <el-form
                ref="form"
                :model="addForm"
                label-width="70px"
                label-position="top"
                @submit.native.prevent>
                <el-form-item :label=dialogTitle>
                    <el-input
                        v-model="addForm.addInfo"
                        clearable
                        placeholder="请输入添加信息"
                        minlength="7"
                        maxlength="15"
                        show-word-limit
                        ></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveAdd">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import Axios from 'axios';
export default {
    name: 'baseform',
    data() {
        return {
            smtpbanIP: {
                ipList:[],
            },
            smtpbanAccount: {
                accountList:[],
            },
            pop3banIP: {
                ipList:[],
            },
            pop3banAccount: {
                accountList:[],
            },
            configForm: {
                server: {
                    domain: "test.com",
                    mailMaxSize: 0,
                    logMaxSize: 0
                }, 
                smtp: {
                    port: 8025,
                    logDir: "\\log\\smtp",
                    banIPs: [],
                    banActs: []
                }, 
                pop3: {
                    port: 8110,
                    logDir: "\\log\\pop3",
                    banIPs: [],
                    banActs: []
                }
            },
            addVisible: false,
            dialogTitle: "",
            addForm: {
                addInfo: "",
            }
        };
    },
    created() {
        this.getData();
    },
    methods: {
        // 获得数据
        getData() {
            let requestURL = 'apis/webmail/showconfig/'

            Axios
                .get(requestURL)
                .then(response => {
                    this.configForm = JSON.parse(response.data.data);
                    
                    // console.log(JSON.stringify(this.configForm));
                    this.smtpbanIP.ipList = [];
                    this.smtpbanAccount.accountList = [];
                    this.pop3banIP.ipList = [];
                    this.pop3banAccount.accountList = [];
                    for (let index in this.configForm.smtp.banIPs)
                    {
                        this.smtpbanIP.ipList.push({'banIP': this.configForm.smtp.banIPs[index]})
                    }
                    for (let index in this.configForm.smtp.banActs)
                    {
                        this.smtpbanAccount.accountList.push({'banAccount': this.configForm.smtp.banActs[index]})
                    }
                    for (let index in this.configForm.pop3.banIPs)
                    {
                        this.pop3banIP.ipList.push({'banIP': configForm.pop3.banIPs[index]})
                    }
                    for (let index in this.configForm.pop3.banActs)
                    {
                        this.pop3banAccount.accountList.push({'banAccount': this.configForm.pop3.banActs[index]})
                    }
                })
                .catch(() => {
                    this.$message({
                        type: 'error',
                        message: '配置信息获取失败'
                    })
                })

        },
        // 添加操作
        handleAdd(addType) {
            this.addVisible = true;
            this.dialogTitle = addType;
        },
        //提交添加
        saveAdd() {
            let requestURL = 'apis/webmail/modifyconfig/';
            if (this.dialogTitle == "添加SMTP屏蔽IP")
            {
                this.configForm.smtp.banIPs.push(this.addForm.addInfo);
            }
            else if (this.dialogTitle == "添加SMTP屏蔽用户")
            {
                this.configForm.smtp.banActs.push(this.addForm.addInfo);
            }
            else if (this.dialogTitle == "添加POP3屏蔽IP")
            {
                this.configForm.pop3.banIPs.push(this.addForm.addInfo);
            }
            else if (this.dialogTitle == "添加POP3屏蔽用户")
            {
                this.configForm.pop3.banActs.push(this.addForm.addInfo);
            }
            else
            {
                this.$message.error("表单类型非法，请重试");
            }

            this.addVisible = false;
            this.onSubmit();
        },
        // SMTP屏蔽IP删除操作
        handleSmtpIpDelete(index, row) {
            // 二次确认删除
            this.$confirm('确定要删除该SMTP屏蔽IP吗？', '提示', {
                type: 'warning'
            })
            .then(() => {
                this.configForm.smtp.banIPs.splice(index,1);
                // console.log(JSON.stringify(this.configForm.smtp.banIPs))

                this.onSubmit();
            })
            .catch(() => {
                this.$message({
                    type: 'info',
                    message: '删除操作已取消'
                })
            });
        },
        // SMTP屏蔽用户删除操作
        handleSmtpAccountDelete(index, row) {
            // 二次确认删除
            this.$confirm('确定要删除该SMTP屏蔽用户吗？', '提示', {
                type: 'warning'
            })
            .then(() => {
                this.configForm.smtp.banActs.splice(index,1);
                // console.log(JSON.stringify(this.configForm.smtp.banActs))

                this.onSubmit();
            })
            .catch(() => {
                this.$message({
                    type: 'info',
                    message: '删除操作已取消'
                })
            });
        },
        // SMTP屏蔽IP删除操作
        handlePop3IpDelete(index, row) {
            // 二次确认删除
            this.$confirm('确定要删除该POP3屏蔽IP吗？', '提示', {
                type: 'warning'
            })
            .then(() => {
                this.configForm.pop3.banIPs.splice(index,1);
                // console.log(JSON.stringify(this.configForm.pop3.banIPs))

                this.onSubmit();
            })
            .catch(() => {
                this.$message({
                    type: 'info',
                    message: '删除操作已取消'
                })
            });
        },
        // SMTP屏蔽用户删除操作
        handlePop3AccountDelete(index, row) {
            // 二次确认删除
            this.$confirm('确定要删除该POP3屏蔽用户吗？', '提示', {
                type: 'warning'
            })
            .then(() => {
                this.configForm.pop3.banActs.splice(index,1);
                // console.log(JSON.stringify(this.configForm.pop3.banActs))

                this.onSubmit();
            })
            .catch(() => {
                this.$message({
                    type: 'info',
                    message: '删除操作已取消'
                })
            });
        },
        // 重置配置为默认配置
        resetConfig() {
            this.$confirm('确定要重置所有配置为默认配置吗？', '提示', {
                type: 'warning'
            })
            .then(() => {
                let requestURL = '/apis/webmail/resetconfig/'

                Axios
                    .get(requestURL)
                    .then(response => {
                        this.configForm = JSON.parse(response.data.data);
                    
                        // console.log(JSON.stringify(this.configForm));
                        this.smtpbanIP.ipList = [];
                        this.smtpbanAccount.accountList = [];
                        this.pop3banIP.ipList = [];
                        this.pop3banAccount.accountList = [];
                        for (let index in this.configForm.smtp.banIPs)
                        {
                            this.smtpbanIP.ipList.push({'banIP': this.configForm.smtp.banIPs[index]})
                        }
                        for (let index in this.configForm.smtp.banActs)
                        {
                            this.smtpbanAccount.accountList.push({'banAccount': this.configForm.smtp.banActs[index]})
                        }
                        for (let index in this.configForm.pop3.banIPs)
                        {
                            this.pop3banIP.ipList.push({'banIP': configForm.pop3.banIPs[index]})
                        }
                        for (let index in this.configForm.pop3.banActs)
                        {
                            this.pop3banAccount.accountList.push({'banAccount': this.configForm.pop3.banActs[index]})
                        }

                        this.$message({
                            type: 'success',
                            message: '重置配置获取成功'
                        })
                    })
                    .catch(() => {
                        this.$message({
                            type: 'error',
                            message: '重置配置获取失败'
                        })
                    })
            })
            .catch(() => {
                this.$message({
                    type: 'info',
                    message: '重置操作已取消'
                })
            });
        },
        // 提交修改
        onSubmit() {
            let requestURL = 'apis/webmail/modifyconfig/';
            let data = new FormData();
            data.append("configJson",JSON.stringify(this.configForm));

            Axios
                .post(requestURL, data)
                .then(response => {
                    if (response.data.status == 200)
                    {
                        this.$message.success('提交成功');
                    }
                })
                .catch(()=>{
                    this.$message({
                        type: 'error',
                        message: '配置信息提交失败'
                    })
                })
            
            this.getData();
        }
    }
};
</script>

<style scoped>
.handle-box {
    margin-bottom: 20px;
}

.handle-select {
    width: 120px;
}

.handle-input {
    width: 300px;
    display: inline-block;
}
.table {
    width: 100%;
    font-size: 14px;
}
.red {
    color: #ff0000;
}
.green {
    color: rgb(35, 214, 74);
}
.mr10 {
    margin-right: 10px;
}
.table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
}
</style>