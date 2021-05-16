<template>
    <div class="" v-loading="loading">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-copy"></i> 日志管理</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-tabs v-model="message">
                <el-tab-pane :label="`SMTP日志(${smtpLogList.length})`" name="first">
                    <el-table :data="smtpLogList" :show-header="false" style="width: 100%">
                        <el-table-column>
                            <template slot-scope="scope">
                                <span class="message-title" @click="showSmtpLog(scope.$index)">{{scope.row.logName}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="logTime" width="180"></el-table-column>
                        <el-table-column width="120">
                            <template slot-scope="scope">
                                <el-button type="danger" @click="handleDelSmtpLog(scope.$index)">删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div class="handle-row">
                        <el-button type="danger" @click="delAllSmtpLog()">删除全部</el-button>
                    </div>
                </el-tab-pane>
                <el-tab-pane :label="`POP3日志(${pop3LogList.length})`" name="second">
                    <el-table :data="pop3LogList" :show-header="false" style="width: 100%">
                        <el-table-column>
                            <template slot-scope="scope">
                                <span class="message-title" @click="showPop3Log(scope.$index)">{{scope.row.logName}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="logTime" width="150"></el-table-column>
                        <el-table-column width="120">
                            <template slot-scope="scope">
                                <el-button type="danger" @click="handleDelPop3Log(scope.$index)">删除</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    <div class="handle-row">
                        <el-button type="danger" @click="delAllPop3Log()">删除全部</el-button>
                    </div>
                </el-tab-pane>
            </el-tabs>
        </div>
        <!-- 新增信息弹出框 -->
        <el-dialog :title="dialogTitle" :visible.sync="logVisible" width="50%">
            <!-- <el-form
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
            </el-form>-->
            <span style="white-space: pre-line">{{this.logContent}}</span>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="logVisible = false">关 闭</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import Axios from 'axios'
    export default {
        name: 'tabs',
        data() {
            return {
                loading: false,
                message: 'first',
                dialogTitle: "日志",
                logVisible: false,
                logContent: "",
                smtpLogList: [{
                    logName: 'SMTP日志',
                    logTime: '2018-04-19 20:00:00',
                    logContent: 'Nothing to log'
                },],
                pop3LogList: [,{
                    logName: 'POP3日志',
                    logTime: '2018-04-19 21:00:00',
                    logContent: 'Nothing to log'
                }]
            }
        },
        created() {
            this.getAllLog()
        },
        methods: {
            // 获取所有日志文件
            getAllLog() {
                this.loading = true;
                let requestURL = '/apis/webmail/getlog/';
                let data = new FormData();
                data.append("logType",0)
                Axios
                    .post(requestURL,data)
                    .then(response => {
                        // console.log(JSON.parse(response.data.data));
                        this.smtpLogList = JSON.parse(response.data.data);
                    })
                    .catch(() => {
                        this.loading = false;
                        this.$message({
                            type: 'error',
                            message: 'SMTP日志内容获取失败'
                        })
                    })
                
                let requestURL2 = '/apis/webmail/getlog/';
                let data2 = new FormData();
                data2.append("logType",1)
                Axios
                    .post(requestURL2,data2)
                    .then(response => {
                        console.log(JSON.parse(response.data.data));
                        this.pop3LogList = JSON.parse(response.data.data);
                        this.loading = false;
                    })
                    .catch(() => {
                        this.loading = false;
                        this.$message({
                            type: 'error',
                            message: 'POP3日志内容获取失败'
                        })
                    })
            },
            //展示smtp日志
            showSmtpLog(index) {
                this.logVisible = true;
                this.logContent = this.smtpLogList[index].logContent;
            },
            // 展示pop3日志
            showPop3Log(index) {
                this.logVisible = true;
                this.logContent = this.pop3LogList[index].logContent;
            },
            // 删除指定SMTP日志文件
            handleDelSmtpLog(index) {
                this.loading = true;
                let requestURL = '/apis/webmail/dellog/';
                let data = new FormData();
                data.append("logType",0)

                let logIndexList = [];
                logIndexList.push(index + 1);

                data.append("logIndexList",JSON.stringify(logIndexList))
                Axios
                    .post(requestURL,data)
                    .then(response => {
                        if (response.data.status == 200)
                        {
                            this.$message.success("删除成功");
                        }
                        else if (response.data.status == 201)
                        {
                            this.$message.error("删除失败");
                        }
                    })
                    .catch(() => {
                        this.$message({
                            type: 'error',
                            message: '指定日志删除失败'
                        })
                    })

                setTimeout(() => {
                    this.getAllLog()
                }, 1000);
            },
            // 删除指定POP3日志文件
            handleDelPop3Log(index) {
                this.loading = true;
                let requestURL = '/apis/webmail/dellog/';
                let data = new FormData();
                data.append("logType",1)

                let logIndexList = [];
                logIndexList.push(index + 1);

                data.append("logIndexList",JSON.stringify(logIndexList))
                console.log(JSON.stringify(logIndexList))
                Axios
                    .post(requestURL,data)
                    .then(response => {
                        if (response.data.status == 200)
                        {
                            this.$message.success("删除成功");
                        }
                        else if (response.data.status == 201)
                        {
                            this.$message.error("删除失败");
                        }
                    })
                    .catch(() => {
                        this.$message({
                            type: 'error',
                            message: '指定日志删除失败'
                        })
                    })

                setTimeout(() => {
                    this.getAllLog()
                }, 1000);
            },
            // 删除所有SMTP日志文件
            delAllSmtpLog() {
                this.loading = true;
                let requestURL = '/apis/webmail/dellog/';
                let data = new FormData();
                data.append("logType",0)

                let logIndexList = [];
                let length = this.smtpLogList.length;
                for(let i=0;i<length;i++)
                {
                    logIndexList.push(i+1);
                }
                if(logIndexList.length == 0)
                {
                    this.$message.error("当前没有可删除的SMTP日志");
                    return;
                }

                data.append("logIndexList",JSON.stringify(logIndexList))
                Axios
                    .post(requestURL,data)
                    .then(response => {
                        if (response.data.status == 200)
                        {
                            this.$message.success("全部删除成功");
                        }
                        else if (response.data.status == 201)
                        {
                            this.$message.error("存在部分删除失败");
                        }
                    })
                    .catch(() => {
                        this.$message({
                            type: 'error',
                            message: 'SMTP日志删除失败'
                        })
                    })

                setTimeout(() => {
                    this.getAllLog()
                }, 1000);
            },
            // 删除所有POP3日志文件
            delAllPop3Log() {
                this.loading = true;
                let requestURL = '/apis/webmail/dellog/';
                let data = new FormData();
                data.append("logType",1)

                let logIndexList = [];
                let length = this.pop3LogList.length;
                for(let i=0;i<length;i++)
                {
                    logIndexList.push(i+1);
                }

                if(logIndexList.length == 0)
                {
                    this.$message.error("当前没有可删除的POP3日志");
                    return;
                }

                data.append("logIndexList",JSON.stringify(logIndexList))
                Axios
                    .post(requestURL,data)
                    .then(response => {
                        if (response.data.status == 200)
                        {
                            this.$message.success("全部删除成功");
                        }
                        else if (response.data.status == 201)
                        {
                            this.$message.error("存在部分删除失败");
                        }
                    })
                    .catch(() => {
                        this.$message({
                            type: 'error',
                            message: 'POP3日志删除失败'
                        })
                    })

                setTimeout(() => {
                    this.getAllLog()
                }, 1000);
            },
        }
    }

</script>

<style>
.message-title{
    cursor: pointer;
}
.handle-row{
    margin-top: 30px;
}
</style>

